host = 'localhost'
port = 43210

class MyDatagram:
    def __init__(self,a,b,c):
        self.abc = a,b,c

    def __repr__(self):
        return f"Datagram: {self.abc}"

