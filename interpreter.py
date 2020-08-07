from renderer import Renderer
import numpy as np


class Interpreter:
    def __init__(self):
        """Chip-8 interpreter that handles everything"""
        # Interpreter can access 4KB of RAM
        self.memory_buffer = np.array([0] * 0xFFF, np.byte)
        # 16 general purpose 8-bit registers
        self.register_v = np.array([0] * 0xF, np.byte)
        # 16-bit register for memory addresses
        self.register_i = np.int16(0x0)
        # 8-bit register for delay/sound timers
        self.register_s = np.byte(0)
        # 16-bit program counter register which stores current address
        self.program_counter = np.int16(0x0)
        # 8-bit pointer to top of stack
        self.stack_pointer = np.byte(0)
        # 16 16-bit addresses which represent the call stack
        self.stack = np.array([0x0] * 0xF, np.int16)
        # Reference to external display
        self.display = 0

    def set_display(self, display):
        """Set a reference to the external display"""
        self.display = display

    def load_program_to_memory(self, file):
        """Stores the program in the memory buffer"""
        return

    def set_register(self, register, value):
        """Set a register to a value"""

    def execute_instruction(self):
        """Executes the current instruction in the program counter register"""
