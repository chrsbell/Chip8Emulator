import numpy as np
from tkinter import messagebox

class Interpreter:
    def __init__(self, display):
        """Chip-8 interpreter that handles everything"""
        # Interpreter can access 4KB of RAM
        self.memory_buffer = np.array([0] * 0xFFF, np.ubyte)
        # 16 general purpose 8-bit registers
        self.register_v = np.array([0] * 0xF, np.ubyte)
        # 16-bit register for memory addresses
        self.register_i = np.int16(0x0)
        # 8-bit register for delay/sound timers
        self.register_s = np.byte(0)
        # 16-bit program counter register which stores current address
        self.program_counter = np.int16(0x0)
        # 8-bit pointer to top of stack
        self.stack_pointer = np.byte(0)
        # 16 16-bit addresses which represent the call stack
        self.stack = np.array([0x0] * 0xF, np.uint16)
        # Reference to external display
        self.display = display
        # Use a dictionary to look up which function to use for any opcode
        # https://en.wikipedia.org/wiki/CHIP-8
        self.opcode = {}
        self.opcode[self.hash_opcode(0x10, 0x9E)] = self._8XY0
        self.opcode[self.hash_opcode(0x00, 0x00)] = 1
        self.opcode[self.hash_opcode(0x00, 0x00)] = 1


    def load_program_to_memory(self, file):
        """Stores the program in the memory buffer"""
        bin = bytes(file.read())
        program = bin.hex()
        # Each opcode must be 2 bytes long (4 characters)
        if not len(program) % 4 == 0:
            messagebox.showerror("Invalid ROM", "That wasn't a Chip-8 ROM...")
            return

        print(len(program))
        # Store each individual opcode in 2 bytes of RAM starting at 0x200
        for i in range(int(len(program) / 4)):
            opcode = program[i*4:i*4+4]
            # Need to split opcode in half to fit in a byte
            self.memory_buffer[0x200 + i*2] = (int(opcode[:2], 16))
            self.memory_buffer[0x200 + (i*2)+1] = (int(opcode[2:], 16))

    def set_register(self, register, value):
        """Set a register to a value"""

    def execute_instruction(self):
        """Executes the current instruction in the program counter register"""

    def hash_opcode(self, upper_byte, lower_byte):
        """Get an ID for a 2-byte opcode using the first and last 4 bits"""
        upper_byte = upper_byte >> 4 & 0b1111
        lower_byte = lower_byte & 0b1111
        print(bin(upper_byte)[2:].zfill(8))
        print(bin(lower_byte)[2:].zfill(8))
        # Concatenate the bits
        id = upper_byte << 4 | lower_byte
        print(id)
        return 0

    def _8XY0(self, x, y):
        """Sets value of VX to VY"""
        self.register_v[x] = self.register_v[y]