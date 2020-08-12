import tkinter
from tkinter import Tk, Menu
from window import Window
from interpreter import Interpreter
from renderer import Renderer
from file_io import FileIO
import os

def main():

    root = tkinter.Tk()
    window = Window(root, width=720, height=480)
    # OpenGL display
    display = Renderer()
    interpreter = Interpreter(display)
    file_io = FileIO(interpreter)
    window.display = display
    window.file_io = file_io
    window.interpreter = interpreter
    # Setup the window frame
    menu_bar = Menu(root)
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open ROM", command=file_io.open)
    file_menu.add_command(label="Save state", command=file_io.save_state)
    file_menu.add_command(label="Load state", command=file_io.load_state())

    file_menu.add_separator()

    file_menu.add_command(label="Quit", command=window.close)
    menu_bar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menu_bar)

    root.protocol("WM_DELETE_WINDOW", window.close)
    window.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    window.animate = 1
    window.after(100, window.printContext)
    window.mainloop()


if __name__ == '__main__':
    main()
