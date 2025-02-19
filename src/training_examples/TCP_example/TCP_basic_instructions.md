### Basic instructions to test TCP sockets

The only dependencies are any version of Python 3.

The server and client communicate with each other using a HOST:PORT connection in python scripts. The HOST and PORT need to be the same for the server and client. The HOST can be any IP address and PORT above 1024 are usually free to use on computers/servers.

Download both `/client_test` and `/server_test` folders

Instructions:

1. Get local HOST: 

On mac: `ifconfig | grep inet`
On windows: `ipconfig`

Use that IP address in the HOST argument below.

2. Open 2 separate terminals/sessions

3.`cd server_test`. The server needs to be started first to open the connection: `python3 ipc-server.py --host HOST --port PORT`

ex. `python3 ipc-server.py --host 127.0.0.1 --port 8080`

4. `cd client_test`. Next start the client which will send a message to the server: `python3 ipc-client.py --host HOST --port PORT`

ex. `python3 ipc-client.py --host 127.0.0.1 --port 8080`

5. If successful you will see the message `b'Hello, connection successful!'` on the Server side. 



