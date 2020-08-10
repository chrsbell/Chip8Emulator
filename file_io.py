from tkinter import filedialog


class FileIO:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.file_open = False
        return

    def open(self):
        filename = filedialog.askopenfilename(title="Select a ROM")
        # Open in binary mode
        with open(filename, 'rb') as file:
            self.interpreter.load_program_to_memory(file)
            self.file_open = True

    def save_state(self):
        """Save the interpreter state"""
        return

    def load_state(self):
        """Load a saved interpreter state"""
        return