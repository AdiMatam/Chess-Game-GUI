import socket
import pickle
from chs_const import ADDR, BUF


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(ADDR)
            return int(self.client.recv(BUF).decode())
        except:
            print("CONNECTION ERROR")

    def send(self, data: str):
        try:
            self.client.send(data.encode())
            return pickle.loads(self.client.recv(BUF))
        except socket.error:
            print("SEND ERROR")
