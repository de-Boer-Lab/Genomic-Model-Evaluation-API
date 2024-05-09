import socket
import json
import numpy as np
#read in JSON file here

evaluator_file = open('/Users/ishika/Desktop/API/Genomic-Model-Evaluation-API/examples/sampleRequest1/evaluator_message.json')

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "127.0.0.1"  # replace with the server's IP address
    server_port = 8000  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))

    while True:
        # input message and send it to the server
        #msg = input("Enter message: ")
        #send the evaluator json
        client.send(jsonResult.encode("utf-8")[:1024])
        #client.send(jsonResult)
        # receive message from the server
        response = client.recv(1024)
        #response = response.decode("utf-8")

        # if server sent us "closed" in the payload, we break out of the loop and close our socket
        if response.lower() == "closed":
            break

        #print("Received: {response}")
        print(response)

    # close client socket (connection to the server)
    client.close()
    print("Connection to server closed")

run_client()
