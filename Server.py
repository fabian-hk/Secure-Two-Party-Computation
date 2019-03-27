import argparse

from tools.server import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for the Fpre function and the client to client communication.')
    parser.add_argument('-p', '--port', type=int, default=8448,
                        help='Port to listen on for in coming connections (default 8448).')
    args = parser.parse_args()

    server = Server(args.port)
    server.start_server()
