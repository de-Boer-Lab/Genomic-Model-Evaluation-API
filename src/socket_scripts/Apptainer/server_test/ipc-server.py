import socket

#HOST = socket.gethostbyname('test_network')  # Standard loopback interface address (localhost)
PORT = 8021       # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('172.16.47.244', PORT))
    s.listen()
    conn, addr = s.accept()

    cell_type_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cell_type_socket.connect(('172.16.47.244', 8020))

    cell_type_socket.sendall(b'Hello, cell type matcher dude!')
    data_cell = cell_type_socket.recv(1024)
    print(data_cell)
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)
