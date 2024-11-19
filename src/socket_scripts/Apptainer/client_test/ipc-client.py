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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Connect to the same host/post as the server
    s.connect((host, port))
    #send test message
    s.sendall(b'Hello, connection successful!')
    s.close()
