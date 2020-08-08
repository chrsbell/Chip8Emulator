from tkinter import filedialog


class FileIO:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        return

    def open(self):
        filename = filedialog.askopenfilename(title="Select a ROM")
        # Open in binary mode
        with open(filename, 'rb') as file:
            self.interpreter.load_program_to_memory(file)
        return
