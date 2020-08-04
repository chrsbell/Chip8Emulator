import OpenGL.GL as GL
import OpenGL.GL.shaders
import ctypes
import pygame
import numpy

#actual window
window_width = 640
window_height = 480

#chip-8 display
display_width = 64
display_height = 32

vertex_shader = """
#version 410

in vec4 position;
void main()
{
   gl_Position = position;
}
"""

fragment_shader = """
#version 410

void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

def create_object(shader):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vertex_array_object)

    # Generate buffers to hold our vertices
    vertex_buffer = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vertex_buffer)

    # Get the position of the 'position' in parameter of our shader and bind it.
    position = GL.glGetAttribLocation(shader, 'position')
    GL.glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    GL.glVertexAttribPointer(position, 4, GL.GL_FLOAT, False, 0, ctypes.c_void_p(0))

    # Send the data over to the buffer
    x_incr = 2.0 / display_width
    y_incr = 2.0 / display_height
    vertices = []
    for i in range(display_width):
        for j in range(display_height):
            top_left = [-1.0 + (i * x_incr), -1.0 + (j * y_incr)]
            vertices.extend([top_left[0], top_left[1], 0.0, 1.0])
            vertices.extend([top_left[0] + x_incr, top_left[1], 0.0, 1.0])
            vertices.extend([top_left[0] + x_incr, top_left[1] + y_incr, 0.0, 1.0])
            vertices.extend([top_left[0], top_left[1] + y_incr, 0.0, 1.0])
    vertices = numpy.array(vertices, dtype=numpy.float32)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, 4 * 4 * 4 * display_width * display_height, vertices, GL.GL_DYNAMIC_DRAW)

    # Unbind the VAO first (Important)
    GL.glBindVertexArray(0)

    # Unbind other stuff
    GL.glDisableVertexAttribArray(position)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    return vertex_array_object


def display(shader, vertex_array_object):
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glUseProgram(shader)

    GL.glBindVertexArray(vertex_array_object)
    # draw each pixel
    GL.glDrawArrays(GL.GL_QUADS, 0, 4 * display_height * display_width)
    GL.glBindVertexArray(0)

    GL.glUseProgram(0)


def update_fps(clock):
    fps = str(int(clock.get_fps()))
    return fps


def main():
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height), pygame.OPENGL | pygame.DOUBLEBUF)
    GL.glClearColor(0.5, 0.5, 0.5, 1.0)
    GL.glEnable(GL.GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER)
    )

    vertex_array_object = create_object(shader)

    clock = pygame.time.Clock()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return

        print(update_fps(clock))
        clock.tick()
        display(shader, vertex_array_object)
        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
