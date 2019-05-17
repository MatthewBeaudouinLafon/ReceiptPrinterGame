## receipt_printer.py
# This file should handle all of the receipt printer interaction.
# It also defines redefinitions of characters. 


class Block_char:
    EMPTY = b"\x20"
    LIGHT = b"\xB0"
    MED = b"\xB1"
    HEAVY = b"\xB2"
    FULL = b"\xDB"

    SHADES = [EMPTY, MED, HEAVY, FULL]


class Player_char:
    RIGHT = b"\x5C"
    LEFT = b"\x2F"


ESC = b"\x1B"  # ESC character

# PAGE_WIDTH = 48
PAGE_WIDTH = 10

# wrapper to use with a "with" statement
def open_descriptor():
    return open("/dev/lp0", 'wb')

# Select code page to use specific character set
# Notably: 0 is the default, 1 is cp437
# cp437 has single byte shade blocks
def select_code_page(n: int):
    return ESC + b"\x1D\x74" + bytes([n])

### get_line(position, direction, shade)
# position:         int position of player
# direction_char:   direction character
# shade:            line shade
# returns game line with proper formatting
def get_line(position, direction_char, shade):
    return Block_char.EMPTY * 20 + (position) * shade + direction_char + (PAGE_WIDTH - position - 1) * shade

### test_shade(printer)
# prints a gradient to test the characters work as intended.
#
# printer: printer file descriptor
def test_shade(printer):
    for s in Block_char.SHADES:
        for _ in range(5):
            printer.write(s * PAGE_WIDTH + b"\n")
