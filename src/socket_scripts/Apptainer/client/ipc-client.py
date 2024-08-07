#!/usr/bin/env python3
# ipc_client.py

import socket

#HOST = socket.gethostbyname(''127.0.0.1'')
PORT = 8015        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('172.16.47.244', PORT))
    evaluator_file = open('/arc/project/st-cdeboer-1/iluthra/API_genomic_model_evaluation/sample_jsons/evaluator_message.json')
    print(evaluator_file)
    s.sendall(b'Hello, world. IPC success!')
    data = s.recv(1024)

print('Received', repr(data))
