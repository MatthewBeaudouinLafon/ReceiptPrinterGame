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

PRINTER_WIDTH = 48
PAGE_WIDTH = 20

"""wrapper to use with a "with" statement"""
def open_descriptor():
    return open("/dev/lp0", 'wb')

""" select_code_page(n: int)
n: code page number (defined by printer)

Select code page to use specific character set
Notably: 0 is the default, 1 is cp437
cp437 has single byte shade blocks
"""
def select_code_page(n: int):
    return ESC + b"\x1D\x74" + bytes([n])


""" get_line(position, direction, shade)
position:         int position of player
direction_char:   direction character
shade:            line shade

returns game line with proper formatting
NOTE: DEPRECATED
"""
def get_line(position, direction_char, shade):
    return Block_char.EMPTY * 15 + (position) * shade + direction_char + (PAGE_WIDTH - position - 1) * shade

""" str_to_print(string)
string: string to be formatted for printing
        eg. "     LLL\L   FFFFF    "

Converts a simple representation of the line to be printed.

' ' -> empty block
'L' -> light shade block
'M' -> medium shade block
'H' -> heavy shade block
'F' -> ful; shade block
"""
def str_to_print(line):
    converter = {
        ' ' : Block_char.EMPTY,
        'L' : Block_char.LIGHT,
        'M' : Block_char.MED,
        'H' : Block_char.HEAVY,
        'F' : Block_char.FULL,
        '\\': Player_char.RIGHT,
        '/' : Player_char.LEFT
    }

    # TODO: Padding for smaller windows
    result = b''
    for char in line:
        result += converter[char]
    result += b'\n'

    return result

""" test_shade(printer)
printer: printer file descriptor

prints a gradient to test the characters work as intended.
"""
def test_shade(printer):
    for s in Block_char.SHADES:
        for _ in range(5):
            printer.write(s * PAGE_WIDTH + b"\n")
