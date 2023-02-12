
import os

COLOR_MAP = {
    "r": "red",
    "g": "green",
    "b": "blue",
    "y": "yellow",
    "j": "joker",
}
NUMBER_MAP = {
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "r": "reverse",
    "n": "skip",
    "+2": "draw 2",
    "j": "wildcard",
    "+4": "draw 4",
}

def get_players_number() -> int:
    while True:
        try:
            return int(input("Players number: "))
        except (ValueError, EOFError):
            print("Sorry, this is not a number")
            continue


def _input(prompt: str = "") -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""


def card_valid(color: str, number: str) -> bool:
    if color == "j" and number in ("j", "+4"):
        return True
    if color in ("r", "g", "b", "y") and number in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "r", "n", "+2"):
        return True
    return False


def clear() -> None:
    if not self.DEV_MODE:
        _input("Press <enter> to clear the screen and continue")
        os.system("clear")


def get_how_many_to_pull() -> int:
    try:
        return int(input("Do I have to pull? If so, how much: "))
    except (ValueError, EOFError):
        return 0
