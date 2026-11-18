class P8_Assembler:
    def __init__(self):
        self.p8_opcodes = {
            "NOP": ["TYPE0", 0],
            "LDI": ["TYPE1", 1],
            "MOV": ["TYPE2", 2],
            "LDR": ["TYPE1", 3],
            "STR": ["TYPE1", 4],
            "ADD": ["TYPE3", 5],
            "SUB": ["TYPE3", 6],
            "AND": ["TYPE3", 7],
            "OR": ["TYPE3", 8],
            "XOR": ["TYPE3", 9],
            "NOT": ["TYPE2", 10],
            "JMP": ["TYPE4", 11],
            "IO": 12,
            "SHFT": 13,
            "CMP": ["TYPE2", 14],
            "HLT": ["TYPE0", 15]    
        }

        self.p8_registers = {
            "reg0": 0,
            "reg1": 1,
            "reg2": 2,
            "reg3": 3,
            "reg4": 4,
            "reg5": 5,
            "reg6": 6,
            "reg7": 7      
        }

        self.p8_extras = {
            "DIR": 0,
            "JZ": 1,
            "JNZ": 2
        }

    def print_bin_program(self, lines):
        for i in range(0, len(lines), 2):
            chunk = lines[i:i+2]
            print(" ".join(f"{b:08b}" for b in chunk))
    
    def encode(self, asm_file, des_file):
        with open(asm_file,"r") as f:
            lines = f.readlines()

            binary_lines = bytearray()

            for line in lines:
                line = line.strip().split()

                encoded_line = 0xFFFF
                
                if len(line) == 0 or line[0] == "#": 
                    encoded_line = 0 & 0xFFFF
                    binary_lines.extend(encoded_line.to_bytes(2, byteorder="big"))
                    continue

                instruction = self.p8_opcodes[line[0]]

                if instruction[0] == "TYPE0":
                    opcode = instruction[1]

                    encoded_line = (opcode << 12)

                elif instruction[0] == "TYPE1":
                    opcode = instruction[1]

                    des_reg = self.p8_registers[line[1]]

                    value = int(line[2]) # value is 8 bit
                    value = value & 0xFF

                    encoded_line = (opcode << 12) | (des_reg << 9)| (value << 1)

                elif instruction[0] == "TYPE2":
                    opcode = instruction[1]

                    reg_a = self.p8_registers[line[1]]

                    reg_b = self.p8_registers[line[2]]

                    encoded_line = (opcode << 12) | (reg_a << 9) | (reg_b << 6)
                    
                elif instruction[0] == "TYPE3":
                    opcode = instruction[1]

                    des_reg = self.p8_registers[line[1]]

                    reg_a = self.p8_registers[line[2]]
                    reg_b = self.p8_registers[line[3]]

                    encoded_line = (opcode << 12) | (des_reg << 9) | (reg_a << 6) | (reg_b << 3)

                elif instruction[0] == "TYPE4":
                    opcode = instruction[1]

                    operand1 = self.p8_extras[line[1]] # 2 bits

                    value = value & 0xFF

                    value = int(line[2]) - 1 # value unknown yet, but 8 bit for now, must chnage when decide rom address size
                    value = value & 0xFF

                    encoded_line = (opcode << 12) | (operand1 << 10) |(value << 2)

                encoded_line = encoded_line & 0xFFFF 
                binary_lines.extend(encoded_line.to_bytes(2, byteorder="big"))

            with open(des_file, "wb") as f:
                f.write(binary_lines)
                self.print_bin_program(binary_lines)


asm = P8_Assembler()
asm.encode(r"PINEAPPLE-8-main\p8_emulator\Assembly\assemble.pasm", r"PINEAPPLE-8-main\p8_emulator\Programs\test.bin")

                
        

        