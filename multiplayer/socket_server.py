import socket
from threading import Thread
import pickle
import sys

from multiplayer.config import host, port, MyDatagram
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent
from multiplayer.events.ServerOrderReceivedEvent import ServerOrderRecievedEvent

class MyServer:
    def __init__(self, fractions_for_players):

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)

        self.active_clients = []
        self.free_fractions = list(fractions_for_players)
        self.socket_fractions = {}

        # self.history = None

    def listen(self):
        print("listening.")
        while True:

            (sock, address) = self.serversocket.accept()
            print("new connection!")

            self.active_clients.append(sock)
            fraction = self.free_fractions[0]
            self.socket_fractions[sock] = fraction
            sock.send(bytes(str(fraction), encoding="utf-8"))

            self.free_fractions.remove(fraction)
            ct = Thread(target=MyServer.client_thread, args=(self,sock))
            ct.start()

    def update_all(self, data):
        data_string = pickle.dumps(data)
        for sock in list(self.active_clients):
            try:
                sock.send(data_string)
            except OSError as e:
                print(self.socket_fractions[sock], "has disconnected")
                self.active_clients.remove(sock)
                self.free_fractions.append(self.socket_fractions[sock])


    def client_thread(self, clientsocket):
        while True:
            data = clientsocket.recv(4096)
            print("bytes actually recieved: ", sys.getsizeof(data))
            e = pickle.loads(data)
            assert isinstance(e, ClientOrderIssuedEvent)
            ServerOrderRecievedEvent(self.socket_fractions[clientsocket],
                                     e.unit_uid, e.active_uid, e.target)

if __name__ == "__main__":
    my_server = MyServer(["abra"])
    th = Thread(target=my_server.listen)
    th.start()
    # my_server.listen()


