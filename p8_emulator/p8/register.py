import p8_emulator.p8.config as config

'''
DESC. - The register class is used to simulate general purpose registers
    in a cpu.
VARIABLES - the bit_mask is used to determine the largest number possible
    depending on the cpu's BIT_DEPTH (you can change BIT_DEPTH in config.py)


EX. BIT_DEPTH of 8 allows values from 0 to 255,
    represented using 8 binary digits.


FUNCTIONS - Functions in the registers class consists of reading the current
    value, using read(), and writing a new value using write().
'''

class Register:
    def __init__(self):
        self.value = 0
        self.bit_mask = (1 << config.REGISTER_BIT_WIDTH) - 1

    def read(self):
        return self.value

    def write(self, value):
        self.value = value & self.bit_mask

    def increment(self):
        self.value += 1
        self.value = self.value & self.bit_mask

    def decrement(self):
        self.value -= 1
        self.value = self.value & self.bit_mask

    def clear(self):
        self.value = 0