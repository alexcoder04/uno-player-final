"""
Command-Line Interface for entering the cards and other data
"""

import os

from .generic import get_players_number, _input


class CmdLineDataloader:
    def __init__(self, dev_mode: bool = True) -> None:
        self.DEV_MODE = dev_mode

    def get_players_number(self) -> int:
        return get_players_number()

    def read_card(self, prompt: str) -> tuple:
        while True:
            try:
                [color, number] = _input(prompt).split(",")
            except (ValueError, EOFError):
                print("Sorry, cannot read your input")
                continue
            color, number = color.strip(), number.strip()
            if color not in ("r", "g", "b", "y", "j"):
                print("Sorry, invalid color, use (r,g,b,y,s)")
                continue
            if color != "j" and number not in (
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "r",
                "n",
                "+2",
                "j",
            ):
                print("Sorry, invalid number, use(0,1,2,3,4,5,6,7,8,9,r,n,+2,j)")
                continue
            if color == "j" and number not in ("j", "+4"):
                print("Sorry, invalid number, use (j,+4)")
                continue
            special = True if color == "j" else False
            return color, number, special

    def get_how_many_to_pull(self) -> int:
        try:
            return int(_input("Do I have to pull? If so, how much: "))
        except (ValueError, EOFError):
            return 0

    def clear(self) -> None:
        if not self.DEV_MODE:
            try:
                _input("Press <enter> to clear the screen and continue")
            except EOFError:
                pass
            os.system("clear")
