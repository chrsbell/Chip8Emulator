from tkinter import filedialog
import ntpath

class FileIO:
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.file_open = False
        self.rom = ''
        self.filename = ''
        return

    def open(self):
        self.filename = filedialog.askopenfilename(title='Select a ROM')
        # Strip file string from path string
        if not isinstance(self.filename, str):
            return
        self.rom = ntpath.basename(self.filename)
        # Open in binary mode
        try:
            with open(self.filename, 'rb') as file:
                self.interpreter.load_program_to_memory(file)
                self.file_open = True
        except IOError as error:
            self.file_open = False

    def save_state(self):
        """Save the interpreter state"""
        return

    def load_state(self):
        """Load a saved interpreter state"""
        return