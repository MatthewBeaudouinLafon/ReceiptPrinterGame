#!/usr/bin/env python3

import receipt_printer
from receipt_printer import Block_char, Player_char

class Player(object):
    def __init__(self):
        self.position = int(receipt_printer.PAGE_WIDTH) / 2
        self.direction = 0  # 0=Right, 1=Left

    def advance(self):
        if self.direction == Player_char.RIGHT:
            self.position += 1
            if self.position == (receipt_printer.PAGE_WIDTH - 1):
                self.change_direction()

        elif self.direction == Player_char.LEFT:
            self.position -= 1
            if self.position == 0:
                self.change_direction()

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

def other_direction(direction):
    if direction == Player_char.LEFT:
        return Player_char.RIGHT
    elif direction == Player_char.RIGHT:
        return Player_char.LEFT
    else:
        print("YO WHAT THE FUCK GIMME A REAL DIRECTION")
        return Player_char.RIGHT

if __name__ == "__main__":
    shade_id = 0
    # position = 0
    # direction = Player_char.RIGHT
    player = Player()

    with receipt_printer.open_descriptor() as printer:
        printer.write(receipt_printer.select_code_page(1))

        for i in range(30):
            if not((i+1) % 10):
                shade_id += 1

            printer.write(receipt_printer.get_line(player.position, player.get_direction_char(), Block_char.SHADES[shade_id])+b"\n")
            
            
            player.advance()


        printer.write(receipt_printer.select_code_page(0))
