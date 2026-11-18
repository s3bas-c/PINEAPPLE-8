from alu import ALU
import config as config
from memory import Ram, Rom
from register import Register
import time

class P8_CPU:
    def __init__(self):
        self.rom = Rom.load_from_file(r"PINEAPPLE-8-main\p8_emulator\Programs\test.bin")
        self.ram = Ram()

        self.alu = ALU()
        self.registers = [Register() for _ in range(8)]

        self.pc = Register()

        self.flags = {
            "Z": False,
            "C": False,
            "N": False,
            "V": False
        }

    def decode_registers(self, instruction):
        operand1 = (instruction >> 9) & 0x7
        operand2 = (instruction >> 6) & 0x7
        operand3 = (instruction >> 3) & 0x7

        return operand1, operand2, operand3

    def execute_alu(self, instruction, operation):
        regDes, regA, regB = self.decode_registers(instruction)
        
        a = self.registers[regA].read()
        b = self.registers[regB].read()

        self.registers[regDes].write(operation(a, b))

    def compute_instruction(self, addr):
        instruction = self.rom.read(addr)

        # Decode the opcode of the instruction

        opcode = (instruction >> 12) & 0xF
        # NOP
        if opcode == 0:
            return "NOP"
        # LDI
        elif opcode == 1:
            operand1 = (instruction >> 9) & 0x7
            operand2 = (instruction >> 1) & 0xFF

            self.registers[operand1].write(operand2)
        # MOV
        elif opcode == 2:
            operand1 = (instruction >> 9) & 0x7
            operand2 = (instruction >> 6) & 0x7

            self.registers[operand1].write(self.registers[operand2].read())
        # ADD
        elif opcode == 5:
            self.execute_alu(instruction, self.alu.ADD)
        # SUB
        elif opcode == 6:
            self.execute_alu(instruction, self.alu.SUB)
        # AND
        elif opcode == 7:
            self.execute_alu(instruction, self.alu.AND)
        # OR
        elif opcode == 8:
            self.execute_alu(instruction, self.alu.OR)
        # XOR
        elif opcode == 9:
            self.execute_alu(instruction, self.alu.XOR)
        # NOT
        elif opcode == 10:
            regDes, regA, regB = self.decode_registers(instruction)
            
            a = self.registers[regA].read()
                        
            self.registers[regDes].write(self.alu.NOT(a))
        # JMP
        elif opcode == 11:
            operand1 = (instruction >> 10) & 0x3
            operand2 = (instruction >> 2) & 0xFF # again unknown rom address, 8 bit for now

            if operand1 == 0:
                self.pc.write(operand2)
            elif operand1 == 1 :
                if self.flags["Z"] == True:
                    self.pc.write(operand2)
            elif operand1 == 2:
                if self.flags["Z"] == False:
                    self.pc.write(operand2)   
        # CMP     
        elif opcode == 14:
            regA, regB, regC = self.decode_registers(instruction)
            
            a = self.registers[regA].read()
            b = self.registers[regB].read()
                        
            self.flags = self.alu.CMP(a, b)
        # HLT
        elif opcode == 15:
            return "HLT"

        return "INS"

    def read_registers(self):
            for r, reg in enumerate(self.registers):
                print(f"Register-{r}: {reg.read()}")
        
    def run(self, clock_hz):
        self.pc.write(0)

        while True:
            time.sleep(1/clock_hz)

            # temporary
            #print(self.pc.read())

            if self.compute_instruction(self.pc.read()) == "HLT":
                break

            self.pc.increment()

    
cpu = P8_CPU()
cpu.run(15)
print(cpu.registers[6].read())

