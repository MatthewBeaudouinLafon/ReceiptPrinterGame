#!/usr/bin/env python3

import time
import curses
from curses import textpad

import receipt_printer
from receipt_printer import Block_char, Player_char

FRAME_LENGTH = 0.1

# TODO: Show something on terminal window - instructions, length?
# TODO: Wrap-around mode?
# TODO: Increasing speed?
# TODO: Figure out why player.position keeps going float

class Player(object):
    def __init__(self):
        self.position: int = int(receipt_printer.PAGE_WIDTH) / 2
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
        
        
# class Block(object):
#     def __init__(self, position=None):
#         if position == None:

def open_test_file():
    return open("test.txt", 'wb')

if __name__ == "__main__":

    # initialize curses for non-blocking keyboard input
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    stdscr.nodelay(True)

    shade_id = 0

    player = Player()
    key = None
    paused = False

    # try:
    # with receipt_printer.open_descriptor() as printer:
    with open_test_file() as printer:
        printer.write(receipt_printer.select_code_page(1))
        
        while (key != ord('x')):
            time.sleep(FRAME_LENGTH)

            # Handle key input
            key = stdscr.getch()
            curses.flushinp()  # flush buffer key buffer to diminish delay
            
            if (key == ord(' ')):
                paused = not paused
            elif (key == curses.KEY_RIGHT):
                player.direction = 0
            elif (key == curses.KEY_LEFT):
                player.direction = 1

            if not paused:
                player.advance()

                line = list(" " * receipt_printer.PAGE_WIDTH)

                line[int(player.position)] = player.get_direction_char()
                
                print_line = receipt_printer.str_to_print(''.join(line))
                printer.write(print_line)
                # printer.write(receipt_printer.get_line(int(player.position), player.get_direction_char(), Block_char.SHADES[shade_id])+b"\n")

        printer.write(receipt_printer.select_code_page(0))

    # except: 
    #     curses.nocbreak()
    #     stdscr.keypad(False)
    #     curses.echo()
    #     curses.endwin()


    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
