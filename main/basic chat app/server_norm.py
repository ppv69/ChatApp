import socket
import threading

# Server configuration
HOST = '192.168.29.189'  # Listen on all available IPv6 and IPv4 interfaces
PORT = 12347
BUFFER_SIZE = 1024

# Create a socket with dual-stack support (IPv4 and IPv6)
server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# List to keep track of connected clients
client_sockets = []

print("Server is listening on [{}]:{}".format(HOST, PORT))

def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            if not message:
                break
            print("Received from {}: {}".format(client_address, message))
            if message.strip() == 'Bye':
                client_socket.send("Goodbye".encode('utf-8'))  # Send acknowledgment to the client
                break
    except socket.error:
        pass
    finally:
        client_socket.close()
        print("Client {} disconnected.".format(client_address))

try:
    while True:
        # Accept client connections
        client_socket, client_address = server_socket.accept()
        client_sockets.append(client_socket)
        print("New client connected: {}".format(client_address))

        # Start a thread to handle the client's messages
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    # Cleanup when the server is terminated with Ctrl+C
    for client_socket in client_sockets:
        client_socket.close()
    server_socket.close()
    print("\nServer is shutting down.")