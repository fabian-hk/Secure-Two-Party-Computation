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

        self.receive_buffer = bytes(0)

        data = self.receive()
        if data[0:1] == b'\x00':
            self.person = Person(data[1])
        else:
            sys.exit(1)
        self.id = 0
        print("Connection successful")

    def receive(self):
        data = self.receive_buffer
        data += self.s.recv(self.BUFFER_SIZE)
        length = int.from_bytes(data[:4], byteorder='big')
        data = data[4:]
        while len(data) < length:
            data += self.s.recv(self.BUFFER_SIZE)
        self.receive_buffer = data[length:]
        return data[:length]

    def send_data(self, data):
        self.s.sendall((len(data).to_bytes(4, byteorder='big') + data))

    def exchange_data(self, data=bytes(1)):
        self.send_data(b'\xfd' + self.id.to_bytes(4, "big") + data)
        d = self.receive()
        if int.from_bytes(d[:4], byteorder='big') == self.id:
            self.id += 1
            return d[4:]
        else:
            print("Com class error ID not equal")

    def close_session(self):
        self.send_data(b'\xfe')
        self.s.close()
