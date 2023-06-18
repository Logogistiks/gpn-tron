# main imports
from multiprocessing import Process, Pipe
import threading
import os
from pathlib import Path

# bot imports
import socket
from random import choice

def flatten_dict(dictionary, parent_key='', separator='.'):
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, new_key, separator))
        else:
            flattened_dict[new_key] = value
    return flattened_dict

##########################################################################
# REGION DEF BOT START                                                   #
##########################################################################
if True: # just for editor folding
    def getAuth():
        with open("auth.csv") as f:
            return f.readlines()[-1].split(";")

    def log(message: str, silent: bool=False):
        with open("log.txt", "a") as f:
            f.write(message + "\n")
        if not silent:
            print(message)

    def logClear():
        with open("log.txt", "w") as f:
            f.write("")

    def splash():
        with open("splashes.txt", "r") as f:
            return choice(f.readlines())

    class Connection:
        def __init__(self, host: str, port: int):
            self.socket = socket.create_connection((host, port))

        def end(self):
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            log("connection closed")

        def readStream(self, buffer: int=1024):
            decoded = self.socket.recv(buffer).decode() # "cmd1|p11|p12\ncmd2|p21|p22\n"
            cmdlst = decoded.split("\n")[:-1] # ["cmd1|p11|p12", "cmd2|p21|p22"]
            log(f"read stream < {cmdlst} >")
            return list(map(lambda x:x.split("|"), cmdlst)) # [["cmd1", "p11", "p12"], ["cmd2", "p21", "p22"]]

        def writeStream(self, *args):
            msg = "|".join(args) + "\n"
            self.socket.send(msg.encode())
            log(f"written stream < {msg} >")

    class GameManager:
        def __init__(self, mapX: str, mapY: str, id: str, comchannel):
            self.mapX = int(mapX)
            self.mapY = int(mapY)
            self.myID = id
            self.players = {}
            self.wins = 0
            self.losses = 0
            self.com = comchannel

        def addPlayer(self, id: str, name: str=None, posX: str=None, posY: str=None):
            self.players[id] = Player(name, posX, posY)

        def remPlayer(self, id: str):
            if id in self.players:
                del self.players[id]

        def getMe(self):
            return self.players[self.myID]

        def getNpcs(self):
            return {k:v for k,v in self.players.items() if k != self.myID}

        def getGameState(self):
            gamestate = dict(vars(self))
            gamestate["players"] = {}
            for id, pl in self.players.items():
                gamestate["players"][id] = vars(pl)
            return gamestate

        def nextMove(self):

            self.com.send({"req move": self.getGameState()})
            move = self.com.recv()
            self.com.send(self.getGameState())
            return move

    class Player:
        def __init__(self, name: str, posX: str, posY: str):
            self.name = name
            self.posX = []
            self.posY = []
            self.updatePos(posX, posY)
            self.messages = []

        def updatePos(self, posX: str, posY: str):
            self.posX.append(posX)
            self.posY.append(posY)

        def addMsg(self, msg: str):
            self.messages.append(msg)

    def main(h, p, u, pw, conn):
        comrec = conn.recv() # wait for ready signal
        while True:
            tcp = Connection(h, p)
            log("connection established")
            tcp.writeStream("join", u, pw)

            while True:
                msglst = tcp.readStream() # [['motd', 'You can find...']]
                for msg in msglst:
                    match msg[0]:
                        case "error":
                            pass
                        case "motd":
                            pass
                        case "game":
                            try: del game
                            except: pass
                            game = GameManager(*msg[1:], conn)
                            #tcp.writeStream("chat", splash())
                        case "pos":
                            game.players[msg[1]].updatePos(*msg[2:])
                        case "player":
                            game.addPlayer(msg[1], msg[2])
                        case "tick":
                            tcp.writeStream("move", game.nextMove())
                        case "die":
                            try:
                                for id in msg[1:]:
                                    game.remPlayer(id)
                            except: pass
                        case "message":
                            game.players[msg[1]].addMsg(msg[2])
                        case "win":
                            #conn.send({"win": game.getGameState()})
                            game.wins = msg[1]
                            game.losses = msg[2]
                        case "lose":
                            #conn.send({"lose": game.getGameState()})
                            game.wins = msg[1]
                            game.losses = msg[2]
##########################################################################
# REGION DEF BOT END                                                     #
##########################################################################



##########################################################################
# REGION DEF RL START                                                    #
##########################################################################

##########################################################################
# REGION DEF RL END                                                      #
##########################################################################

def startServer(num):
    original = os.getcwd()
    new = Path(original[0].upper() + original[1:], "serverside")
    sub = Path(original[0].upper() + original[1:], "serverside", "server")

    os.chdir(sub)
    with open("index_original.ts", "r") as f:
        code = f.readlines()
        newcode = "".join([line if not line.startswith("const NUMBOTS") else f"const NUMBOTS = {num}\n" for line in code])
    with open("index.ts", "w") as f:
        f.write(newcode)

    os.chdir(new)
    os.system("yarn dev")
    os.chdir(original)

def startBot(conn):
    os.chdir("bot")
    HOST = "localhost"
    PORT = 4000
    USER, PASS = getAuth()
    logClear()
    while True:
        main(HOST, PORT, USER, PASS, conn)

def startRL(conn):
    # start rl script
    conn.send("ready")
    while True:
        comrec = conn.recv()
        if "req move" in comrec:
            gamestate = comrec["req move"]
            move = choice(["up", "down", "left", "right"]) # interact with rl agent based on gamestate
            conn.send(move)

if __name__ == '__main__':
    numBots = 5

    conn1, conn2 = Pipe(duplex=True)

    server = Process(target=startServer, args=[numBots])
    bot = threading.Thread(target=startBot, args=[conn1])
    rl = Process(target=startRL, args=[conn2])

    server.start()
    bot.start()
    rl.start()

    server.join()
    bot.join()
    rl.join()