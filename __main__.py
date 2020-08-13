import tkinter
from window import Window
from interpreter import Interpreter
from renderer import Renderer
from file_io import FileIO

def main():

    root = tkinter.Tk()

    # OpenGL display
    display = Renderer()

    # Chip-8 interpreter
    interpreter = Interpreter(display)

    # File manager
    file_io = FileIO(interpreter)

    window = Window(root, display, interpreter, file_io, width=720, height=480)

    # Setup the window frame
    menu_bar = tkinter.Menu(root)
    file_menu = tkinter.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open ROM", command=file_io.open)
    file_menu.add_command(label="Save state", command=file_io.save_state)
    file_menu.add_command(label="Load state", command=file_io.load_state())

    file_menu.add_separator()

    file_menu.add_command(label="Quit", command=window.close)
    menu_bar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menu_bar)

    root.protocol("WM_DELETE_WINDOW", window.close)
    window.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    # Approximate milliseconds between update calls
    window.animate = int(1000 / display.max_fps)
    window.after(100, window.printContext)
    window.mainloop()


if __name__ == '__main__':
    main()
