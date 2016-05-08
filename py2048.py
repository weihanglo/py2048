#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import copy
import random

from getch import getch

class Py2048(object):
    UP = 2
    LEFT = 1
    DOWN = -2
    RIGHT = -1

    def __init__(self, row, col):
        self.board = [[0 for r in range(col)] for c in range(row)]
        self.board_size = row, col
        self.gameover = False

    @classmethod
    def _merge(cls, line):
        length = len(line)
        result = [i for i in line if i]
        result.extend([0] * (length - len(result)))
        for i in range(length - 1):
            if result[i] == result[i + 1]:
                result[i] *= 2
                result.pop(i + 1)
                result.append(0)
        return result

    
    @classmethod
    def _move(cls, line, direction):
        if direction < 0:
            line_copy = line[:]
            line_copy.reverse()
            result = cls._merge(line_copy)
            result.reverse()
        return result if direction < 0 else cls._merge(line)

    def _transpose(self):
        self.board = list(map(list, zip(*self.board)))

    def _check_zero_tile(self):
        has_zeros = False
        for row in self.board:
            for elem in row:
                if elem is 0:
                    has_zeros = True
                    break
            if has_zeros: break
        return has_zeros

    def update_move(self, direction):
        if abs(direction) == 2:
            self._transpose()
            self.board = [self._move(line, direction) for line in self.board]
            self._transpose()
        else: 
            self.board = [self._move(line, direction) for line in self.board]

    def add_tile(self):
        has_zeros = self._check_zero_tile()
        while has_zeros:
            i = random.randrange(0, self.board_size[0])
            j = random.randrange(0, self.board_size[1])
            if self.board[i][j] is 0:
                self.board[i][j] = 2 if random.randrange(0, 10) > 1 else 4
                break

    def check_gameover(self):
        has_zeros = self._check_zero_tile()
        self.gameover = not has_zeros
        if not has_zeros:
            test_game = copy.deepcopy(self)
            for direction in [Py2048.DOWN, Py2048.DOWN, Py2048.UP, Py2048.RIGHT]:
                test_game.update_move(direction)
                if test_game.board != self.board:
                    self.gameover = False
                    break

    def gameloop(self):
        def clear(): os.system('cls' if os.name=='nt' else 'clear')

        def print_board():
            print('\tGame Board')
            print('----------------------------')
            for row in self.board:
                print(*row, sep='\t', end='\n')
            print('----------------------------')

        direction = {
            'A': [self.UP, "UP"],
            'B': (self.DOWN, "DOWN"),
            'C': (self.RIGHT, "RIGHT"),
            'D': (self.LEFT, "LEFT"),
        }
        
        self.add_tile()
        while not self.gameover:
            old_board = copy.deepcopy(self.board)
            char = None
            while old_board == self.board:
                clear()
                print_board()
                char = getch()
                if char == 'q':
                    break
                if direction.get(char):
                    self.update_move(direction[char][0])
            if char == 'q':
                break

            self.add_tile()
            self.check_gameover()
        print("\nGame Over")

def main():
    print('Welcome to 2048!')
    print('================')
    print('Please use arrow keys to play.')
    print('Use "q" to quit.\n')
    print('Setup the board size.')
    while True:
        row = str(input("Row: "))
        col = str(input("Column: "))
        if row.isdecimal() and col.isdecimal():
            row = int(row)
            col = int(col)
            if row >= 1 <= col:
                break
        print("\nWrong size? Please input correct size.\n")
    game = Py2048(row, col)
    game.gameloop()

if __name__ == '__main__':
    main()
