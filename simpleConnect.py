from main import Connection, getAuth
from time import sleep
import keyboard

HOST1 = "gpn-tron.duckdns.org"
PORT1 = 4000

HOST2 = "127.0.0.1"
PORT2 = 23

USER, PASS = getAuth()

tcp = Connection(HOST1, PORT1)
print("connection made")
tcp.writeStream("join", USER, PASS)
while True:
    #msg = tcp.socket.recv(512)
    msg = tcp.socket.recv(512)
    if msg:
        print(msg)