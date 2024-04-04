# https://github.com/freehuntx/gpn-tron/blob/master/PROTOCOL.md
# https://github.com/freehuntx/gpn-tron/blob/master/ERRORCODES.md

import os
from random import random
from time import sleep
from colorama import Fore

# local
from utils import log, getAuth, logClear, splash, updateStats
from connection import Connection
from logic import GameHandler

def main(host: str, port: int, chat: bool=False, chatProb: int|float=10) -> None:
    """Parameters:
    * `host`: str - the server host
    * `port`: int - the server port
    * `chat`: bool - whether to enable chat
    * `chatProb`: int|float - the probability of sending a chat message each tick in percent"""
    logClear()
    tcp = Connection(host, port)
    log("connection established")
    tcp.writeStream("join", *getAuth().values())

    try:
        while True:
            for msg in tcp.readStream():
                match msg[0]: # order like in docs
                    case "motd":
                        pass # ignore
                    case "error":
                        log(f"{Fore.LIGHTRED_EX}ERROR{Fore.WHITE} {msg[1]}")
                    case "game":
                        game = GameHandler(*msg[1:]) # overwrite game object
                    case "pos":
                        game.updatePlayerPos(*msg[1:])
                    case "player":
                        game.addPlayer(*msg[1:])
                    case "tick":
                        newMove = game.getMe().nextMove()
                        game.getMe().dir = newMove
                        tcp.writeStream("move", newMove)
                        if chat and random() < chatProb/100:
                            sleep(0.05)
                            tcp.writeStream("chat", splash())
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
        log("connection closed")

if __name__ == "__main__":
    main(host="localhost", port=4000, chat=True)