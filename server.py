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


def new_client(conn, player, boId):
    global idcount, boards
    print("Starting client!")
    conn.send(str(player).encode())
    while True:
        try:
            data = conn.recv(BUF).decode()
            if boId in boards:
                board = boards[boId]
                if not data:
                    break
                else:
                    if "select" in data:
                        split = data.split(",")
                        row, col = int(split[1]), int(split[2])
                        board.set_selected(board.piece_at(row, col))
                        board.store_allowed()
                    elif "move" in data:
                        split = data.split(",")
                        row, col = int(split[1]), int(split[2])
                        board.move(row, col)
                    elif "updated" in data:
                        player = int(data.split(",")[1])
                        print(f"Player {player} - update token")
                        board.update_went(player)
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
        boards[boardId].setup()
    else:
        player = -1

    Thread(target=new_client, args=(conn, player, boardId)).start()
