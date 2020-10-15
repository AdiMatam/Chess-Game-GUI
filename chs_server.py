import socket
from threading import Thread
import pickle
from chs_board import Board
from chs_const import ADDR, BUF


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.listen()

games = {}
idcount = 0


def new_client(conn, player, gameid):
    global idcount
    conn.send(str(player).encode())
    while True:
        if gameid in games:
            game = games[gameid]
            data = conn.recv(BUF).decode()
            if data:
                if data == "reset":
                    game.setup()
                elif data != "get":
                    pass
                conn.sendall(pickle.dumps(game))
            else:
                print("Connection Lost")
                break

    if gameid in games:
        del games[gameid]
        print(f"GAME {gameid} CLOSING")

    idcount -= 1
    conn.close()


print("WAITING for connection")
while True:
    conn, addr = sock.accept()
    gameid = idcount // 2
    idcount += 1
    if idcount % 2 == 1:
        player = 1
        games[gameid] = Board()

    else:
        player = -1
        games[gameid].begin()

    Thread(target=new_client, args=(conn, player, gameid))
