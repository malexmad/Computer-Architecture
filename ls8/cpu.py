"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, add):
        """ Accept address to read and return valued stored """
        return self.ram[add]

    def ram_write(self, add, val):
        """ Accept address and value to write """
        self.ram[add] = val

    # def load(self):
    #     """Load a program into memory."""
    #
    #     address = 0
    #
    #     # For now, we've just hardcoded a program:
    #
    #     program = [
    #         # From print8.ls8
    #         0b10000010, # LDI R0,8
    #         0b00000000,
    #         0b00001000,
    #         0b01000111, # PRN R0
    #         0b00000000,
    #         0b00000001, # HLT
    #     ]
    #
    #     for instruction in program:
    #         self.ram[address] = instruction
    #         address += 1

    def load(self):
        address = 0

        try:

            filename = sys.argv[1]
            with open(filename) as f:
                for line in f:

                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    if num == '':
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1

            print("done loading")
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            print(self.reg[reg_a] * self.reg[reg_b])

        else:
            raise Exception("Unsupported ALU operation")

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
        running = True

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        MUL = 0b10100010

        while running:

            inst = self.ram_read(self.pc)

            if inst == LDI:
                # store value in register
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                # print(operand_a, operand_b)
                self.reg[operand_a] = operand_b
                # self.ram_write(operand_a,operand_b)
                self.pc += 3

            elif inst == MUL:
                # print the product of 2 values
                self.alu("MUL", self.ram_read(self.pc+1), self.ram_read(self.pc+2))
                self.pc += 3

            elif inst == PRN:
                # print value in register
                print(self.reg[self.ram_read(self.pc+1)])
                self.pc += 2

            elif inst == HLT:
                # halt CPU and exit
                running = False


# cpu = CPU()
#
# cpu.load()
# cpu.run()
