#!~/.pyenv/versions/3.11.6/bin/python
#
# Copyright (c) 2024 Cutieguwu | Olivia Brooks
#
# -*- coding: utf-8 -*-
# @Title: CutieBoard
# @Author: Cutieguwu | Olivia Brooks
# @Description: Soundboard
#
# @Script: main.py
# @Date Created: 18 Dec, 2024
# @Last Modified: 18 Dec, 2024
# @Last Modified by: Cutieguwu | Olivia Brooks
# --------------------------------------------

from __future__ import annotations


from dataclasses import dataclass
from icecream import ic #type: ignore[import-untyped]
import os
from tkinter import Tk, LEFT, RIGHT
from tkinter.ttk import Button
from typing import *
from vlc import MediaPlayer #type: ignore[import-untyped]


DIR_BOARDS: str = os.path.dirname(__file__) + '/../soundboards/'
BOARD_NAMES: list[str]= [x.name for x in os.scandir(DIR_BOARDS)]
active_board:Optional[Board] = None

tk = Tk()
boards: list[Board] = []

class MissingBoardError(Exception):
    def __init__(self) -> None:
        super().__init__('Unable to locate a soundboard.')


@dataclass
class Board:
    name:str

    def __post_init__(self) -> None:
        global tk

        self._path = DIR_BOARDS + self.name + '/'
        self._buttons: list[Button] = []
        self.button = Button(
            tk,
            text=self.name,
            command=self.set
        )

        sounds: list[str] = [
            f for f in os.listdir(self._path)
            if os.path.isfile(self._path + f)
        ]

        for s in sounds:
            sound = Sound(s, self._path)
            self._buttons.append(Button(
                tk,
                text=s,
                command=sound.play
            ))
        
        ic(self._buttons)

    def set(self) -> None:
        global active_board
        global boards

        for b in boards:
            if self == active_board:
                b.unset()

        active_board = self

        for s in self._buttons:
            s.pack(side=RIGHT, padx=2, pady=2)

        ic()
    
    def unset(self) -> None:
        for b in self._buttons:
            b.pack_forget()
        
        ic()


@dataclass
class Sound:
    name:str
    board_path:str

    def __post_init__(self) -> None:
        self._media_player = MediaPlayer(self.board_path + self.name)

    def play(self) -> None:
        self._media_player.play()


if BOARD_NAMES.__len__() != 0:
    for name in BOARD_NAMES:
        boards.append(Board(name))
else:
    raise MissingBoardError

for b in boards:
    b.button.pack(side=LEFT, padx=2, pady=2)

tk.mainloop()