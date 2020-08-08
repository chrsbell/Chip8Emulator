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
        # Using 'F' as a placeholder for N, X, and Y
        self.opcode[self.hash_opcode(0x00, 0x00)] = 1
        self.opcode[self.hash_opcode(0x00, 0xE0)] = 1
        self.opcode[self.hash_opcode(0x00, 0xEE)] = 1
        self.opcode[self.hash_opcode(0x1F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x2F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x3F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x4F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x5F, 0xF0)] = 1
        self.opcode[self.hash_opcode(0x6F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x7F, 0xFF)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF0)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF1)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF2)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF3)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF4)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF5)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF6)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xF7)] = 1
        self.opcode[self.hash_opcode(0x8F, 0xFE)] = 1
        self.opcode[self.hash_opcode(0x9F, 0xF0)] = 1
        self.opcode[self.hash_opcode(0xAF, 0xFF)] = 1
        self.opcode[self.hash_opcode(0xBF, 0xFF)] = 1
        self.opcode[self.hash_opcode(0xCF, 0xFF)] = 1
        self.opcode[self.hash_opcode(0xDF, 0xFF)] = 1
        self.opcode[self.hash_opcode(0xEF, 0x9E)] = 1
        self.opcode[self.hash_opcode(0xEF, 0xA1)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x07)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x0A)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x15)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x18)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x1E)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x29)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x33)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x55)] = 1
        self.opcode[self.hash_opcode(0xFF, 0x65)] = 1

        print(len(self.opcode))


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
        upper_bits = upper_byte >> 4 & 0b1111
        lower_bits = lower_byte & 0b1111
        # print(bin(upper_byte)[2:].zfill(8))
        # print(bin(lower_byte)[2:].zfill(8))
        # Concatenate the bits
        hash_value = upper_bits << 4 | lower_bits
        if hash_value in self.opcode:
            # Need to encode using entire lower byte
            hash_value = upper_bits << 8 | lower_byte
            #print("Collision at " + hex(upper_byte) + hex(lower_byte)[2:] + " " + str(hash_value))
        return hash_value

    def _8XY0(self, x, y, n, addr, kk):
        """Sets value of VX to VY"""
        self.register_v[x] = self.register_v[y]