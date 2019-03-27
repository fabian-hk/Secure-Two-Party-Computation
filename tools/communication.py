import socket
import sys

from tools.person import Person


class Com:
    TCP_IP = 'localhost'
    TCP_PORT = 8448
    BUFFER_SIZE = 2048

    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((ip, port))
        data = self.receive()
        if data[0:1] == b'\x00':
            self.person = Person(data[1])
        else:
            sys.exit(1)
        self.id = 0
        print("Connection successful")

    def receive(self):
        data = bytes(0)
        while True:
            part = self.s.recv(self.BUFFER_SIZE)
            data += part
            if len(part) < self.BUFFER_SIZE:
                break
        return data

    def exchange_data(self, data=bytes(1)):
        print("Com class: send data length: " + str(len(data)))
        self.s.sendall(b'\xfd' + self.id.to_bytes(1, "big") + data)
        d = self.receive()
        print("Com class: receive data length: " + str(len(d)))
        if d[0] == self.id:
            self.id += 1
            return d[1:]
        else:
            print("Com class error ID not equal")

    def close_session(self):
        self.s.sendall(b'\xfe')
        self.s.close()
