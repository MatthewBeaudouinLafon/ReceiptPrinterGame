#!/usr/bin/env python3

import time
import random
import curses
from curses import textpad

import receipt_printer
from receipt_printer import Block_char, Player_char

FRAME_LENGTH = 0.1
NEW_BLOCK_LIKELIHOOD = 0.3

# TODO: Show something on terminal window - instructions, length?
# TODO: Wrap-around mode?
# TODO: Increasing speed?
# TODO: Figure out why player.position keeps going float

class Player(object):
    def __init__(self):
        self.position = int(receipt_printer.PAGE_WIDTH) / 2
        self.direction = 1  # 0=Right, 1=Left

    def advance(self):
        if self.direction == 0:  # Right
            self.position += 1
            if self.position == (receipt_printer.PAGE_WIDTH - 1):
                self.change_direction() 

        elif self.direction == 1:  # Left
            self.position -= 1
            if self.position == 0:
                self.change_direction()

        else:
            print("INVALID DIRECTION")

    def change_direction(self):
        self.direction = (self.direction + 1) % 2

    def get_direction_char(self):
        if self.direction == 0:
            # return Player_char.RIGHT
            return '\\'
        elif self.direction == 1:
            # return Player_char.LEFT
            return '/'
        else:
            print("INVALID DIRECTION")
            return None
        
        
class Block(object):
    WIDTH = 4
    LIFETIME = 5

    def __init__(self):
        self.position = random.randint(0, receipt_printer.PAGE_WIDTH - Block.WIDTH - 1)
        self.shade_id = 1
        self.phase_age = 0

    def advance(self):
        self.phase_age += 1

        if self.phase_age == Block.LIFETIME:
            self.phase_age = 0
            self.shade_id += 1

        if self.shade_id == (len(Block_char.SHADES) - 1):
            return True

        return False

    def get_line_char(self):
        shades = 'ELMHF'
        if (self.shade_id >= len(Block_char.SHADES)):
            print("Warning: shade_id too big")
            return 'F'
        return shades[self.shade_id]

def open_test_file():
    return open("test.txt", 'wb')

if __name__ == "__main__":

    # initialize curses for non-blocking keyboard input
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    block = None

    player = Player()
    key = None
    paused = False

    # try:
    # with receipt_printer.open_descriptor() as printer:
    with open_test_file() as printer:
        printer.write(receipt_printer.select_code_page(1))
        printer.flush()
        # receipt_printer.test_shade(printer)
        
        while (key != ord('x')):
            # time.sleep(0.001)
            time.sleep(FRAME_LENGTH)
            
            ### "time.sleep"
            # n = 0
            # while (n < 12500000):
            #     n += 1

            ##
            # printer.write(receipt_printer.str_to_print("   LLLMMM/HHHFFF   "))
            ##

            # Handle key input
            key = stdscr.getch()
            curses.flushinp()  # flush buffer key buffer to diminish delay
            
            if (key == ord(' ')):
                paused = not paused
            elif (key == curses.KEY_RIGHT):
                player.direction = 0
            elif (key == curses.KEY_LEFT):
                player.direction = 1

            if paused:
                continue

            player.advance()
            
            if block == None:
                if random.random() < NEW_BLOCK_LIKELIHOOD:
                    block = Block()
            else:
                end_of_block = block.advance()

                if end_of_block:
                    del block
                    block = None

            ### Rendering
            # space as background
            line = list(" " * receipt_printer.PAGE_WIDTH)

            # Render block
            if block != None:
                for i in range(block.position, (block.position + Block.WIDTH)):
                    line[i] = block.get_line_char()

            if line[int(player.position)] == Block_char.FULL:  # block collision
                printer.write(b'bye')
                break
            else:
                # player rendering
                line[int(player.position)] = player.get_direction_char()

            # ship it to printer
            print_line = receipt_printer.str_to_print(''.join(line))
            # print(print_line)
            printer.write(print_line)
            printer.flush()

        printer.write(receipt_printer.select_code_page(0))
        printer.flush()

    # except: 
    #     curses.nocbreak()
    #     stdscr.keypad(False)
    #     curses.echo()
    #     curses.endwin()


    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
