import socket
from time import sleep

class MyClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self):
        self.socket.connect(("localhost", 5678))

    def myreceive(self):

        history = self.socket.recv(2048).decode("utf-8", "strict")
        print("current history is:", history)

    def send(self, new_chunk):

        self.socket.send(bytes(new_chunk, encoding="utf-8"))

    def send_and_update(self, new_chunk):
        self.send(new_chunk)
        self.myreceive()



my_client = MyClient()
my_client.connect()
while True:
    string = input()
    my_client.send_and_update(string)

