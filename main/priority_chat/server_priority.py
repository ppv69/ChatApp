import socket
import threading
import queue
import time

# Dictionary to store connected clients and their priorities
clients = {}  # Dictionary to hold client sockets and their corresponding priorities

# Server configuration
SERVER_HOST = 'IP'  # Replace with the server's IP address
SERVER_PORT = 12347  # Replace with the server's port number
BUFFER_SIZE = 1024  # Size of the buffer for receiving data

# Priority levels
LOW_PRIORITY = 1
HIGH_PRIORITY = 2

# Message queues
message_queues = {LOW_PRIORITY: queue.Queue(), HIGH_PRIORITY: queue.Queue()}  # Separate queues for high and low priority messages

def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE).decode('utf-8')  # Receive the message from the client
            if not message:
                break
            # Get the client's priority from the dictionary
            priority = clients[client_socket]
            # Add the received message to the corresponding queue based on priority
            message_queues[priority].put(message)
            # Wait until both high and low priority messages are received before processing
            if not message_queues[LOW_PRIORITY].empty() and not message_queues[HIGH_PRIORITY].empty():
                process_messages()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        client_socket.close()
        # Remove the client from the dictionary when the connection is closed
        if client_socket in clients:
            del clients[client_socket]

def process_messages():
    low_priority_msg = message_queues[LOW_PRIORITY].get()  # Get the low priority message from the queue
    high_priority_msg = message_queues[HIGH_PRIORITY].get()  # Get the high priority message from the queue
    # Simulate processing time for the messages
    time.sleep(2)
    print(f"Processed message with priority {HIGH_PRIORITY}: {high_priority_msg}")
    print(f"Processed message with priority {LOW_PRIORITY}: {low_priority_msg}")

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print("Server listening on {}:{}".format(SERVER_HOST, SERVER_PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        client_priority = int(client_socket.recv(BUFFER_SIZE).decode('utf-8'))  # Receive the client's priority
        clients[client_socket] = client_priority  # Store the client socket and its priority in the dictionary
        print(f"New client connected from {client_address} with priority {client_priority}")
        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
