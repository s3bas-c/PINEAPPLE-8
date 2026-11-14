from p8_emulator.p8.alu import ALU
import p8_emulator.p8.config as config
from p8_emulator.p8.memory import Ram, Rom
from p8_emulator.p8.register import Register

class P8_CPU:
    def __init__(self):
        self.rom = Rom.load_from_file("Programs/test.bin")
        self.ram = Ram()

        self.alu = ALU()
        self.register = Register()
    def read(self):
        for cell in self.rom.rom_cells:
            print((cell >> 12))

cpu = P8_CPU()
cpu.read()