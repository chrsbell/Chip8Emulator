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

        self.attributes = {}
        self.shader = 0

        self.vertex_shader = """
        #version 410

        in vec4 position;
        void main()
        {
           gl_Position = position;
        }
        """

        self.fragment_shader = """
        #version 410

        void main()
        {
           gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
        }
        """

        GL.glClearColor(0.5, 0.5, 0.5, 1.0)
        GL.glEnable(GL.GL_DEPTH_TEST)

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
        """Generates the VAO and VBO"""
        vertex_array_object = GL.glGenVertexArrays(1)
        vertex_buffer = GL.glGenBuffers(1)
        try:
            # Bind the buffers
            GL.glBindVertexArray(vertex_array_object)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)

            with self.add_attributes(['position']):
                # Describe vertex information
                GL.glVertexAttribPointer(self.attributes['position'], 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))

                # Add vertices to the buffer
                x_increment = 2.0 / self.display_width
                y_increment = 2.0 / self.display_height
                vertices = []
                for i in range(self.display_width):
                    for j in range(self.display_height):
                        top_left = [-1.0 + (i * x_increment), -1.0 + (j * y_increment)]
                        vertices.extend([top_left[0], top_left[1], 0.0, 1.0])
                        vertices.extend([top_left[0] + x_increment, top_left[1], 0.0, 1.0])
                        vertices.extend([top_left[0] + x_increment, top_left[1] + y_increment, 0.0, 1.0])
                        vertices.extend([top_left[0], top_left[1] + y_increment, 0.0, 1.0])
                vertices = numpy.array(vertices, dtype=numpy.float32)
                # Size of float (4) *  number of components in a vertex (4) * number of vertices in a square (4)
                GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 4 * 4 * self.display_width * self.display_height,
                                vertices, GL.GL_STATIC_DRAW)
                yield
        finally:
            # Unbind VAO first, then VBO
            GL.glBindVertexArray(0)
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
            GL.glDeleteBuffers(1, [vertex_buffer])

    def display(self):
        """Draw each 'pixel\'"""
        # Clear the color/depth buffers first
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_QUADS, 0, 4 * self.display_height * self.display_width)
