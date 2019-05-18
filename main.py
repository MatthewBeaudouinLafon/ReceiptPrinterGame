#!/usr/bin/env python3

import sys
import select
import time

import curses
from curses import textpad

import receipt_printer
from receipt_printer import Block_char, Player_char

class Player(object):
    def __init__(self):
        self.position = int(receipt_printer.PAGE_WIDTH) / 2
        self.direction = 0  # 0=Right, 1=Left

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
            return Player_char.RIGHT
        elif self.direction == 1:
            return Player_char.LEFT
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
    
    # ### TEST LOOP
    # with open_test_file() as printer:
    #     while True:
    #         time.sleep(0.1)
    #         player.advance()
    #         print(player.position)
    #         printer.write(receipt_printer.get_line(int(player.position), player.get_direction_char(), Block_char.SHADES[shade_id])+b"\n")


    ### REAL GAME LOOP
    # with receipt_printer.open_descriptor() as printer:
    with open_test_file() as printer:
        printer.write(receipt_printer.select_code_page(1))
        
        while (key != ord('x')):
            time.sleep(0.1)

            # Handle key input
            key = stdscr.getch()
            curses.flushinp()  # flush buffer key buffer to diminish delay
            
            if (key == curses.KEY_RIGHT):
                player.direction = 0
            elif (key == curses.KEY_LEFT):
                player.direction = 1
            elif (key == ' '):
                paused = not paused

            if not paused:
                player.advance()
                
            printer.write(receipt_printer.get_line(int(player.position), player.get_direction_char(), Block_char.SHADES[shade_id])+b"\n")

        printer.write(receipt_printer.select_code_page(0))

    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
