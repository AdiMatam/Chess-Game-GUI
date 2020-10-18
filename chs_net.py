import socket
import pickle
from chs_const import ADDR, BUF


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)
        self.player = self.initial()

    def initial(self):
        try:
            return int(self.client.recv(BUF).decode())
        except Exception as e:
            print("CONNECTION ERROR")

    def send(self, data: str):
        try:
            self.client.send(data.encode())
            return pickle.loads(self.client.recv(BUF))
        except socket.error:
            print("SEND ERROR")
