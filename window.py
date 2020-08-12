import os
from tkinter import Menu, Tk, Toplevel, Button, Frame, messagebox
from renderer import Renderer
from OpenGL.error import GLError
from pyopengltk import OpenGLFrame
import time


class Window(OpenGLFrame):

    def initgl(self):
        """Uses a programmable pipeline PyOpenGL based tkinter window"""

        self.start = time.time()
        self.nframes = 0

        if self.display:
            try:
                # Compile the shader and create the vertex buffers
                self.display.bind_shader()
                self.display.create_vertex_objects()
            except GLError as gl_error:
                # Format and show an error
                gl_error.format_description('description', gl_error.description)
                messagebox.showerror("OpenGL Error: " + str(gl_error.err), error.description + str.encode(" at ") +
                                     str.encode('%s' % gl_error.baseOperation.__name__))
                self.close()

    def redraw(self):
        #self.clock.tick(1000)
        if self.file_io.file_open:
            self.interpreter.execute_instruction()
        tm = time.time() - self.start
        self.nframes += 1
        self.display.max_fps = self.nframes / tm
        self.display.render()
        #for event in pygame.event.get():
        #    if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        #        return
        #self.title("Chip-8 Emulator " + "~ " + self.file_io.rom + " ~ FPS: " + str(int(self.clock.get_fps())))

    def close(self):
        self.display.destroy()
        self.tk.quit()
