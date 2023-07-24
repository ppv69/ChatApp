import socket
import threading

# Client configuration
SERVER_IP = 'IP'  # Server's IPv4 address (localhost)
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

def receive_messages():
    while True:
        message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print("Received from server:", message)
        if message.strip() == 'Goodbye':
            break

try:
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.strip() == 'Bye':
            break

    receive_thread.join()

except KeyboardInterrupt:
    pass

client_socket.close()
