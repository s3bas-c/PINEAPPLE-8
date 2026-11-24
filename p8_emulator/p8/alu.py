import p8.config as config

class ALU:
    """Arithmetic Logic Unit (ALU) for performing bitwise and arithmetic tasks
    
    Attributes:
        bit_mask (int): Bitmask used to constrain results to `config.ALU_BIT_WIDTH`.
    """

    def __init__(self):
        self.bit_mask = (1 << config.ALU_BIT_WIDTH) - 1

    def ADD(self, a, b):
        """Compute the sum of two values, wrapped to ALU bit-width

        Args:
            a: first value
            b: second value

        Returns:
            The masked sum `(a + b) & self.bit_mask`
        """
        return (a + b) & self.bit_mask

    def SUB(self, a, b):
        """Compute the difference of two values, wrapped to ALU bit-width
        
        Args:
            a: first value
            b: second value

        Returns:
            The masked difference `(a - b) & self.bit_mask`
        """
        return (a - b) & self.bit_mask

    def AND(self, a, b):
        """Perform a bitwise AND operation between two values, wrapped to ALU bit-width

        Args:
            a: first value
            b: second value

        Returns:
            The masked result `(a & b) & self.bit_mask`
        """
        return (a & b) & self.bit_mask

    def OR(self, a, b):
        """Perform a bitwise OR operation between two values, wrapped to ALU bit-width
        
        Args:
            a: first value
            b: second value

        Returns:
            The masked result `(a | b) & self.bit_mask`
        """
        return (a | b) & self.bit_mask

    def XOR(self, a, b):
        """Perform a bitwise XOR operation between two values, wrapped to ALU bit-width
        
        Args:
            a: first value
            b: second value

        Returns:
            The masked result `(a ^ b) & self.bit_mask`
        """
        return (a ^ b) & self.bit_mask

    def NOT(self, a):
        """Perform a bitwise NOT operation on a value, wrapped to ALU bit-width
        
        Args:
            a: value

        Returns:
            The masked result `~a & self.bit_mask`
        """
        return ~a & self.bit_mask

    def CMP(self, a, b):
        """Return conditional flags by comparing the difference of two values
                
        Args:
            a: first value
            b: second value

        Returns:
            A dictionary that maps flag names to booleans:
                - "Z": Zero flag (if the result is 0)
                - "C": Carry/Borrow flag (if a carry/borrow occurred)
                - "N": Negative flag (if highest bit is 1, signed bit)
                - "V": Overflow flag (If signed overflow occurred)
        """
        flags = {
            "Z": False,
            "C": False,
            "N": False,
            "V": False
        }

        # mask each value
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

        # checks if sign bit is on
        a_sign = a & sign_bit
        b_sign = b & sign_bit

        if (a_sign != b_sign) and (a_sign != (masked_result & sign_bit)):
            flags["V"] = True

        return flags
