import pygame
import os
from tkinter import Menu, Tk, Toplevel, Button, Frame, messagebox
from renderer import Renderer
import contextlib
from OpenGL.error import GLError


class Window:

    def __init__(self):
        """Uses a programmable pipeline PyOpenGL based PyGame window
        embedded in a tkinter interface for file interaction"""

        # Main window
        self.root = Tk()
        # OpenGL display
        self.display = Renderer()

        # Setup the window frame
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open ROM", command=self.donothing)
        self.file_menu.add_command(label="Save state", command=self.donothing)
        self.file_menu.add_command(label="Load state", command=self.donothing)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Quit", command=self.close)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.root.config(menu=self.menu_bar)

        embed = Frame(self.root, width=self.display.window_width, height=self.display.window_height)
        embed.pack()

        # Set the OS window ID for PyGame to use
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        self.root.update()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # PyGame window wrapper for OpenGL display, used for keyboard input also
        pygame.init()
        pygame.display.set_mode((self.display.window_width, self.display.window_height),
                                pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.i = 0
        self.error = False
        self.quit = False

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def show_opengl_error(self, error):
        self.error = True
        # Format and show an error
        error.format_description('description', error.description)
        messagebox.showerror("OpenGL Error: " + str(error.err), error.description + str.encode(" at ") +
                             str.encode('%s' % error.baseOperation.__name__))

    @contextlib.contextmanager
    def init_opengl(self):
        # Context manager handles deallocation of OpenGL resources when quitting
        try:
            # Compile the shader and create the vertex buffers
            with self.display.bind_shader():
                with self.display.create_vertex_objects():
                    yield
        except GLError as gl_error:
            self.show_opengl_error(gl_error)
            self.close()
            yield

    def update(self):
        if self.i < (self.display.width * self.display.height):
            self.display.set_pixel(self.i, 0, 1)
            self.i += 1
        self.clock.tick(self.display.max_fps)
        self.display.render()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return
        self.root.title("Chip-8 Emulator " + " ~ FPS: " + str(int(self.clock.get_fps())))
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        pygame.quit()
        self.root.quit()
        self.quit = True