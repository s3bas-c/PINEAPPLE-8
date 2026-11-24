import p8.config as config

class Port:
    def __init__(self):
        self.read_function = None
        self.write_function = None

        self.bit_mask = (1 << config.PORT_BIT_WIDTH) - 1

    def initialize_read(self, function):
        self.read_function = function

    def initialize_write(self, function):
        self.write_function = function

    def on_read(self):
        return self.read_function()

    def on_write(self, value):
        return self.write_function(value & self.bit_mask)