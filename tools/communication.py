import socket
import sys
import ssl

from tools.person import Person
import conf


class Com:
    BUFFER_SIZE = 2048

    def __init__(self, ip, port):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations(conf.crt_storage+'ca-root.pem')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s = context.wrap_socket(s, server_hostname='127.0.0.1')
        self.s.connect((ip, port))

        self.receive_buffer = bytes(0)

        data = self.receive()
        if data[0:1] == b'\x00':
            self.person = Person(data[1])
        else:
            sys.exit(1)
        self.id = 0
        print("Connection successful "+str(self.s.version()))

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
