#!/usr/bin/env python3

ESC = b"\x1B"  # ESC character

BLOCK_EMPTY = b"\x20"
BLOCK_LIGHT = b"\xB0"
BLOCK_MED = b"\xB1"
BLOCK_HEAVY = b"\xB2"
BLOCK_FULL = b"\xDB"

RIGHT = b"\x5C"
LEFT = b"\x2F"

shading = [BLOCK_LIGHT, BLOCK_MED, BLOCK_HEAVY, BLOCK_FULL]

# PAGE_WIDTH = 48
PAGE_WIDTH = 10

def select_code_page(n: int):
    return ESC + b"\x1D\x74" + bytes([n])

def get_line(position, direction, shade):
    return BLOCK_EMPTY * 20 + (position) * shade + direction + (PAGE_WIDTH - position - 1) * shade

def other_direction(direction):
    if direction == LEFT:
        return RIGHT
    elif direction == RIGHT:
        return LEFT
    else:
        print("YO WHAT THE FUCK GIMME A REAL DIRECTION")
        return RIGHT

def test_shade():
    for s in shading:
        for i in range(5):
            f.write(s*PAGE_WIDTH+b"\n")

if __name__ == "__main__":
    position = 0
    shade_id = 0
    direction = RIGHT

    with open("/dev/lp0", 'wb') as f:
        f.write(select_code_page(1))

        for i in range(30):
            if not((i+1) % 10):
                shade_id += 1

            f.write(get_line(position, direction, shading[shade_id])+b"\n")
            
            if direction == RIGHT:
                position += 1
                if position == (PAGE_WIDTH - 1):
                    direction = other_direction(direction)
            elif direction == LEFT:
                position -= 1
                if position == 0:
                    direction = other_direction(direction)


        f.write(select_code_page(0))