import socket
import pickle
from const import ADDR, BUF


class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        try:
            self.player = int(self.client.recv(BUF).decode())
        except:
            print("CONNECTION ERROR")

    def send(self, data: str):
        try:
            self.client.send(data.encode())
            return pickle.loads(self.client.recv(BUF))
        except socket.error:
            print("SEND ERROR")
