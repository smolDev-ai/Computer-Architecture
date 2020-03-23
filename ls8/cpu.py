"""CPU functionality."""

# OPCODES:
LDI = 0b10000010
MUL = 0b10100010
PRN = 0b01000111
HLT = 0b00000001

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # RAM
        self.reg = [0] * 8  # Register
        self.pc = 0  # Program Counter

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as program:
            for line in program:
                # strip new lines and split at the # symbol
                clean_up = line.strip().split('#')
                # grab the number
                value = clean_up[0].strip()

                if value != "":
                    # convert to binary
                    num = int(value, 2)
                    self.ram[address] = num
                    address += 1
                else:
                    continue


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        if op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        if op == "MOD":
            self.reg[reg_a] %= self.reg[reg_b]
        if op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        if op == "NOT":
            ~self.reg[reg_a]
        if op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        if op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        if op == "SHL":
            self.reg[reg_a] <<= self.reg[reg_b]
        if op == "SHR":
            self.reg[reg_a] >>= self.reg[reg_b]
        if op == "INC":
            self.reg[reg_a] += 1
        if op == "DEC":
            self.reg[reg_a] -= 1


        else:
            raise Exception("Unsupported ALU operation")
    
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        # MDR -- Value
        # MAR -- Address to write the value to.
        self.ram[MAR] = MDR


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            if self.ram_read(self.pc) == LDI:
                reg_index = self.ram[self.pc+1]
                value = self.ram[self.pc+2]

                self.reg[reg_index] = value

                self.pc += 3
            if self.ram_read(self.pc) == MUL:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("MUL", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == PRN:
                reg_index = self.ram[self.pc+1]

                print(self.reg[reg_index])

                self.pc += 2
            if self.ram_read(self.pc) == HLT:
                return False



