import pickle
import socket
import sys

from multiplayer.events.ClientOrderRecievedEvent import ClientOrderRecievedEvent
from multiplayer.events.ClientOrderIssuedEvent import ClientOrderIssuedEvent
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent
from multiplayer.network.config import host, port


class ClientSocket:
    def __init__(self, game):
        self.game = game
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.next_order = 1
        self.orders_stored = {}

    def connect(self):
        self.socket.connect((host, port))
        name = self.socket.recv(2048).decode("utf-8", "strict")
        self.name = name
        print(f"Connected as {self.name}")

    def myreceive(self):
        while True:
            data = self.socket.recv(4096)
            print("bytes actually recieved: ", sys.getsizeof(data))
            e: ServerOrderIssuedEvent = pickle.loads(data)
            assert isinstance(e, ServerOrderIssuedEvent)

            if self.next_order != e.uid:
                self.orders_stored[e.uid] = e
            else:
                ClientOrderRecievedEvent(
                    self.game, e.unit_uid, e.active_uid, e.target)
                self.next_order += 1
                while self.next_order in self.orders_stored:
                    e = self.orders_stored[self.next_order]
                    ClientOrderRecievedEvent(
                        e.unit_uid, e.active_uid, e.target)
                    self.next_order += 1

    def send(self, e: ClientOrderRecievedEvent):
        e.game = None
        data_string = pickle.dumps(e)
        self.socket.send(data_string)
