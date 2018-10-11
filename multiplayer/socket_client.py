import socket
import sys
import pickle
import time
from threading import Thread

from multiplayer.config import host, port, MyDatagram
from multiplayer.events.ClientOrderRecievedEvent import ClientOrderRecievedEvent
from multiplayer.events.ServerOrderIssuedEvent import ServerOrderIssuedEvent


class MyClient:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.next_order = 1
        self.orders_stored = {}



    def connect(self):
        self.socket.connect((host,port))
        name = self.socket.recv(2048).decode("utf-8", "strict")
        self.name = name
        print(f"Connected as {self.name}")

    def myreceive(self):
        while True:
            data = self.socket.recv(4096)
            print("bytes actually recieved: ", sys.getsizeof(data))
            e = pickle.loads(data)
            assert isinstance(e, ServerOrderIssuedEvent)

            if self.next_order != e.uid:
                self.orders_stored[e.uid] = e
            else:
                ClientOrderRecievedEvent(e.unit_uid, e.active_uid, e.target)
                self.next_order += 1
                while self.next_order in self.orders_stored:
                    e = self.orders_stored[self.next_order]
                    ClientOrderRecievedEvent(e.unit_uid, e.active_uid, e.target)
                    self.next_order += 1


    def send(self, new_chunk):
        data_string = pickle.dumps(new_chunk)
        self.socket.send(data_string)


if __name__ == "__main__":

    my_client = MyClient()
    my_client.connect()

    ct = Thread(target=my_client.myreceive)
    ct.start()

    ctr = 1
    while True:
        ctr += 10
        my_client.send(MyDatagram(my_client.name, ctr, ctr+5))
        time.sleep(10)

