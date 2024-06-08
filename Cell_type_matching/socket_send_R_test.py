#!/usr/bin/env python3
# ipc_client.py

# import socket
#
# HOST = socket.gethostbyname('test_network')
# PORT = 8000        # The port used by the server
#
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world. IPC success!')
#     data = s.recv(1024)
#
# print('Received', repr(data))

import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 6013))
while 1:
    #data = raw_input( "Enter text to be upper-cased, q to quit\n" )
    #data = "HI R script"
    client_socket.send(b'Hello, world. IPC success!')
    if ( data == 'q' or data == 'Q'):
        client_socket.close()
        break;
    else:
        data = client_socket.recv(5000)
        print("Your upper cased text:  " , data)
