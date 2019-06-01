import socket
from multiprocessing import Process
import ssl
import select

from fpre.fpre_server import FpreServer
from conf import conf
from conf import cert_conf


class Server(Process):

    def __init__(self, port, no_encryption=False):
        super().__init__()
        #        while(True):
        #            pass
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)

        if not no_encryption:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(cert_conf.server_certificate, cert_conf.server_priv_key)
            context.load_verify_locations(cert_conf.root_cert)
            context.verify_mode = ssl.CERT_REQUIRED
            self.s = context.wrap_socket(s, server_side=True)
        else:
            self.s = s

        self.ex_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.ex_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ex_s.bind(('', port + 1))
        self.ex_s.listen(5)

    def start_server(self):
        """
        Runs server in the same process as it was instantiated.
        """
        while True:
            print("Waiting for connection")

            try:
                conn1, addr1 = self.s.accept()
                print("First connection. IP: " + str(addr1))

                conn2, addr2 = self.s.accept()
                print("Second connection. IP: " + str(addr2))

                conn = Connection(conn1, conn2)
                conn.start()

                conn3, addr3 = self.ex_s.accept()
                print("Third connection. IP: " + str(addr3))

                conn4, addr4 = self.ex_s.accept()
                print("Fourth connection. IP: " + str(addr4))

                print()

                ex = Exchange(conn3, conn4)
                ex.start()

                conn.join()
                ex.join()
            except OSError:
                print("Error: SSL handshake failed")

    def run(self):
        """
        Runs server in a new process.
        """
        self.start_server()


class Exchange(Process):
    BUFFER_SIZE = 4096

    def __init__(self, conn1, conn2):
        super().__init__()
        self.conn1 = conn1
        self.conn2 = conn2
        self.conn1.setblocking(0)
        self.conn2.setblocking(0)

        self.receive_buffer = bytes(0)

    def run(self):
        run = True
        while run:
            readable_s, _, _ = select.select([self.conn1, self.conn2], [], [])

            for sock in readable_s:
                try:
                    data = sock.recv(self.BUFFER_SIZE)
                except ConnectionResetError:
                    run = False
                    break
                if data != b'\xfe':
                    if sock == self.conn1:
                        try:
                            self.conn2.sendall(data)
                        except ConnectionResetError:
                            run = False
                            break
                    elif sock == self.conn2:
                        try:
                            self.conn1.sendall(data)
                        except ConnectionResetError:
                            run = False
                            break
                else:
                    run = False
                    break

        self.conn1.close()
        self.conn2.close()


class Connection(Process):
    BUFFER_SIZE = 2048

    def __init__(self, conn1: socket, conn2: socket):
        super().__init__()

        self.conn1 = conn1
        self.conn2 = conn2

        self.receive_buffer = bytes(0)

        self.fpre_server = FpreServer()

    def receive(self, conn):
        data = self.receive_buffer
        if len(self.receive_buffer) >= 4:
            length = int.from_bytes(data[:4], byteorder='big')
        else:
            data += conn.recv(self.BUFFER_SIZE)
            length = int.from_bytes(data[:4], byteorder='big')
        data = data[4:]
        while len(data) < length:
            data += conn.recv(self.BUFFER_SIZE)
        self.receive_buffer = data[length:]
        return data[:length]

    def send_data(self, conn, data):
        conn.sendall((len(data).to_bytes(4, byteorder='big') + data))

    def run(self):
        # initialize connection with the appropriate persons
        self.send_data(self.conn1, b'\x00\x00')
        self.send_data(self.conn2, b'\x00\x01')

        run = True
        while run:
            data_A = self.receive(self.conn1)
            if not data_A:
                continue

            if data_A[0:1] == b'\x01':
                delta_b = self.fpre_server.init(data_A[1:])
                self.send_data(self.conn2, b'\x01' + delta_b)
                self.send_data(self.conn1, b'\x01')
            elif data_A[0:1] == b'\x02':
                ser_auth_bits_b = self.fpre_server.create_auth_bits(data_A[1:])
                self.send_data(self.conn2, b'\x02' + ser_auth_bits_b)
                self.send_data(self.conn1, b'\x02')
            elif data_A == b'\xfe':
                self.conn1.shutdown(socket.SHUT_RDWR)
                self.conn1.close()
                self.conn2.shutdown(socket.SHUT_RDWR)
                self.conn2.close()
                run = False


if __name__ == "__main__":
    server = Server(conf.test_server_port)
    server.start_server()
