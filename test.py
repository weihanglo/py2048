#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from copy import deepcopy

from py2048 import Py2048

class Test2048Core(unittest.TestCase):
    def setUp(self):
        self.game = Py2048(0, 0)

    def tearDown(self):
        del self.game

    def test_merge_0000(self):
        self.assertSequenceEqual(self.game.merge([0] * 4), [0] * 4)

    def test_merge_2020(self):
        self.assertSequenceEqual(self.game.merge([2, 0] * 2), [4, 0, 0, 0])

    def test_merge_2244(self):
        self.assertSequenceEqual(self.game.merge([2, 2, 4, 4]), [4, 8, 0, 0])

    def test_move_2244_left_right(self):
        self.assertSequenceEqual(self.game.move([2, 2, 4, 4], Py2048.LEFT), \
            [4, 8, 0 ,0])
        self.assertSequenceEqual(self.game.move([2, 2, 4, 4], Py2048.RIGHT), \
            [0, 0, 4 ,8])

    def test_move_2244_up_down(self):
        self.assertSequenceEqual(self.game.move([2, 2, 4, 4], Py2048.UP), \
            [4, 8, 0 ,0])
        self.assertSequenceEqual(self.game.move([2, 2, 4, 4], Py2048.DOWN), \
            [0, 0, 4 ,8])

class Test2048Board(unittest.TestCase):
    def setUp(self):
        self.game = Py2048(3, 3)
        self.game.board = [[2, 2, 2] , [2, 4, 4], [8, 8, 4]]

    def tearDown(self):
        del self.game

    def test_new_board_3x4(self):
        self.assertSequenceEqual(Py2048(3, 4).board, [[0] * 4] * 3)

    def test_board_transpose(self):
        new_game = deepcopy(self.game)
        new_game.board_transpose()
        self.assertSequenceEqual(new_game.board, \
            [[2, 2, 8], [2, 4, 8], [2, 4, 4]])

    def test_board_update_move_left(self):
        new_game = deepcopy(self.game)
        new_game.board_update_move(new_game.LEFT)
        self.assertSequenceEqual(new_game.board, \
            [[4, 2, 0], [2, 8, 0], [16, 4, 0]])

    def test_board_update_move_right(self):
        new_game = deepcopy(self.game)
        new_game.board_update_move(new_game.RIGHT)
        self.assertSequenceEqual(new_game.board, \
            [[0, 2, 4], [0, 2, 8], [0, 16, 4]])

    def test_board_update_move_up(self):
        new_game = deepcopy(self.game)
        new_game.board_update_move(new_game.UP)
        self.assertSequenceEqual(new_game.board, \
            [[4, 2, 2], [8, 4, 8], [0, 8, 0]])

    def test_board_update_move_down(self):
        new_game = deepcopy(self.game)
        new_game.board_update_move(new_game.DOWN)
        self.assertSequenceEqual(new_game.board, \
            [[0, 2, 0], [4, 4, 2], [8, 8, 8]])

    def test_add_tile(self):
        new_game = deepcopy(self.game)
        new_game.board[2][1] = new_game.board[1][2] = 0
        new_game.board_add_tile()
        tile1 = new_game.board[2][1]
        tile2 = new_game.board[1][2]
        self.assertTrue(any({tile1, tile2} & {2, 4}), 
            msg="Random tile not found")
    def test_gameover(self):
        new_game = Py2048(2, 2)
        new_game.board = [[2, 4], [8, 16]]
        new_game.board_gameover()
        self.assertTrue(new_game.gameover)

    def test_not_gameover(self):
        new_game = Py2048(2, 2)
        new_game.board = [[2, 4], [0, 16]]
        new_game.board_gameover()
        self.assertFalse(new_game.gameover)

if __name__ == '__main__':
    unittest.main(verbosity=2)
