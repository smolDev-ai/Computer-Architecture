"""CPU functionality."""

# GENERAL OPCODES:
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

# ALU--Math:
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
DEC = 0b01100110
INC = 0b01100101

# ALU--Bitwise:
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101

# Stack
PUSH = 0b01000101
POP = 0b01000110

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # RAM
        self.reg = [0] * 8  # Register
        self.pc = 0  # Program Counter
        self.sp = 7  # Stack Pointer
        self.reg[self.sp] = 0xF4  # register where the stack pointer is 0xF4 is empty


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


    def alu(self, op, reg_a, reg_b=None):
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
            self.reg[reg_a] = ~self.reg[reg_a]
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
            if self.ram_read(self.pc) == ADD:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("ADD", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == SUB:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("SUB", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == MUL:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("MUL", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == DIV:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("DIV", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == MOD:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("MOD", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == INC:
                reg_1 = self.ram[self.pc+1]
                self.alu("INC", reg_1)
                
                self.pc += 2
            if self.ram_read(self.pc) == DEC:
                reg_1 = self.ram[self.pc+1]
                self.alu("DEC", reg_1)
                
                self.pc += 2
            if self.ram_read(self.pc) == NOT:
                reg_1 = self.ram[self.pc+1]
                self.alu("NOT", reg_1)
                
                self.pc += 2
            if self.ram_read(self.pc) == AND:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("AND", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == OR:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("OR", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == XOR:
                reg_1 = self.ram[self.pc+1]
                reg_2 = self.ram[self.pc+2]
                self.alu("XOR", reg_1, reg_2)
                
                self.pc += 3
            if self.ram_read(self.pc) == PRN:
                reg_index = self.ram[self.pc+1]

                print(self.reg[reg_index])

                self.pc += 2
            if self.ram_read(self.pc) == PUSH:
                self.reg[self.sp] -= 1
                stack_address = self.reg[self.sp]
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]
                self.ram_write(value, stack_address)
                self.pc += 2
            if self.ram_read(self.pc) == POP:
                stack_value = self.ram_read(self.reg[self.sp])
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                self.reg[reg_num] = stack_value

                self.reg[self.sp] += 1
                self.pc += 2
           
            if self.ram_read(self.pc) == HLT:
                return False



