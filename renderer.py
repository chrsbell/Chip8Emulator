import numpy as np
import ctypes
import contextlib
import OpenGL
# Manually show errors
OpenGL.ERROR_LOGGING = False
# Ensure we use numpy arrays instead of lists to prevent copying data
OpenGL.ERROR_ON_COPY = True
import OpenGL.GL as GL
import OpenGL.GL.shaders


class Renderer:

    def __init__(self):
        """Modern OpenGL rendering class"""

        # Chip-8 display
        self.width = 64
        self.height = 32

        # Actual window size
        self.window_width = 1024
        self.window_height = 576

        self.max_fps = 60

        # Whether each pixel is on or off
        self.display_state = [[0 for y in range(self.height)] for x in range(self.width)]

        # Objects for vertex/color buffers
        self.buffer_object = np.array([])
        # Using 4 vertices per 'pixel'
        self.display_buffer = np.array([0] * (4 * self.height * self.width), np.int32)
        self.vertex_buffer = []
        self.vertex_array_object = 0

        self.attributes = {}
        self.shader = 0

        self.vertex_shader = """
        #version 330

        in vec2 position;
        in int pixel_state;
        flat out int color; //don't interpolate the color
        void main()
        {
           color = pixel_state;
           gl_Position.xy = position.xy;
           gl_Position.zw = vec2(0.0, 1.0);
        }
        """

        self.fragment_shader = """
        #version 330
        
        flat in int color;
        void main()
        {
           gl_FragColor = vec4(color, color, color, color);
        }
        """

    @contextlib.contextmanager
    def add_attributes(self, attributes):
        """Gets location of each string attribute in the shader and enables it"""
        try:
            for attribute in attributes:
                self.attributes[attribute] = GL.glGetAttribLocation(self.shader, attribute)
                GL.glEnableVertexAttribArray(self.attributes[attribute])
            yield
        finally:
            for attribute in self.attributes.values():
                GL.glDisableVertexAttribArray(attribute)

    @contextlib.contextmanager
    def bind_shader(self):
        """Compiles and binds the shader program"""
        try:
            self.shader = OpenGL.GL.shaders.compileProgram(
                OpenGL.GL.shaders.compileShader(self.vertex_shader, GL.GL_VERTEX_SHADER),
                OpenGL.GL.shaders.compileShader(self.fragment_shader, GL.GL_FRAGMENT_SHADER)
            )
            GL.glUseProgram(self.shader)
            yield
        finally:
            GL.glUseProgram(0)

    @contextlib.contextmanager
    def create_vertex_objects(self):
        """Generates the VAO and VBOs"""
        # Shader attributes
        attribute_names = ['position', 'pixel_state']
        # The VAO contains both position and color VBOs
        self.vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vertex_array_object)
        # Generate VBOs for each of the shader attributes
        self.buffer_object = GL.glGenBuffers(len(attribute_names))
        try:
            with self.add_attributes(attribute_names):
                # Bind the position buffer and describe/send its data
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_object[0])
                GL.glVertexAttribPointer(self.attributes['position'], 2, GL.GL_FLOAT, False, 0,
                                         ctypes.c_void_p(0))
                # Add vertices of 'pixels' to the buffer
                # The position of each vertex is in normalized device coordinate space
                x_increment = 2.0 / self.width
                y_increment = 2.0 / self.height
                for y in range(self.height):
                    for x in range(self.width):
                        # Add each 'pixel' to the list
                        top_left = [-1.0 + (x * x_increment), -1.0 + (y * y_increment)]
                        self.vertex_buffer.extend([top_left[0], top_left[1]])
                        self.vertex_buffer.extend([top_left[0] + x_increment, top_left[1]])
                        self.vertex_buffer.extend([top_left[0] + x_increment, top_left[1] + y_increment])
                        self.vertex_buffer.extend([top_left[0], top_left[1] + y_increment])
                self.vertex_buffer = np.array(self.vertex_buffer, np.float32)
                # sizeof float (4) * vertex components (2) * vertices in square (4) * number of 'pixels'
                GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 2 * 4 * self.height * self.width,
                                self.vertex_buffer, GL.GL_STATIC_DRAW)

                # Bind the color buffer and describe/send its data
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_object[1])
                GL.glVertexAttribPointer(self.attributes['pixel_state'], 1, GL.GL_INT, False, 0,
                                         ctypes.c_void_p(0))
                # Size of int (4) * number of vertices in a square (4) * number of 'pixels'
                GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 4 * self.height * self.width,
                                self.display_buffer, GL.GL_DYNAMIC_DRAW)
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
                yield
        finally:
            # Unbind and delete VAO first, then VBOs
            GL.glBindVertexArray(0)
            GL.glDeleteVertexArrays(1, np.array([self.vertex_array_object]))
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glDeleteBuffers(len(self.attributes), self.buffer_object)

    def get_pixel(self, x, y):
        return self.display_state[x][y]

    def set_pixel(self, x, y, on):
        # Get offset into buffer and update only that pixel
        start = (y * self.width * 4 * 4) + (x * 4 * 4)
        data = np.array([np.int32(on)] * 4, np.int32)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_object[1])
        GL.glBufferSubData(GL.GL_ARRAY_BUFFER, start, 4 * 4, data)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        # Update display state for interpreter
        self.display_state[x][y] = on

    def clear_screen(self):
        for x in self.width:
            for y in self.height:
                self.set_pixel(x, y, 0)

    def render(self):
        """Draw each 'pixel'"""
        # Clear the color buffer first
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_QUADS, 0, 4 * self.height * self.width)
