import numpy as np
from tkinter import messagebox
import random


# noinspection PyPep8Naming
class Interpreter:
    def __init__(self, display, keyboard):
        """Chip-8 interpreter"""

        # Interpreter can access 4KB of RAM
        self.memory_buffer = np.array([0] * 4096, np.ubyte)
        # 16 general purpose 8-bit registers
        self.register_v = np.array([0] * 16, np.ubyte)
        # 16-bit register for memory addresses
        self.register_i = np.int16(0)
        # 8-bit registers for delay/sound timers
        self.register_d = np.ubyte(0)
        self.register_s = np.ubyte(0)
        # 16-bit program counter register which stores current address
        self.program_counter = 0x200
        # 8-bit pointer to top of stack
        self.stack_pointer = np.ubyte(0)
        # 16 16-bit addresses which represent the call stack
        self.stack = np.array([0] * 16, np.uint16)
        # Reference to external display
        self.display = display
        # Reference to keymap
        self.keyboard = keyboard

        # Used for Fx0A
        self.wait_for_key = False
        self.x = 0

        # Error handling
        self.error = False

        # Debug mode
        self.debug = True

        # Using a dictionary to look up which function to use for any opcode
        # https://en.wikipedia.org/wiki/CHIP-8
        # Most of the descriptions are taken directly from http://devernay.free.fr/hacks/chip8/C8TECH10.HTM#3.1
        # Using 'F' as a placeholder for N, X, and Y
        self.opcode = {}

        self.initialized_hash = False

        self.opcode[self.hash_opcode(0x00, 0x00)] = self._0NNN
        self.opcode[self.hash_opcode(0x00, 0xE0)] = self._00E0
        self.opcode[self.hash_opcode(0x00, 0xEE)] = self._00EE
        self.opcode[self.hash_opcode(0x1F, 0xFF)] = self._1nnn
        self.opcode[self.hash_opcode(0x2F, 0xFF)] = self._2nnn
        self.opcode[self.hash_opcode(0x3F, 0xFF)] = self._3xkk
        self.opcode[self.hash_opcode(0x4F, 0xFF)] = self._4xkk
        self.opcode[self.hash_opcode(0x5F, 0xF0)] = self._5xy0
        self.opcode[self.hash_opcode(0x6F, 0xFF)] = self._6xkk
        self.opcode[self.hash_opcode(0x7F, 0xFF)] = self._7xkk
        self.opcode[self.hash_opcode(0x8F, 0xF0)] = self._8xy0
        self.opcode[self.hash_opcode(0x8F, 0xF1)] = self._8xy1
        self.opcode[self.hash_opcode(0x8F, 0xF2)] = self._8xy2
        self.opcode[self.hash_opcode(0x8F, 0xF3)] = self._8xy3
        self.opcode[self.hash_opcode(0x8F, 0xF4)] = self._8xy4
        self.opcode[self.hash_opcode(0x8F, 0xF5)] = self._8xy5
        self.opcode[self.hash_opcode(0x8F, 0xF6)] = self._8xy6
        self.opcode[self.hash_opcode(0x8F, 0xF7)] = self._8xy7
        self.opcode[self.hash_opcode(0x8F, 0xFE)] = self._8xyE
        self.opcode[self.hash_opcode(0x9F, 0xF0)] = self._9xy0
        self.opcode[self.hash_opcode(0xAF, 0xFF)] = self._Annn
        self.opcode[self.hash_opcode(0xBF, 0xFF)] = self._Bnnn
        self.opcode[self.hash_opcode(0xCF, 0xFF)] = self._Cxkk
        self.opcode[self.hash_opcode(0xDF, 0xFF)] = self._Dxyn
        self.opcode[self.hash_opcode(0xEF, 0x9E)] = self._Ex9E
        self.opcode[self.hash_opcode(0xEF, 0xA1)] = self._ExA1
        self.opcode[self.hash_opcode(0xFF, 0x07)] = self._Fx07
        self.opcode[self.hash_opcode(0xFF, 0x0A)] = self._Fx0A
        self.opcode[self.hash_opcode(0xFF, 0x15)] = self._Fx15
        self.opcode[self.hash_opcode(0xFF, 0x18)] = self._Fx18
        self.opcode[self.hash_opcode(0xFF, 0x1E)] = self._Fx1E
        self.opcode[self.hash_opcode(0xFF, 0x29)] = self._Fx29
        self.opcode[self.hash_opcode(0xFF, 0x33)] = self._Fx33
        self.opcode[self.hash_opcode(0xFF, 0x55)] = self._Fx55
        self.opcode[self.hash_opcode(0xFF, 0x65)] = self._Fx65

        self.initialized_hash = True

        # Hex Sprites

        # "0"
        self.sprites = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
                        0x20, 0x60, 0x20, 0x20, 0x70,  # 1
                        0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
                        0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
                        0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
                        0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
                        0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
                        0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
                        0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
                        0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
                        0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
                        0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
                        0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
                        0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
                        0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
                        0xF0, 0x80, 0xF0, 0x80, 0x80   # F
                        ]

        for i in range(len(self.sprites)):
            self.memory_buffer[i] = self.sprites[i]

        if self.debug:
            assert(len(self.opcode) == 35)

    def load_program_to_memory(self, file):
        """Stores the program in the memory buffer"""
        file_bin = bytes(file.read())
        program = file_bin.hex()
        self.__init__(self.display, self.keyboard)
        self.display.clear_screen()
        # Make sure program isn't too large
        if int(len(program) / 2 > (4096 - 0x200)):
            messagebox.showerror("ROM Error", "ROM size is too large!")
            self.error = True
            return
        # Store each individual opcode in 2 bytes of RAM starting at 0x200
        for i in range(int(len(program) / 4)):
            opcode = program[i*4:i*4+4]
            # Need to split opcode in half to fit in a byte
            self.memory_buffer[self.program_counter + i*2] = (int(opcode[:2], 16))
            self.memory_buffer[self.program_counter + (i*2)+1] = (int(opcode[2:], 16))
        # Successfully loaded ROM
        self.error = False

    def execute_instruction(self):
        """Executes the current instruction in the program counter register"""
        # Update the timer registers at ~60hz
        if self.register_d > 0:
            self.register_d -= int(self.display.max_fps / 60)
            if self.register_d < 0:
                self.register_d = 0
        if self.register_s > 0:
            self.register_s -= int(self.display.max_fps / 60)
            if self.register_s < 0:
                self.register_s = 0
        upper_byte = self.memory_buffer[self.program_counter]
        lower_byte = self.memory_buffer[self.program_counter + 1]
        x = upper_byte & 0b1111
        y = lower_byte >> 4 & 0b1111
        n = lower_byte & 0b1111
        address = x << 8 | lower_byte
        if self.debug:
            print("Current Opcode: ")
        hash_value = self.hash_opcode(upper_byte, lower_byte)
        if hash_value not in self.opcode:
            messagebox.showerror("ROM Error", "Couldn't read ROM...")
            self.error = True
            return
        self.opcode[hash_value](x, y, n, address, lower_byte)

    def hash_opcode(self, upper_byte, lower_byte):
        """Gets an ID for a 2-byte opcode using the first and last 4-8 bits"""
        upper_bits = upper_byte >> 4 & 0b1111
        lower_bits = lower_byte & 0b1111

        if upper_bits == 0xF or upper_bits == 0xE:
            # Encode opcodes beginning with F or E
            hash_value = upper_bits << 8 | lower_byte
        elif upper_bits == 0x0:
            hash_value = lower_byte
            if self.initialized_hash and hash_value not in self.opcode:
                # 'Call' opcode
                hash_value = 0x00
        elif upper_bits == 0x08:
            hash_value = upper_bits << 8 | lower_bits
        else:
            hash_value = upper_bits

        if self.debug:
            print(hex(upper_byte) + hex(lower_byte)[2:] + ": " + str(hash_value))

        return hash_value

    def _0NNN(self, x, y, n, address, byte):
        """Jump to a machine code routine at nnn. This instruction is only used on the old computers on which Chip-8
        was originally implemented. It is ignored by modern interpreters. """
        self.program_counter += 2

    def _00E0(self, x, y, n, address, byte):
        """Clear the display."""
        self.display.clear_screen()
        self.program_counter += 2

    def _00EE(self, x, y, n, address, byte):
        """Return from a subroutine. The interpreter sets the program counter to the address at the top of the stack,
        then subtracts 1 from the stack pointer. """
        self.stack_pointer -= 1
        self.program_counter = self.stack[self.stack_pointer] + 2

    def _1nnn(self, x, y, n, address, byte):
        """Jump to location at address. The interpreter sets the program counter to address."""
        self.program_counter = address

    def _2nnn(self, x, y, n, address, byte):
        """Call subroutine at nnn. The interpreter increments the stack pointer, then puts the current PC on the top
        of the stack. The PC is then set to nnn. """
        self.stack[self.stack_pointer] = self.program_counter
        self.stack_pointer += 1
        self.program_counter = address
        # self.execute_instruction()

    def _3xkk(self, x, y, n, address, byte):
        """Skip next instruction if Vx = byte. The interpreter compares register Vx to byte, and if they are equal,
        increments the program counter by 2. """
        if self.register_v[x] == byte:
            self.program_counter += 4
        else:
            self.program_counter += 2

    def _4xkk(self, x, y, n, address, byte):
        """Skip next instruction if Vx != kk. The interpreter compares register Vx to kk, and if they are not equal,
        increments the program counter by 2. """
        if self.register_v[x] != byte:
            self.program_counter += 4
        else:
            self.program_counter += 2

    def _5xy0(self, x, y, n, address, byte):
        """Skip next instruction if Vx = Vy. The interpreter compares register Vx to register Vy, and if they are
        equal, increments the program counter by 2. """
        if self.register_v[x] == self.register_v[y]:
            self.program_counter += 4
        else:
            self.program_counter += 2

    def _6xkk(self, x, y, n, address, byte):
        """Set Vx = kk. The interpreter puts the value kk into register Vx."""
        self.register_v[x] = byte
        self.program_counter += 2

    def _7xkk(self, x, y, n, address, byte):
        """Set Vx = Vx + kk. Adds the value kk to the value of register Vx, then stores the result in Vx."""
        self.register_v[x] += byte
        self.program_counter += 2

    def _8xy0(self, x, y, n, address, byte):
        """Set Vx = Vy. Stores the value of register Vy in register Vx."""
        self.register_v[x] = self.register_v[y]
        self.program_counter += 2

    def _8xy1(self, x, y, n, address, byte):
        """Set Vx = Vx OR Vy. Performs a bitwise OR on the values of Vx and Vy, then stores the result in Vx."""
        self.register_v[x] |= self.register_v[y]
        self.program_counter += 2

    def _8xy2(self, x, y, n, address, byte):
        """Set Vx = Vx AND Vy. Performs a bitwise AND on the values of Vx and Vy, then stores the result in Vx."""
        self.register_v[x] &= self.register_v[y]
        self.program_counter += 2

    def _8xy3(self, x, y, n, address, byte):
        """Set Vx = Vx XOR Vy. Performs a bitwise exclusive OR on the values of Vx and Vy, then stores the result in
        Vx. """
        self.register_v[x] = self.register_v[x] ^ self.register_v[y]
        self.program_counter += 2

    def _8xy4(self, x, y, n, address, byte):
        """Set Vx = Vx + Vy, set VF = carry. The values of Vx and Vy are added together. If the result is greater
        than 8 bits (i.e., > 255,) VF is set to 1, otherwise 0. Only the lowest 8 bits of the result are kept,
        and stored in Vx. """
        temp = self.register_v[x]
        self.register_v[x] += self.register_v[y]
        if temp > self.register_v[x]:
            # There was an overflow, which is OK
            self.register_v[0xF] = 0x01
        else:
            self.register_v[0xF] = 0x00
        self.program_counter += 2

    def _8xy5(self, x, y, n, address, byte):
        """Set Vx = Vx - Vy, set VF = NOT borrow. If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted
        from Vx, and the results stored in Vx. """
        if self.register_v[x] > self.register_v[y]:
            self.register_v[0xF] = 0x01
        else:
            self.register_v[0xF] = 0x00
        self.register_v[x] -= self.register_v[y]
        self.program_counter += 2

    def _8xy6(self, x, y, n, address, byte):
        """Set Vx = Vx SHR 1. If the least-significant bit of Vx is 1, then VF is set to 1, otherwise 0. Then Vx is
        divided by 2. """
        if self.register_v[x] & 0b1:
            self.register_v[0xF] = 0x01
        else:
            self.register_v[0xF] = 0x00
        self.register_v[x] /= 2
        self.program_counter += 2

    def _8xy7(self, x, y, n, address, byte):
        """Set Vx = Vy - Vx, set VF = NOT borrow. If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted
        from Vy, and the results stored in Vx. """
        if self.register_v[y] > self.register_v[x]:
            self.register_v[0xF] = 0x01
        else:
            self.register_v[0xF] = 0x00
        self.register_v[x] = self.register_v[y] - self.register_v[x]
        self.program_counter += 2

    def _8xyE(self, x, y, n, address, byte):
        """Set Vx = Vx SHL 1. If the most-significant bit of Vx is 1, then VF is set to 1, otherwise to 0. Then Vx is
        multiplied by 2. """
        # Using string binary representation to check
        bin_string = bin(self.register_v[x])
        if len(bin_string) == 10 and int(bin_string[2]) == 1:
            self.register_v[0xF] = 0x01
        else:
            self.register_v[0xF] = 0x00
        self.register_v[x] *= 2
        self.program_counter += 2

    def _9xy0(self, x, y, n, address, byte):
        """Skip next instruction if Vx != Vy. The values of Vx and Vy are compared, and if they are not equal,
        the program counter is increased by 2. """
        if self.register_v[x] != self.register_v[y]:
            self.program_counter += 4
        else:
            self.program_counter += 2

    def _Annn(self, x, y, n, address, byte):
        """Set I = address"""
        self.register_i = address
        self.program_counter += 2

    def _Bnnn(self, x, y, n, address, byte):
        """Jump to location nnn + V0. The program counter is set to nnn plus the value of V0."""
        self.program_counter = address + self.register_v[0x00]

    def _Cxkk(self, x, y, n, address, byte):
        """Set Vx = random byte AND kk. The interpreter generates a random number from 0 to 255, which is then ANDed
        with the value kk. The results are stored in Vx. """
        random_byte = random.randint(0, 255)
        self.register_v[x] = random_byte & byte
        self.program_counter += 2

    def _Dxyn(self, x, y, n, address, byte):
        """Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision. The interpreter reads
        n bytes from memory, starting at the address stored in I. These bytes are then displayed as sprites on screen
        at coordinates (Vx, Vy). Sprites are XORed onto the existing screen. If this causes any pixels to be erased,
        VF is set to 1, otherwise it is set to 0. If the sprite is positioned so part of it is outside the
        coordinates of the display, it wraps around to the opposite side of the screen. """
        for j in range(n):
            # Add padding to fit 8 bits
            sprite = format(self.memory_buffer[self.register_i + j], '#010b')[2:]
            for i in range(8):
                vx = (self.register_v[x] + i) % self.display.width
                vy = self.display.height - ((self.register_v[y] + j) % self.display.height) - 1
                pixel_state = self.display.get_pixel(vx, vy)
                if pixel_state and int(sprite[i]):
                    # There was a collision
                    self.register_v[0xF] = 1
                self.display.set_pixel(vx, vy, int(sprite[i]) ^ pixel_state)
        self.program_counter += 2

    def _Ex9E(self, x, y, n, address, byte):
        """Skip next instruction if key with the value of Vx is pressed. Checks the keyboard, and if the key
        corresponding to the value of Vx is currently in the down position, PC is increased by 2. """
        if self.keyboard.keydown and self.keyboard.key == self.register_v[x]:
            self.program_counter += 4
        else:
            self.program_counter += 2
        return

    def _ExA1(self, x, y, n, address, byte):
        """Skip next instruction if key with the value of Vx is not pressed. Checks the keyboard, and if the key
        corresponding to the value of Vx is currently in the up position, PC is increased by 2. """
        # Check if key pressed doesn't match or there is no key pressed
        if (self.keyboard.keydown and self.keyboard.key != self.register_v[x]) or not self.keyboard.keydown:
            self.program_counter += 4
        else:
            self.program_counter += 2
        return

    def _Fx07(self, x, y, n, address, byte):
        """Set Vx = delay timer value. The value of DT is placed into Vx."""
        self.register_v[x] = self.register_d
        self.program_counter += 2

    def _Fx0A(self, x, y, n, address, byte):
        """Wait for a key press, store the value of the key in Vx. All execution stops until a key is pressed,
        then the value of that key is stored in Vx. """
        self.wait_for_key = True
        self.x = x
        return

    def _Fx15(self, x, y, n, address, byte):
        """Set delay timer = Vx. DT is set equal to the value of Vx."""
        self.register_d = self.register_v[x]
        self.program_counter += 2
        return

    def _Fx18(self, x, y, n, address, byte):
        """Set sound timer = Vx. ST is set equal to the value of Vx."""
        self.register_s = self.register_v[x]
        self.program_counter += 2
        return

    def _Fx1E(self, x, y, n, address, byte):
        """Set I = I + Vx. The values of I and Vx are added, and the results are stored in I."""
        self.register_i += self.register_v[x]
        self.program_counter += 2

    def _Fx29(self, x, y, n, address, byte):
        """Set I = location of sprite for digit Vx. The value of I is set to the location for the hexadecimal sprite
        corresponding to the value of Vx. """
        self.register_i = (x*5)
        self.program_counter += 2

    def _Fx33(self, x, y, n, address, byte):
        """Store BCD representation of Vx in memory locations I, I+1, and I+2. The interpreter takes the decimal
        value of Vx, and places the hundreds digit in memory at location in I, the tens digit at location I+1,
        and the ones digit at location I+2. """
        decimal = self.register_v[x]
        self.memory_buffer[self.register_i] = int(decimal / 100)
        self.memory_buffer[self.register_i + 1] = int((decimal % 100) / 10)
        self.memory_buffer[self.register_i + 2] = decimal % 10
        self.program_counter += 2

    def _Fx55(self, x, y, n, address, byte):
        """Store registers V0 through Vx in memory starting at location I. The interpreter copies the values of
        registers V0 through Vx into memory, starting at the address in I. """
        for i in range(x + 1):
            self.memory_buffer[self.register_i + i] = self.register_v[i]
        self.program_counter += 2

    def _Fx65(self, x, y, n, address, byte):
        """The interpreter reads values from memory starting at location I into registers V0 through Vx. """
        for i in range(x + 1):
            self.register_v[i] = self.memory_buffer[self.register_i + i]
        self.program_counter += 2
