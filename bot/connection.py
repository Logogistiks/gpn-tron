"""Handles the connection to the server."""

import socket
from colorama import Fore

# local
from utils import log

class Connection:
    def __init__(self, host: str, port: int) -> None:
        """Creates a connection to the server."""
        self.socket = socket.create_connection((host, port))

    def end(self, verbose: bool=True) -> None:
        """Ends the connection to the server."""
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        if verbose:
            log("connection closed")

    def readStream(self, buffer: int=1024, verbose: bool=True) -> list[list[str]]:
        """Reads a stream of commands from the server."""
        decoded = self.socket.recv(buffer).decode() # "cmd1|p11|p12\ncmd2|p21|p22\n"
        cmdlst = decoded.split("\n")[:-1] # ["cmd1|p11|p12", "cmd2|p21|p22"]
        if verbose:
            log(f"{Fore.LIGHTCYAN_EX}READ{Fore.WHITE} {cmdlst}")
        return list(map(lambda x: x.split("|"), cmdlst))

    def writeStream(self, *args: str, verbose: bool=True) -> None:
        """Writes a stream of commands to the server."""
        msg = "|".join(args) + "\n"
        self.socket.send(msg.encode())
        if verbose:
            log(f"{Fore.LIGHTGREEN_EX}WRITE{Fore.WHITE} {msg}")

if __name__ == "__main__":
    print("This file is not meant to be run directly")