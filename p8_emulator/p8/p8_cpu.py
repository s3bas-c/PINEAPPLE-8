from .alu import ALU
import p8.config as config
from .memory import Ram, Rom
from .register import Register
from .port import Port
import time

class P8_CPU:
    def __init__(self):
        """Central Processing Unit (CPU) for PINEAPPLE-8 emulator
            
        Attributes:
            rom (object): Preloaded rom used for running programs
            ram (object): Ram unit for quick data storage
            alu (object): ALU unit for arithmetic operations
            registers (list): list of Registers for instant single value data storage
            ports (list): list of Ports for external device use
            pc (object): Program Counter for current storing rom address
            flags (dict): Conditional flags calculated from operations
        """
        
        self.rom = Rom.load_from_file(r"p8_emulator/Programs/program.rom")
        self.ram = Ram()

        self.alu = ALU()
        self.registers = [Register() for _ in range(8)]

        self.ports = [Port() for _ in range(4)]

        self.pc = Register()

        self.flags = {
            "Z": False,
            "C": False,
            "N": False,
            "V": False
        }

    def decode_registers(self, instruction):
        """Extract three registers from rom instructions
        
        Args:
            instruction: raw two-byte instruction from rom

        Returns:
            the three register indexes from the instruction
        """
        
        operand1 = (instruction >> 9) & 0x7
        operand2 = (instruction >> 6) & 0x7
        operand3 = (instruction >> 3) & 0x7

        return operand1, operand2, operand3

    def execute_alu(self, instruction, operation):
        """Execute an ALU operation
                
        Args:
            instruction: raw two-byte instruction from rom
            operation: ALU operation to perform

        Returns:
            None
        """
        regDes, regA, regB = self.decode_registers(instruction)
        
        a = self.registers[regA].read()
        b = self.registers[regB].read()

        self.registers[regDes].write(operation(a, b))

    def compute_instruction(self, addr):
        """Execute an instruction from the rom at a current address
                        
        Args:
            addr: The address to read from rom

        Returns:
            The instruction executed 
        """
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
            return "LDI"
        # MOV
        elif opcode == 2:
            operand1 = (instruction >> 9) & 0x7
            operand2 = (instruction >> 6) & 0x7

            self.registers[operand1].write(self.registers[operand2].read())
            return "MOV"
        # LDR
        elif opcode == 3:
            operand1 = (instruction >> 9) & 0x7
            operand2 = (instruction >> 6) & 0x7 #8 bit for now but depends on 

            self.registers[operand1].write(self.ram.read(self.registers[operand2].read()))
            return "LDR"
        # STR
        elif opcode == 4:
            operand1 = (instruction >> 9) & 0x7
            operand2 = (instruction >> 6) & 0x7 #8 bit for now but depends on 

            self.ram.write(self.registers[operand2].read(), self.registers[operand1].read())
            return "STR"
        # ADD
        elif opcode == 5:
            self.execute_alu(instruction, self.alu.ADD)
            return "ADD"
        # SUB
        elif opcode == 6:
            self.execute_alu(instruction, self.alu.SUB)
            return "SUB"
        # AND
        elif opcode == 7:
            self.execute_alu(instruction, self.alu.AND)
            return "AND"
        # OR
        elif opcode == 8:
            self.execute_alu(instruction, self.alu.OR)
            return "OR"
        # XOR
        elif opcode == 9:
            self.execute_alu(instruction, self.alu.XOR)
            return "XOR"
        # NOT
        elif opcode == 10:
            regDes, regA, regB = self.decode_registers(instruction)
            
            a = self.registers[regA].read()
                        
            self.registers[regDes].write(self.alu.NOT(a))
            return "NOT"
        # JMP
        elif opcode == 11:
            operand1 = (instruction >> 10) & 0x3
            operand2 = (instruction >> 2) & 0xFF # again unknown rom address, 8 bit for now

            if operand1 == 0:
                self.pc.write(operand2)
                return "JMP"  
            elif operand1 == 1:
                if self.flags["Z"] == True:
                    self.pc.write(operand2)
                    return "JMP"
            elif operand1 == 2:
                if self.flags["Z"] == False:
                    self.pc.write(operand2) 
                    return "JMP"  
        # IO
        elif opcode == 12:
            operand1 = (instruction >> 10) & 0x3 # in/out selector
            regA = (instruction >> 7) & 0x7 # again unknown rom address, 8 bit for now
            operand3 = (instruction >> 5) & 0x3 # port selector

            if operand1 == 0: # IN
                self.registers[regA].write(self.ports[operand3].on_read())
            elif operand1 == 1: # OUT
                self.ports[operand3].on_write(self.registers[regA].read())
            return "IO"
        # SHIFT
        elif opcode == 13:
            operand1 = (instruction >> 10) & 0x3 # in/out selector
            regA = (instruction >> 7) & 0x7 # again unknown rom address, 8 bit for now
            regB = (instruction >> 4) & 0x7 # port selector

            if operand1 == 0: # SHL
                self.registers[regA].write(self.registers[regB].read() << 1)
            elif operand1 == 1: # SHR
                self.registers[regA].write(self.registers[regB].read() >> 1)
            return "SHIFT"
        # CMP     
        elif opcode == 14:
            regA, regB, regC = self.decode_registers(instruction)
            
            a = self.registers[regA].read()
            b = self.registers[regB].read()

            self.flags = self.alu.CMP(a, b)
            return "CMP"
        # HLT
        elif opcode == 15:
            return "HLT"

        return "ERROR"

    def read_registers(self):
        """Print all register values
                                
        Args:
            None

        Returns:
            None
        """
        for r, reg in enumerate(self.registers):
            print(f"Register-{r}: {reg.read()}")
        
    def run(self, clock_hz):
        """Execute rom instructions one by one until it reaches a halt
                                
        Args:
            clock_hz: Value to determine CPU clock speed in hertz (hz)

        Returns:
            None
        """
        self.pc.write(0)

        while True:
            time.sleep(1/clock_hz)

            # temporary
            #print(self.pc.read())

            result = self.compute_instruction(self.pc.read())

            if result == "HLT":
                break
            elif result == "JMP":
                continue
            else:
                self.pc.increment()

    
