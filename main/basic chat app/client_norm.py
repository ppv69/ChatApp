import socket
import threading
import os

# Client configuration
SERVER_IP = '192.168.29.189'  # Server's IPv4 address 
SERVER_PORT = 12347
BUFFER_SIZE = 1024

def receive_messages():
    while True:
        message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(message)

def send_messages():
    username = input("Enter your username: ")
    client_socket.send(f"username {username}".encode('utf-8'))
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.strip() == 'Bye':
            break
        elif message.strip() == 'img_transfer':
            files = [file for file in os.listdir('.') if file.endswith('.jpg')]
            for file in files:
                with open(file, 'rb') as f:
                    data = f.read()
                    client_socket.send(data)
        elif message.strip().split()[0] == 'block':
            client_socket.send(message.encode('utf-8'))

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    # Receive and send messages using threads
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages)
    send_thread.start()

    receive_thread.join()
    send_thread.join()

except KeyboardInterrupt:
    pass

client_socket.close()
