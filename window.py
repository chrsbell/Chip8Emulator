from tkinter import messagebox
from OpenGL.error import GLError
from pyopengltk import OpenGLFrame
import time


class Window(OpenGLFrame):

    def __init__(self, master=None, display=0, interpreter=0, file_io=0, keymap=0, cnf={}, **kw):
        """The main tkinter window"""
        # Inherits from BaseOpenGLFrame
        super().__init__(master, cnf, **kw)
        # Actual window size
        self.window_width = kw['width']
        self.window_height = kw['height']

        # Used for FPS calculations
        self.start = time.time()
        self.delta = 0

        self.display = display
        self.interpreter = interpreter
        self.file_io = file_io
        self.keymap = keymap

    def initgl(self):
        """Uses a programmable pipeline PyOpenGL based tkinter window"""
        try:
            # Compile the shader and create the vertex buffers
            self.display.bind_shader()
            self.display.create_vertex_objects()
        except GLError as gl_error:
            # Format and show an error
            gl_error.format_description('description', gl_error.description)
            messagebox.showerror("OpenGL Error: " + str(gl_error.err), gl_error.description + str.encode(" at ") +
                                 str.encode('%s' % gl_error.baseOperation.__name__))
            self.close()

    def redraw(self):
        if self.file_io.file_open and not self.interpreter.error:
            self.interpreter.execute_instruction()

        self.display.render()

        # Update the FPS
        end = time.time()
        self.delta = end - self.start
        self.start = end
        self.master.title("Chip-8 Emulator " + "~ " + self.file_io.rom + " ~ FPS: " + str(int(1.0 / self.delta)))

    def close(self):
        self.display.destroy()
        self.tk.quit()
