import threading
from p8.p8_cpu import P8_CPU
from Assembly.p8_assembler import P8_Assembler
import tkinter as tk

asm = P8_Assembler()
asm.encode(r"p8_emulator/Assembly/assemble.pasm", r"p8_emulator/Programs/program.rom")

root = tk.Tk()
img = tk.PhotoImage(width=16, height=16)
img.put("black", to=(0, 0, 16, 16))  # Fill background black

# Zoom 30x so 16x16 becomes 480x480 on screen
display = img.zoom(30, 30)
label = tk.Label(root, image=display)
label.pack()

# Simple function to update a single pixel (x, y)
def set_pixel(value):
    if value == 255:
        img.put("black", to=(0, 0, 16, 16)) 
        return None

    x = (value >> 4) & 0xF
    y = 15 - (value) & 0xF
  
    if 0 <= x < 16 and 0 <= y < 16:
        img.put("white", (x, y))
        # Refresh display
        global display
        display = img.zoom(30, 30)
        label.config(image=display)

screen = [["_  " for _ in range(16)] for _ in range(16)]

def edit_screen(value):
    x = (value >> 4) & 0xF
    y = (value) & 0xF

    screen[y][x] = "X  "

    print("\033[H", end="")

    for row in reversed(screen):
        new_row = ""    
        for pixel in row:
            new_row += pixel
        print(new_row)

def print_number(value):
    print("Current: " + str(value))

cpu = P8_CPU()

cpu.ports[1].initialize_write(set_pixel)

threading.Thread(target=lambda: cpu.run(300), daemon=True).start()

root.mainloop()

