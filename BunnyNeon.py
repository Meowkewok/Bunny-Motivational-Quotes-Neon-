import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import random

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1
)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

bunny_bitmap_data = [
    0b00000011000000000110000000000000,
    0b00000011000000000110000000000000,    
    0b00000011100000001110000000000000,
    0b00000001110000011100000000000000,
    0b00000001111111111100000000000000,
    0b00000001101111101100000000000000,
    0b00000011101111101110000000000000,
    0b00000011111111111110000000000000,
    0b00000001111111111100000000000000,
    0b00000000111111111000000000000000,
]

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xFFFFFF

bunny_bitmap = displayio.Bitmap(32, 10, 2)
for row in range(10):
    for column in range(32):
        if bunny_bitmap_data[row] & (1 << (31 - column)):
            bunny_bitmap[column, row] = 1
        else:
            bunny_bitmap[column, row] = 0

bunny_sprite = displayio.TileGrid(bunny_bitmap, pixel_shader=palette)
bunny_sprite.x = 0
bunny_sprite.y = 21


line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x5D3FD3,
    text="")
line1.x = display.width
line1.y = 8

g=displayio.Group()
g.append(line1)
g.append(bunny_sprite)
display.root_group = g

quotes = ["Hop toward your dreams, one leap at a time!",
    "Even the smallest bunny can leave the biggest paw prints.",
    "When life gets tough, just hop over it!",
    "Stay fluffy, stay strong, and always keep hopping forward.",
    "You don't have to be the biggest to make the biggest impact.",
    "Every hop is progress, no matter how small.",
    "The best things in life are worth hopping for.",
    "Don’t worry if you stumble, just hop right back up!",
    "Hoppiness is found in the little leaps.",
    "Be brave like a bunny: bounce back from every setback!",
    "Don't worry, be hoppy.",
    "Hop to it, you can do it!",
    "Jump, jump, jump!"
    ]

def scroll(line):
    line.x -= 1
    line_width = line.bounding_box[2]
    if line.x + line_width <= 0:
        time.sleep(60)
        line.x = display.width


while True:
    line1.text = quotes[random.randint(0,12)]
    while line1.x + line1.bounding_box[2] > 0:
        scroll(line1)
        display.refresh()
        
