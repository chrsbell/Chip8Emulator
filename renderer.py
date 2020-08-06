import OpenGL.GL as GL
import OpenGL.GL.shaders
import numpy
import ctypes
import contextlib

class Renderer:

    def __init__(self):
        # Actual window size
        self.window_width = 640
        self.window_height = 480

        # Chip-8 display
        self.display_width = 64
        self.display_height = 32

        # A Chip-8 pixel is either on or off, 4 vertices per pixel
        self.display_buffer = [1] * (4 * self.display_height * self.display_width)
        self.vertex_buffer = []

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
    def create_program(self):
        """Creates the shader and vertex buffers"""
        with self.bind_shader():
            with self.create_vertex_objects():
                yield

    @contextlib.contextmanager
    def create_vertex_objects(self):
        """Generates the VAO and VBOs"""
        # The VAO contains both position and color VBOs
        vertex_array_object = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vertex_array_object)
        # Generate two VBOs
        self.buffer_object = GL.glGenBuffers(2)
        try:
            with self.add_attributes(['position', 'pixel_state']):
                # Bind the position buffer and describe/send its data
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_object[0])
                GL.glVertexAttribPointer(self.attributes['position'], 2, GL.GL_FLOAT, False, 0,
                                         ctypes.c_void_p(0))

                # Add vertices of 'pixels' to the buffer
                # The position of each vertex is in normalized device coordinate space
                x_increment = 2.0 / self.display_width
                y_increment = 2.0 / self.display_height
                for j in range(self.display_height):
                    for i in range(self.display_width):
                        # Add each 'pixel' to the list
                        top_left = [-1.0 + (i * x_increment), -1.0 + (j * y_increment)]
                        self.vertex_buffer.extend([top_left[0], top_left[1]])
                        self.vertex_buffer.extend([top_left[0] + x_increment, top_left[1]])
                        self.vertex_buffer.extend([top_left[0] + x_increment, top_left[1] + y_increment])
                        self.vertex_buffer.extend([top_left[0], top_left[1] + y_increment])
                self.vertex_buffer = numpy.array(self.vertex_buffer, dtype=numpy.float32)
                # Size of float (4) *  number of components in a vertex (2) * number of vertices in a square (4) * number of 'pixels'
                GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 2 * 4 * self.display_height * self.display_width,
                                self.vertex_buffer, GL.GL_STATIC_DRAW)

                # Bind the color buffer and describe/send its data
                GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffer_object[1])
                GL.glVertexAttribPointer(self.attributes['pixel_state'], 1, GL.GL_INT, False, 0,
                                         ctypes.c_void_p(0))
                self.display_buffer = numpy.array(self.display_buffer, dtype=numpy.int32)
                for i in range(256, 512):
                    self.display_buffer[i] = 0.0
                # Size of float (4) * number of vertices in a square (4) * number of 'pixels'
                GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 4 * self.display_height * self.display_width,
                                self.display_buffer, GL.GL_STATIC_DRAW)
                yield
        finally:
            # Unbind VAO first, then VBO
            GL.glBindVertexArray(0)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glDeleteBuffers(1, self.buffer_object)

    def display(self):
        """Draw each 'pixel\'"""
        # Clear the color buffer first
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_QUADS, 0, 4 * self.display_height * self.display_width)