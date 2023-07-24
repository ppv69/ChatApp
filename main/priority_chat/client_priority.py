# Import the required socket module
import socket

# Server configuration
SERVER_HOST = 'IP'  # Replace with the IP address of the server
SERVER_PORT = 12347  # Replace with the port number used by the server
BUFFER_SIZE = 1024  # Size of the buffer for receiving data

def set_priority():
    # Function to prompt the user for priority selection
    while True:
        try:
            priority = int(input("Enter priority (1 for low, 2 for high): "))
            if priority in [1, 2]:
                return priority
            print("Invalid priority. Please enter 1 for low or 2 for high.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def send_message(client_socket, message):
    # Function to send a message to the server
    client_socket.send(message.encode('utf-8'))

if __name__ == "__main__":
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Set the client's priority
    priority = set_priority()
    client_socket.send(str(priority).encode('utf-8'))

    while True:
        # Prompt the user to enter a message
        message = input("Enter your message (type 'exit' to quit): ")

        # Check if the user wants to exit
        if message.lower() == 'exit':
            break

        # Send the message to the server
        send_message(client_socket, message)

    # Close the client socket when done
    client_socket.close()
