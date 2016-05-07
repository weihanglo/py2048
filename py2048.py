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
        self.nrow = row
        self.ncol = col
        self.gameover = False

    def merge(self, line):
        length = len(line)
        result = [i for i in line if i]
        result.extend([0] * (length - len(result)))
        for i in range(length - 1):
            if result[i] == result[i + 1]:
                result[i] *= 2
                result.pop(i + 1)
                result.append(0)
        return result

    def move(self, line, direction):
        if direction < 0:
            line_copy = line[:]
            line_copy.reverse()
            result = self.merge(line_copy)
            result.reverse()
        return result if direction < 0 else self.merge(line)

    def board_transpose(self):
        self.board = list(map(list, zip(*self.board)))

    def board_update_move(self, direction):
        if abs(direction) == 2:
            self.board_transpose()
            self.board = [self.move(line, direction) for line in self.board]
            self.board_transpose()
        else: 
            self.board = [self.move(line, direction) for line in self.board]

    def board_add_tile(self):
        while True:
            i = random.randrange(0, self.nrow)
            j = random.randrange(0, self.ncol)
            if self.board[i][j] == 0:
                self.board[i][j] = 2 if random.randrange(0, 10) > 1 else 4
                break
    def board_gameover(self):
        self.gameover = True
        for row in self.board:
            for elem in row:
                if elem is 0:
                    self.gameover = False
                    break
            if not self.gameover: break

        test_game = copy.deepcopy(self)
        for direction in [Py2048.DOWN, Py2048.DOWN, Py2048.UP, Py2048.RIGHT]:
            test_game.board_update_move(direction)
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
        
        self.board_add_tile()
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
                    self.board_update_move(direction[char][0])
            if char == 'q':
                break

            self.board_add_tile()
            self.board_gameover()
        print("\nGame Over")

if __name__ == '__main__':
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
