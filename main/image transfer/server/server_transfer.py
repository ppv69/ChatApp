import socket
import sys
import zipfile
import os

# Port number for the server to listen on
port = 1337

# Create a socket object for the server
ss = socket.socket()
# Print message to indicate that the server socket is created.
print('[+] Server socket is created.')

# Bind the socket to the specified port on any available network interface
ss.bind(('', port))
# Print message to indicate that the socket is binded to the specified port.
print('[+] Socket is binded to {}'.format(port))

# Set the server to listen for incoming connections
ss.listen(5) #server listens to 5 clients
# Print message to indicate that the server is waiting for connections.
print('[+] Waiting for connection...')

# Accept incoming connection and get the connection object and the client address
con, addr = ss.accept()
# Print message to indicate that the server got a connection from the client.
print('[+] Got connection from {}'.format(addr[0]))

# Receive the filename of the incoming zip file from the client
filename = con.recv(1024).decode()

# Open a new file with the received filename in binary write mode
f = open(filename, 'wb')

# Receive data in chunks (1024 bytes) and write to the file until no more data is received
l = con.recv(1024) #l is a temp file used to store recieved data
while(l):
    f.write(l)
    l = con.recv(1024)

# Close the file after receiving the entire data
f.close()
# Print message to indicate that the server received the file successfully.
print('[+] Received file ' + filename)

# Extract the files from the received zip archive
with zipfile.ZipFile(filename, 'r') as file:
    # Print message to indicate that the server is extracting files from the zip archive.
    print('[+] Extracting files...')
    file.extractall()
    # Print message to indicate that the extraction is done.
    print('[+] Done')

# Remove the received zip file from the server's storage
os.remove(filename)

# Close the client connection
con.close()
# Close the server socket
ss.close()
