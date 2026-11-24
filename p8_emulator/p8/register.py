import p8.config as config

class Register:
    """Register for quick single value data storage
        
    Attributes:
        value (int): Stored value of the register.
        bit_mask (int): Bitmask used to constrain values to `config.REGISTER_BIT_WIDTH`
    """

    def __init__(self):
        self.value = 0
        self.bit_mask = (1 << config.REGISTER_BIT_WIDTH) - 1

    def read(self):
        """Return the current stored value
        
        Returns: 
            The stored value of the register `self.value`
        """
        return self.value

    def write(self, value):
        """Overwrite the current stored value, wrapped to register bit-width
        
        Args:
            value: The new value to store
        """
        self.value = value & self.bit_mask

    def increment(self):
        """Increment stored value by one, wrapped to register bit-width"""
        self.value += 1
        self.value = self.value & self.bit_mask

    def decrement(self):
        """Decrement stored value by one, wrapped to register bit-width"""
        self.value -= 1
        self.value = self.value & self.bit_mask

    def clear(self):
        """Clear stored value by setting it to 0"""
        self.value = 0