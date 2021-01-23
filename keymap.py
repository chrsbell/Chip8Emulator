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

from tkinter import messagebox, Toplevel, Button, PhotoImage
from functools import partial


class Keymap:
    def __init__(self, root):
        """Represents the Chip-8 hexadecimal keypad"""
        self.root = root
        self.keymap_frame = None
        self.width = 300
        self.height = 300
        # Whether keymap editor is open
        self.editing = False
        # Whether we are listening for keyboard input to map
        self.listening = False
        # The target hex value to map (0x0-0xF)
        self.target_key = 0
        # Keyboard input mapped to hex keypad
        self.keyboard = {
                    '0': 0x0,
                    '1': 0x1,
                    '2': 0x2,
                    '3': 0x3,
                    '4': 0x4,
                    '5': 0x5,
                    '6': 0x6,
                    '7': 0x7,
                    '8': 0x8,
                    '9': 0x9,
                    'a': 0xA,
                    'b': 0xB,
                    'c': 0xC,
                    'd': 0xD,
                    'e': 0xE,
                    'f': 0xF}

        # Inverse dictionary for removing old keys mapped to the target hex value
        self.inverse_keyboard = {value: key for key, value in self.keyboard.items()}

        # Current hex key that is down
        self.key = 0
        self.keydown = False

        # Dictionary of tk buttons
        self.button = {}

    def add_button(self, hex_value, row, column):
        self.button[hex_value] = Button(master=self.keymap_frame, text=hex_value,
                                        compound='c', command=partial(self.add_listener, hex_value))
        self.button[hex_value].grid(row=row, column=column)

    def open_window(self):
        """Opens a new window for keymap editing"""
        self.editing = True
        self.keymap_frame = Toplevel(self.root, width=self.width, height=self.height)
        self.keymap_frame.title("Keyboard Settings")
        self.keymap_frame.protocol("WM_DELETE_WINDOW", self.close_window)
        self.keymap_frame.bind('<Key>', self.add_key)
        self.add_button(self.inverse_keyboard[0x1].upper(), 0, 0)
        self.add_button(self.inverse_keyboard[0x2].upper(), 0, 1)
        self.add_button(self.inverse_keyboard[0x3].upper(), 0, 2)
        self.add_button(self.inverse_keyboard[0xC].upper(), 0, 3)

        self.add_button(self.inverse_keyboard[0x4].upper(), 1, 0)
        self.add_button(self.inverse_keyboard[0x5].upper(), 1, 1)
        self.add_button(self.inverse_keyboard[0x6].upper(), 1, 2)
        self.add_button(self.inverse_keyboard[0xD].upper(), 1, 3)

        self.add_button(self.inverse_keyboard[0x7].upper(), 2, 0)
        self.add_button(self.inverse_keyboard[0x8].upper(), 2, 1)
        self.add_button(self.inverse_keyboard[0x9].upper(), 2, 2)
        self.add_button(self.inverse_keyboard[0xE].upper(), 2, 3)

        self.add_button(self.inverse_keyboard[0xA].upper(), 3, 0)
        self.add_button(self.inverse_keyboard[0x0].upper(), 3, 1)
        self.add_button(self.inverse_keyboard[0xB].upper(), 3, 2)
        self.add_button(self.inverse_keyboard[0xF].upper(), 3, 3)


    def save_keymap(self):
        """Save the current keymap layout"""
        return

    def load_keymap(self):
        """Load a saved keymap layout"""
        return

    def close_window(self):
        self.editing = False
        self.listening = False
        self.target_key = 0
        self.keymap_frame.destroy()

    def add_listener(self, hex_value):
        self.target_key = int(hex_value, 16)
        self.listening = True

    def process_keypress(self, event):
        if event.char in self.keyboard:
            print('Hex key down: ', self.keyboard[event.char])
            self.key = self.keyboard[event.char]
            self.keydown = True

    def process_keyrelease(self, event):
        print('Hex key released: ', self.keyboard[event.char])
        self.keydown = False

    def add_key(self, event):
        """Adds a key to the keymap"""
        if self.listening:
            # Remove the old entry
            del self.keyboard[self.inverse_keyboard[self.target_key]]
            # Update both dictionaries
            self.inverse_keyboard[self.target_key] = event.char
            self.keyboard[event.char] = self.target_key
            # Update button text
            self.button[str(hex(self.target_key)[2]).upper()]['text'] = event.char.upper()
            print('Added key mapping: ' + repr(event.char) + ' to ' + hex(self.target_key))
            self.listening = False