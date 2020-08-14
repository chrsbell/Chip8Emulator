from tkinter import messagebox, Toplevel, Button
from functools import partial


class Keymap:
    def __init__(self, root, interpreter):
        """Represents the Chip-8 hexadecimal keypad"""
        self.root = root
        self.interpreter = interpreter
        self.keymap_frame = None
        # Whether window is open
        self.editing = False
        # Whether we are listening for keyboard input to map
        self.listening = False
        # Hexadecimal keypad buttons mapped to keyboard characters
        self.key = {'1': -1,
                    '2': -1,
                    '3': -1,
                    '4': -1,
                    '5': -1,
                    '6': -1,
                    '7': -1,
                    '8': -1,
                    '9': -1,
                    'A': -1,
                    'B': -1,
                    'C': -1,
                    'D': -1,
                    'E': -1,
                    'F': -1}

        # Dictionary of tk buttons
        self.button = {'1': None,
                       '2': None,
                       '3': None,
                       '4': None,
                       '5': None,
                       '6': None,
                       '7': None,
                       '8': None,
                       '9': None,
                       'A': None,
                       'B': None,
                       'C': None,
                       'D': None,
                       'E': None,
                       'F': None}

    def add_button(self, hex, row, column):
        self.button[hex] = Button(self.keymap_frame, text=hex, command=partial(self.add_listener, hex))
        self.button[hex].grid(row=row, column=column)

    def open_window(self):
        """Opens a new window for keymap editing"""
        self.editing = True
        self.keymap_frame = Toplevel(self.root, width=400, height=400)
        self.keymap_frame.protocol("WM_DELETE_WINDOW", self.close_window)
        self.add_button('1', 0, 0)
        self.add_button('2', 0, 1)
        self.add_button('3', 0, 2)
        self.add_button('C', 0, 3)

        self.add_button('4', 1, 0)
        self.add_button('5', 1, 1)
        self.add_button('6', 1, 2)
        self.add_button('D', 1, 3)

        self.add_button('7', 2, 0)
        self.add_button('8', 2, 1)
        self.add_button('9', 2, 2)
        self.add_button('E', 2, 3)

        self.add_button('A', 3, 0)
        self.add_button('0', 3, 1)
        self.add_button('B', 3, 2)
        self.add_button('F', 3, 3)


    def save_keymap(self):
        """Save the current keymap layout"""
        return

    def load_keymap(self):
        """Load a saved keymap layout"""
        return

    def close_window(self):
        self.editing = False
        self.keymap_frame.destroy()

    def add_listener(self, hex):
        print(hex)
        print(self.button[hex])
        self.listening = True

    def add_key(self, button, key):
        """Adds a key to the keymap"""
        self.key[button] = key
