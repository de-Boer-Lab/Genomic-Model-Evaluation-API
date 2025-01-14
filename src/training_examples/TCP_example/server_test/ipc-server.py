#Basic client-server TCP test scripts
import socket
import argparse
#pass in host/port
#need to use unrestricted ports
parser = argparse.ArgumentParser(description='Socket Test')
parser.add_argument('--host', action="store", dest="host",required=True, help='ip address')
parser.add_argument('--port', action="store", dest="port", type=int,required=True, help='port')

given_args = parser.parse_args()
host = given_args.host
port = given_args.port
#The server is started first and is listening
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        while True:
            #receieve message from client
            data = conn.recv(1024)
            print(data)
            if not data:
                break
                conn.close()
