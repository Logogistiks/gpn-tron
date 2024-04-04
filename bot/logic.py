"""Handles the game logic."""

# local
from utils import randMove

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

    def getPos(self) -> tuple[int, int]:
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
        self.map = [[" "]*int(sizeX)]*int(sizeY)
        self.players: dict[str, Player] = {}
        self.myID = pID
        self.wins = 0
        self.losses = 0

    def addPlayer(self, pID: str, name: str, posX: str=None, posY: str=None) -> None:
        """Adds a player to the game."""
        if not None in (posX, posY):
            self.players[pID] = Player(pID, name, posX, posY)
        else:
            self.players[pID] = Player(pID, name)

    def remPlayer(self, pID: str) -> None:
        """Removes a player from the game."""
        self.players.pop(pID, None)

    def updatePlayerPos(self, pID: str, posX: str, posY: str) -> None:
        """Updates a player's position."""
        self.players[pID].updatePos(posX, posY, self.sizeX, self.sizeY)

    def getMe(self) -> Player:
        """Returns the player object of the bot."""
        return self.players[self.myID]

    def getNpcs(self) -> dict[str, Player]:
        """Returns all the other players except the bot."""
        return {k: v for k, v in self.players.items() if k != self.myID}

    def nextMove(self, pID: str=None) -> str: # has ability to simulate moves of other players
        """Returns the next move for a player"""
        if pID is None:
            pID = self.myID
        newMove = self.calcMove(pID)
        self.players[pID].dir = newMove
        return newMove

    def calcMove(self, pID: str) -> str:
        """Calculates the next move for the bot."""
        return randMove(self.players[pID].dir) #todo: implement better logic