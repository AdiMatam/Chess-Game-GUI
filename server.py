import pickle
import socket
from threading import Thread

from board import Board
from const import ADDR, BUF

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)
sock.listen()

boards = {}
idcount = 0


def decode_pos(s: str):
    return ((int(s[0]), int(s[1])), (int(s[2]), int(s[3])))


def new_client(conn, player, boId):
    global idcount, boards
    conn.send(str.encode(str(player)))
    while True:
        try:
            data = conn.recv(BUF).decode()
            if boId in boards:
                board = boards[boId]
                if not data:
                    break
                else:
                    if data == "setup":
                        board.setup()
                    elif data != "get":
                        board.move(*decode_pos(data))
                    conn.sendall(pickle.dumps(board))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del boards[boId]
        print("Closing Game", boId)
    except:
        pass
    idcount -= 1
    conn.close()


print("WAITING for connection")
while True:
    conn, addr = sock.accept()
    print(f"<{addr}> connected")
    boardId = idcount // 2
    idcount += 1
    if idcount % 2 == 1:
        player = 1
        boards[boardId] = Board()
    else:
        player = -1
        boards[boardId].begin()
        boards[boardId].setup()

    Thread(target=new_client, args=(conn, player, boardId)).start()
