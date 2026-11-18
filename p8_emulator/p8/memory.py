import config as config

class Ram:
    """Random Access Memory (RAM) for runtime data storage"""
    def __init__(self):
        self.bit_mask = (1 << config.RAM_BIT_WIDTH) - 1
        self.ram_cells = [0 for _ in range((1 << config.RAM_ADDR_WIDTH))]

    def write(self, address, value):
        """Write a masked value to RAM cell
        
        Args:
            address: The address of the ram cell to overwrite
            value: The raw value written to the ram cell (Masked afterwards)
            
        Raises:
            IndexError: If Address is invalid or exceeds RAM capacity
        """

        try:
            self.ram_cells[address] = value & self.bit_mask
        except IndexError:
            raise IndexError("Address invalid or out of range (increase RAM_SIZE)")

    def read(self, address):
        """Reads and returns the value of a RAM cell at a certain address
        
        Args:
            address: The address of the RAM cell to read
            
        Raises:
            IndexError: If Address is invalid or exceeds RAM capacity
        """

        try:
            return self.ram_cells[address]
        except IndexError:
            raise IndexError("Address invalid or out of range (increase RAM_SIZE)")



class Rom:
    """Read only Memory (ROM) module for preloaded programs"""

    def __init__(self, data):
        
        self.rom_cells = data

    @classmethod
    def load_from_file(cls, file):
        """Automatically loads the program from a file, typically from a .bin or .rom file, in binary.
        
        Args:
            file: Path to the .bin or .rom file
            
        Raises:
            ValueError: if binary file exceeds the ROM capacity
        """
        

        max_size = (1 << config.ROM_ADDR_WIDTH)
        bit_mask = (1 << config.ROM_BIT_WIDTH) - 1

        # Automatically calculates the amount of bytes per item
        bytes_per_item = (config.ROM_BIT_WIDTH + 7) // 8
        max_file_bytes = max_size * bytes_per_item

        with open(file, "rb") as f:
            raw_bytes = f.read()

        if len(raw_bytes) > max_file_bytes:
            raise ValueError(f"ROM file exceeds CPU ROM capacity, increase config.ROM_ADDR_WIDTH!")

        cells = max_size * [0]

        current_byte = 1
        current_data = bytearray()
        slot = 0
        
        # Traverses through the list of bytes in Instruction sized chunks
        for byte in raw_bytes:

            if current_byte > bytes_per_item:
                current_data = bytearray()
                current_byte = 1
                slot += 1

            current_data.append(byte)
            current_byte += 1

            cells[slot] = int.from_bytes(current_data, byteorder="big") & bit_mask

        return cls(tuple(cells))

        
    def read(self, address):
        """Reads and returns the value of a rom cell at a certain address
        
        Args:
            address: The address of the ROM cell to read
            
        Raises:
            IndexError: If address is out of range
        """

        try:
            return self.rom_cells[address]
        except IndexError:
            raise IndexError("Address invalid or out of range (increase ROM_SIZE)")