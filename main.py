# https://github.com/freehuntx/gpn-tron/blob/master/PROTOCOL.md
import socket

def getAuth():
    with open("auth.csv") as f:
        return f.readlines()[-1].split(";")

class Connection:
    def __init__(self, host, port):
        self.socket = socket.create_connection((host, port))


HOST = "gpn-tron.duckdns.org"
PORT = 4000
USER, PASS = getAuth()
print(USER, PASS)