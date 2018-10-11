import socket
from time import sleep
from threading import Thread

class MyServer:
    def __init__(self):

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind(("localhost", 5678))
        self.serversocket.listen(5)

        self.history = ""

    def listen(self):
        print("listening.")
        while True:

            (clientsocket, address) = self.serversocket.accept()
            print("new connection!")
            ct = Thread(target=MyServer.client_thread, args=(self,clientsocket))
            ct.start()

    def client_thread(self, clientsocket):
        while True:
            new_chunk = clientsocket.recv(2048).decode("utf-8", "strict")
            self.history += new_chunk
            clientsocket.send(bytes(self.history, encoding="utf-8"))
            sleep(1)

my_server = MyServer()
my_server.listen()


