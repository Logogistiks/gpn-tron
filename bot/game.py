# https://github.com/freehuntx/gpn-tron/blob/master/PROTOCOL.md
# https://github.com/freehuntx/gpn-tron/blob/master/ERRORCODES.md

# local
from utils import log, getAuth, logClear, splash, updateStats
from connection import Connection
from logic import GameHandler

def main(host: str, port: int, chat: bool=False, verbose: bool=True) -> None:
    logClear()
    tcp = Connection(host, port)
    if verbose:
        log("connection established")
    tcp.writeStream("join", *getAuth().values())

    try:
        while True:
            for msg in tcp.readStream():
                match msg[0]: # order like in docs
                    case "motd":
                        pass # ignore
                    case "error":
                        pass # todo: handle errors
                    case "game":
                        game = GameHandler(*msg[1:]) # overwrite game object
                        if chat:
                            tcp.writeStream("chat", splash())
                    case "pos":
                        game.updatePlayerPos(*msg[1:])
                    case "player":
                        game.addPlayer(*msg[1:])
                    case "tick":
                        newMove = game.getMe().nextMove()
                        game.getMe().dir = newMove
                        tcp.writeStream("move", newMove)
                    case "die":
                        for id in msg[1:]:
                            game.remPlayer(id)
                    case "message":
                        game.players[msg[1]].addMsg(msg[2])
                    case "win":
                        updateStats(msg[1], msg[2])
                    case "lose":
                        updateStats(msg[1], msg[2])
    except KeyboardInterrupt:
        tcp.end()

if __name__ == "__main__":
    main(host="localhost", port=4000, chat=True)