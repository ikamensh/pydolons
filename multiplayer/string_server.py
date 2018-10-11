import socket
from threading import Thread
import pickle
import sys

from multiplayer.config import host, port, MyDatagram
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent

class MyServer:
    def __init__(self):

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)

        self.active_clients = []
        self.socket_names = {}
        self.ctr = 1

        # self.history = None

    def listen(self):
        print("listening.")
        while True:

            (sock, address) = self.serversocket.accept()
            print("new connection!")

            self.active_clients.append(sock)
            self.socket_names[sock] = f"Player {self.ctr}"
            self.ctr += 1
            sock.send(bytes(self.socket_names[sock], encoding="utf-8") )

            ct = Thread(target=MyServer.client_thread, args=(self,sock))
            ct.start()

    def update_all(self, data):
        data_string = pickle.dumps(data)
        for sock in list(self.active_clients):
            try:
                sock.send(data_string)
            except OSError as e:
                print(self.socket_names[sock], "has disconnected")
                self.active_clients.remove(sock)


    def client_thread(self, clientsocket):
        while True:
            data = clientsocket.recv(4096)
            print("bytes actually recieved: ", sys.getsizeof(data))
            data_variable = pickle.loads(data)
            # self.history = data_variable
            self.update_all(data_variable)

if __name__ == "__main__":
    my_server = MyServer()
    my_server.listen()


