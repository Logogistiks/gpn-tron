"""Outsourced utility functions."""

from random import choice

DIRECTIONS = ["up", "right", "down", "left"] # do not change order

def getAuth() -> dict[str, str]:
    """Returns the last entry in the auth file as {"user", "pass"}"""
    with open("auth.csv") as f:
        return {k: v for k, v in zip(["user", "pass"], f.readlines()[-1].split(";"))}

def log(message: str, silent: bool=False):
    """Logs a message to the log file and prints it to the console if not silent."""
    with open("log.txt", "a") as f:
        f.write(message + "\n")
    if not silent:
        print(message)

def logClear() -> None:
    """Clears the log file."""
    with open("log.txt", "w") as f:
        f.write("")

def splash() -> str:
    """Returns a random splash message from the splashes file."""
    with open("splashes.txt", "r") as f:
        return choice(f.readlines())

def reverseDir(dir: str) -> str:
    """Returns the opposite direction of the given direction."""
    return DIRECTIONS[(DIRECTIONS.index(dir) + 2) % 4] # depends on the defined order of DIRECTIONS

def updateStats(wins: int, losses: int) -> None:
    """Updates the stats file with the given wins and losses."""
    with open("stats.txt", "w") as f:
        f.write(f"wins;losses\n{wins};{losses}")

#temp
def randMove(dir: str) -> str:
    """TEMPORARY: Returns a random direction while avoiding impossible move (180-turn)."""
    return choice(tuple(set(DIRECTIONS) - set(reverseDir(dir))))