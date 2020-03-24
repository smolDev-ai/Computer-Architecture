import sys
"""CPU functionality."""

# GENERAL OPCODES:
LDI = 0b10000010
PRN = 0b01000111
PRA = 0b01001000
HLT = 0b00000001
ST = 0b10000100
LD = 0b10000011

# ALU--Math:
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
DEC = 0b01100110
INC = 0b01100101

# ALU--Comparison
CMP = 0b10100111

# ALU--Bitwise:
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101

# Stack:
PUSH = 0b01000101
POP = 0b01000110

# Call related:
CALL = 0b01010000
RET = 0b00010001

# Jump related:
JEQ = 0b01010101
JGE = 0b01011010
JGT = 0b01010111
JLE = 0b01011001
JLT = 0b01011000
JMP = 0b01010100
JNE = 0b01010110

# Interrupt
INT = 0b01010010
IRET = 0b00010011

# Do Nothing:
NOP = 0b00000000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # RAM
        self.reg = [0] * 8  # Register
        self.fl = {}  # flags
        self.pc = 0  # Program Counter
        self.sp = 7  # Stack Pointer
        self.reg[self.sp] = 0xF4  # register where the stack pointer is 0xF4 is empty
        self.opcodes = {
            LDI: lambda register, value: self.handle_LDI(register, value),
            PRN: lambda value, _: print(self.reg[value]),
            PRA: lambda value, _: print(chr(self.reg[value])),
            ST: lambda reg_a, reg_b: self.handle_ST(reg_a, reg_b),
            LD: lambda reg_a, reg_b: self.handle_LD(reg_a, reg_b),
            ADD: lambda reg_a, reg_b: self.alu("ADD", reg_a, reg_b),
            SUB: lambda reg_a, reg_b: self.alu("SUB", reg_a, reg_b),
            MUL: lambda reg_a, reg_b: self.alu("MUL", reg_a, reg_b),
            DIV: lambda reg_a, reg_b: self.alu("DIV", reg_a, reg_b),
            MOD: lambda reg_a, reg_b: self.alu("MOD", reg_a, reg_b),
            DEC: lambda num: self.alu("DEC", num),
            INC: lambda num: self.alu("INC", num),
            AND: lambda reg_a, reg_b: self.alu("AND", reg_a, reg_b),
            OR: lambda reg_a, reg_b: self.alu("OR", reg_a, reg_b),
            XOR: lambda reg_a, reg_b: self.alu("XOR", reg_a, reg_b),
            NOT: lambda num: self.alu("NOT", num),
            SHL: lambda reg_a, reg_b: self.alu("SHL", reg_a, reg_b),
            SHR: lambda reg_a, reg_b: self.alu("SHR", reg_a, reg_b),
            CMP: lambda reg_a, reg_b: self.alu("CMP", reg_a, reg_b),
            PUSH: lambda opa, _: self.handle_push(opa),
            POP: lambda opa, _: self.handle_pop(opa),
            CALL: lambda opa, _: self.handle_call(opa),
            RET: lambda *_args: self.handle_ret(),
            JMP: lambda opa, _: self.handle_jmp(opa),
            JEQ: lambda reg_a, _: self.handle_comparison("JEQ", reg_a),
            JGE: lambda reg_a, _: self.handle_comparison("JGE", reg_a),
            JGT: lambda reg_a, _: self.handle_comparison("JGT", reg_a),
            JLE: lambda reg_a, _: self.handle_comparison("JLE", reg_a),
            JLT: lambda reg_a, _: self.handle_comparison("JLT", reg_a),
            JNE: lambda reg_a, _: self.handle_comparison("JNE", reg_a),

        }

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

        def add(reg_a, reg_b):
            self.reg[reg_a] += self.reg[reg_b]
        
        def sub(reg_a, reg_b):
            self.reg[reg_a] -= self.reg[reg_b]
        
        def mul(reg_a, reg_b):
            self.reg[reg_a] *= self.reg[reg_b]

        def div(reg_a, reg_b):
            self.reg[reg_a] /= self.reg[reg_b]

        def mod(reg_a, reg_b):
            self.reg[reg_a] %= self.reg[reg_b]

        def ir_and(reg_a, reg_b):
            self.reg[reg_a] &= self.reg[reg_b]

        def ir_or(reg_a, reg_b):
            self.reg[reg_a] |= self.reg[reg_b]

        def ir_not(reg_a):
            self.reg[reg_a] = ~self.reg[reg_a]

        def xor(reg_a, reg_b):
            self.reg[reg_a] ^= self.reg[reg_b]

        def shl(reg_a, reg_b):
            self.reg[reg_a] <<= self.reg[reg_b]

        def shr(reg_a, reg_b):
            self.reg[reg_a] >>= self.reg[reg_b]

        def inc(reg_a):
            self.reg[reg_a] += 1

        def dec(reg_a):
            self.reg[reg_a] -= 1

        alu_math = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "DIV": div,
            "MOD": mod,
            "INC": inc,
            "DEC": dec
        }

        alu_bitwise = {
            "AND": ir_and,
            "OR": ir_or,
            "NOT": ir_not,
            "XOR": xor,
            "SHL": shl,
            "SHR": shr
        }

        if op in alu_math:
            alu_math[op](reg_a, reg_b)
        elif op in alu_bitwise:
            alu_bitwise[op](reg_a, reg_b)
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl['E'] = 1
            else:
                self.fl['E'] = 0
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl['L'] = 1
            else:
                self.fl['L'] = 0
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl['G'] = 1
            else:
                self.fl['G'] = 0
            
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
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def handle_LDI(self, register, value):
        self.reg[register] = value

    def handle_LD(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.reg[reg_b])

    def handle_ST(self, reg_a, reg_b):
        self.ram_write(self.reg[reg_b], self.reg[reg_a])

    def handle_push(self, opa):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[opa], self.reg[self.sp])

    def handle_pop(self, opa):
        self.reg[opa] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def handle_call(self, address):
        self.reg[self.sp] -= 1
        self.ram_write(self.pc + 2, self.reg[self.sp])
        self.pc = self.reg[address]

    def handle_ret(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def handle_jmp(self, address):
        self.pc = self.reg[address]

    def handle_comparison(self, op, reg_a):
        def equal(a):
            if self.fl['E'] == 1:
                self.pc = self.reg[a]
            else:
                self.pc += 2

        def greater(a):
            if self.fl['G'] == 1:
                self.pc = self.reg[a]
            else:
                self.pc += 2

        def less(a):
            if self.fl['L'] == 1:
                self.pc = self.reg[a]
            else:
                self.pc += 2
        
        def not_equal(a):
            if self.fl['E'] == 0:
                self.pc = self.reg[a]
            else:
                self.pc += 2

       # Create functions for each check
        comparison_ops = {
            "JEQ": equal,
            "JGE": equal,
            "JGT": greater,
            "JLE": equal,
            "JLT": less,
            "JNE": not_equal
        }

        if op in comparison_ops:
            comparison_ops[op](reg_a)


    def run(self):
        """Run the CPU."""
        while True:
            IR = self.ram_read(self.pc)
            OPA = self.ram_read(self.pc + 1)
            OPB = self.ram_read(self.pc + 2)

            if IR == HLT:
                return False

            if IR == NOP:
                continue

            if IR in self.opcodes:
                self.opcodes[IR](OPA, OPB)
                operands = IR >> 6
                set_pc = (IR & 0b10000) >> 4

                if not set_pc:
                    self.pc += operands + 1



