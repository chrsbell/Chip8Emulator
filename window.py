"""
MIT License

Copyright (c) 2020 Chris Bell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from tkinter import messagebox
from OpenGL.error import GLError
from pyopengltk import OpenGLFrame
import time


class Window(OpenGLFrame):

    def __init__(self, master=None, display=0, interpreter=0, file_io=0, keymap=0, audio=0, cnf={}, **kw):
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
        self.audio = audio

    def initgl(self):
        """Compile the shaders and creates the vertex buffers"""
        try:
            self.display.bind_shader()
            self.display.create_vertex_objects()
        except GLError as gl_error:
            # Format and show an error
            gl_error.format_description('description', gl_error.description)
            messagebox.showerror("OpenGL Error: " + str(gl_error.err), gl_error.description + str.encode(" at ") +
                                 str.encode('%s' % gl_error.baseOperation.__name__))
            self.close()

    def redraw(self):
        """Main execution loop"""
        if self.file_io.file_open and not self.interpreter.error:
            # Check if executing Fx0A
            if not self.interpreter.wait_for_key:
                self.interpreter.execute_instruction()
            elif self.keymap.keydown:
                # Continue execution from opcode Fx0A
                x = self.interpreter.x
                self.interpreter.wait_for_key = False
                self.interpreter.register_v[x] = self.keymap.key
                self.interpreter.program_counter += 2

        self.display.render()

        # Update the FPS
        end = time.time()
        self.delta = end - self.start
        self.start = end
        self.master.title("Chip-8 Emulator " + "~ " + self.file_io.rom + " ~ FPS: " + str(int(1.0 / self.delta)))

    def close(self):
        self.display.destroy()
        self.tk.quit()
