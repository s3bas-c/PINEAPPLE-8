import config as config

'''
DESC. the ALU holds all of the math in the computer, we call
    the ALU directly from our ROM.


VARIABLES. the bit_mask is used to determine the largest number possible
    depending on the cpu's BIT_DEPTH (you can change BIT_DEPTH in config.py)


FUNCTIONS:
    - ADD, returns the addition 2 values directly
    - SUB, returns the difference of 2 values directly
    - AND, returns the bitwise AND of 2 values directly
    - OR, returns the bitwise OR of 2 values directly
    - XOR, returns the bitwise XOR of 2 values directly
    - NOT, returns the bitwise NOT of a value
    - CMP, compares 2 values and updates flags, the boolean flag updates
'''

class ALU:
    def __init__(self):
        self.bit_mask = (1 << config.ALU_BIT_WIDTH) - 1

    def ADD(self, a, b):
        return (a + b) & self.bit_mask

    def SUB(self, a, b):
        return (a - b) & self.bit_mask

    def AND(self, a, b):
        return (a & b) & self.bit_mask

    def OR(self, a, b):
        return (a | b) & self.bit_mask

    def XOR(self, a, b):
        return (a ^ b) & self.bit_mask

    def NOT(self, a):
        return ~a & self.bit_mask

    def CMP(self, a, b):
        flags = {
            "Z": False,
            "C": False,
            "N": False,
            "V": False
        }

        a = a & self.bit_mask
        b = b & self.bit_mask
        result = a - b
        masked_result = result & self.bit_mask

        # Sign_bit: works by isolating the bit higher than the highest, and shifting to right
        sign_bit = (self.bit_mask + 1) >> 1


        if masked_result == 0:
            flags["Z"] = True

        if result < 0:
            flags["C"] = True

        # NEG. flag: if the sign bit is on, then the value is negative
        if (masked_result & sign_bit) != 0:
            flags["N"] = True

        a_sign = a & sign_bit
        b_sign = b & sign_bit

        if (a_sign != b_sign) and (a_sign != (masked_result & sign_bit)):
            flags["V"] = True
           
        return flags
