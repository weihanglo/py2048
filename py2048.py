#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from itertools import chain
from random import randrange

from logic.logic import Py2048

_WIDTH = _HEIGHT = 512
_WELCOMEMSG = (
    ('', '2048', 'in', 'Py', ''),
    ('', 'Select', '', 'Board\nSize', ''), 
    (3, '', 4, '', 5),
    ('', 6, '', 7, ''),
    ('Source\nCode', 'https://', 'github.com', '/weihanglo', '/py2048'),
)
_COLOR = {
    'mainBg': '#bbada0', 'darktext': '#776e65', 'lighttext': '#f9f6f2',
    0: '#ccc0b4', 2: '#eee4da', 4: '#ede0c8', 8: '#f2b179', 16: '#f59563',
    32: '#f67c5f', 64: '#f65e3b', 128: '#edcf72', 256: '#edcc61',
    512: '#edc850', 1024: '#edc53f', 2048: '#edc22e', 4096: '#ed702e',
    8192: '#ed4c2e', 16384: '#c83d22', 32768: '#A0301B', 65536: '#802615',
}
_FONT = {
    '2XL': ('Helvetica', 72, 'bold'),
    'XL': ('Helvetica', 60, 'bold'),
    'L': ('Helvetica', 44, 'bold'),
    'M': ('Helvetica', 32, 'bold'),
    'S': ('Helvetica', 24, 'bold'),
    'XS': ('Helvetica', 16, 'bold'),
}

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._game = None
        self._cells = []
        self.master.title("2048 in Tkinter")
        self.master.maxsize(_WIDTH, _HEIGHT)
        self.master.minsize(_WIDTH, _HEIGHT)
        self.master.config(bg=_COLOR['mainBg'])
        self.config(bg=_COLOR['mainBg'])
        self.grid(row=2, column=2)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(2, weight=1)

    def _setGrids(self, nrow, ncol, data, fonttype='S'):
        width = _WIDTH / (1.1 * nrow + 0.1)
        height = _HEIGHT / (1.1 * ncol + 0.1)
        padx = 0.05 * width
        pady = 0.05 * height
        self._cells = []
        for row in range(nrow):
            cellRow = []
            for col in range(ncol):
                frame = tk.Frame(self, width=int(width), height=int(height))
                frame.propagate(0)
                frame.grid(column=col, row=row, padx=int(padx), pady=int(pady))
                var = data[row][col]
                text = var if var else ""
                cell = tk.Label(frame, text=text)
                cell.config(font=_FONT.get(fonttype, 'S'))
                cell.config(width=int(width), height=int(height))
                cell.config(justify=tk.CENTER, bg=_COLOR[0])
                cell.pack()
                cellRow.append(cell)
            self._cells.append(cellRow)
        self.update_idletasks()

    def _newGame(self, nrow, ncol):
        self._game = Py2048(nrow, ncol)
        fontsize = 'M' if nrow < 6 else 'XS'
        self._setGrids(nrow, ncol, self._game.board, fontsize)
        self._game.add_tile()
        self._updateBoard()
        self.bind('<Key>', self._keyPressWhileGame)

    def _mouseActionWhileSet(self, event):
        widget = event.widget
        value = widget.cget('text')
        value = { 
            '4': lambda: int(value) if value else 0,
            '7': lambda: widget.config(font=_FONT['2XL']), 
            '8': lambda: widget.config(font=_FONT['M']),
        }[event.type]()
        if value:
            self._destroyChildren()
            self._newGame(value, value)

    def _keyPressWhileGame(self, event):
        direction = getattr(Py2048, event.keysym.upper(), None)
        if not self._game.gameover and direction:
            self.unbind('<Key>')
            self._game.update_move(direction)
            self._game.add_tile()
            self._updateBoard()
        self._game.check_gameover()
        if self._game.gameover:
            self.after(1500, self._displayGameOver)
            self.after(1500 + 2000, self._destroyChildren)
            self.after(1500 + 2000, self.waitForStart)
        else:
            self.bind('<Key>', self._keyPressWhileGame)

    def _destroyChildren(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _updateBoard(self):
        for i, cellRow in enumerate(self._cells):
            for j, cell in enumerate(cellRow):
                var = self._game.board[i][j]
                text = var if var else ""
                fg = _COLOR['darktext'] if var <= 4 else _COLOR['lighttext']
                cell.config(text=text, bg=_COLOR[var], fg=fg)

    def _displayGameOver(self):
        text = list("GameOver")
        text.reverse()
        bg = _COLOR[0]
        fg = _COLOR['darktext']
        font = _FONT.get('M' if self._game.board_size[0] < 6 else 'XS')
        for cell in chain.from_iterable(self._cells):
            if text:
                cell.config(text=text.pop(), bg=bg, fg=fg, font=font)

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        l = len(value)
        s = int(l / 3)
        return tuple(int(value[i:i + s], 16) for i in range(0, l, s))

    @staticmethod
    def rgb_to_hex(value):
        return '#{:x}{:x}{:x}'.format(*value)

    def waitForStart(self):
        nrow = len(_WELCOMEMSG)
        ncol = len(_WELCOMEMSG[0])
        self._setGrids(nrow, ncol, _WELCOMEMSG, 'XS')
        color = map(lambda x: (_COLOR[x], x),
            map(lambda _: 2 ** randrange(1, 14), range(ncol * 2)))
        for cell, col in zip(chain.from_iterable(self._cells[2:4]), color):
            fg = _COLOR['darktext'] if col[1] <= 4 else _COLOR['lighttext']
            cell.config(bg=col[0], fg=fg, font=_FONT['M'])
            cell.bind('<Enter>', self._mouseActionWhileSet)
            cell.bind('<Leave>', self._mouseActionWhileSet)
            cell.bind('<Button-1>', self._mouseActionWhileSet)
        for cell in self._cells[0]:
            cell.config(font=_FONT['M'])

def runApp():
    app = App()
    app.waitForStart()
    app.focus()
    app.mainloop()

if __name__ == '__main__':
    runApp()
