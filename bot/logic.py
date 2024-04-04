"""Handles the game logic."""

from random import choice

# local
from utils import DIRECTIONS, randMove

class Player:
    def __init__(self, pID: str, name: str, posX: str=None, posY: str=None) -> None:
        """Creates a player object."""
        self.pID = pID
        self.name = name
        self.pos = [(posX, posY)] if not None in (posX, posY) else []
        self.dir = None
        self.messages = []

    def updatePos(self, newPosX: str, newPosY: str, sizeX: int, sizeY: int) -> None:
        """Updates the player's position and direction."""
        if self.pos: #not first move
            dx = int(newPosX) - int(self.pos[-1][0])
            dy = int(newPosY) - int(self.pos[-1][1])
            if dx == 1 or dx == -sizeX:
                self.dir = "right"
            if dx == -1 or dx == sizeX:
                self.dir = "left"
            if dy == 1 or dy == -sizeY:
                self.dir = "down"
            if dy == -1 or dy == sizeY:
                self.dir = "up"
        self.pos.append((newPosX, newPosY))

    def getPos(self) -> tuple[str, str]:
        """Returns the player's current position."""
        return self.pos[-1]

    def addMsg(self, msg: str) -> None:
        """Adds a message to the player's message history."""
        self.messages.append(msg)

class GameHandler:
    def __init__(self, sizeX: str, sizeY: str, pID: str) -> None:
        """Creates a game object."""
        self.sizeX = int(sizeX)
        self.sizeY = int(sizeY)
        self.grid = [[" " for _ in range(int(sizeX))] for _ in range(int(sizeY))]
        self.players: dict[str, Player] = {}
        self.myID = pID
        self.wins = 0
        self.losses = 0

    def addPlayer(self, pID: str, name: str, posX: str=None, posY: str=None) -> None:
        """Adds a player to the game."""
        if not None in (posX, posY):
            self.players[pID] = Player(pID, name, posX, posY)
            self.grid[int(posY)][int(posX)] = pID
        else:
            self.players[pID] = Player(pID, name)

    def remPlayer(self, pID: str) -> None:
        """Removes a player from the game."""
        self.players.pop(pID, None)
        for y in range(self.sizeY):
            for x in range(self.sizeX):
                if self.grid[y][x] == pID:
                    self.grid[y][x] = " "

    def updatePlayerPos(self, pID: str, posX: str, posY: str) -> None:
        """Updates a player's position."""
        self.players[pID].updatePos(posX, posY, self.sizeX, self.sizeY)
        self.grid[int(posY)][int(posX)] = pID

    def getMe(self) -> Player:
        """Returns the player object of the bot."""
        return self.players[self.myID]

    def getNpcs(self) -> dict[str, Player]:
        """Returns all the other players except the bot."""
        return {k: v for k, v in self.players.items() if k != self.myID}

    def getNewPos(self, posX: str, posY: str, dir: str) -> tuple[str, str]:
        """Returns the new position after moving in the given direction."""
        if dir == "up":
            return posX, str((int(posY) - 1) % self.sizeY)
        if dir == "down":
            return posX, str((int(posY) + 1) % self.sizeY)
        if dir == "left":
            return str((int(posX) - 1) % self.sizeX), posY
        if dir == "right":
            return str((int(posX) + 1) % self.sizeX), posY

    def nextMove(self, pID: str=None) -> str: # has ability to simulate moves of other players
        """Moves the player and returns the move."""
        if pID is None:
            pID = self.myID
        newMove = self.calcMove(pID)
        self.players[pID].dir = newMove
        return newMove

    '''
    def calcMove(self, pID: str) -> str:
        """Calculates the next move for a player."""
        return randMove(self.players[pID].dir)
    '''

    def calcMove(self, pID: str) -> str:
        """Calculates the next move for a player."""
        possibleMoves = []
        for dir in DIRECTIONS:
            newPos = self.getNewPos(*self.players[pID].getPos(), dir)
            if self.grid[int(newPos[1])][int(newPos[0])] == " ":
                possibleMoves.append(dir)
        return choice(possibleMoves) if possibleMoves else "up" # theres nothing we can do but surrender