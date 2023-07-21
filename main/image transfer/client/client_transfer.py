import socket
import sys
import zipfile
import os

# Define the host and port for the socket connection
host = '127.0.0.1'
port = 1337

# Number of image files to include in the zip archive
k = 3

# Name of the zip file to be created
zip_name = 'main.zip'

# Create a socket object
s = socket.socket()
# Print message to indicate that the client socket is created.
print('[+] Client socket is created.')

# Connect the socket to the specified host and port
s.connect((host, port))
# Print message to indicate that the socket is connected to the host.
print('[+] Socket is connected to {}'.format(host))

# Create a zip file with the specified name and write image files into it
with zipfile.ZipFile(zip_name, 'w') as file:
    for j in range(1, (k + 1)):
        file.write('{}.jpg'.format(j))
        # Print a message for each image file that is added to the zip archive.
        print('[+] {}.jpg is sent'.format(j))

# Send the name of the zip file to the server
s.send(zip_name.encode())

# Open the zip file in binary read mode
f = open(zip_name, 'rb')
# Read the contents of the zip file
l = f.read()
# Send the entire contents of the zip file over the socket connection
s.sendall(l)

# Remove the zip file after it has been sent
os.remove(zip_name)
# Close the file object
f.close()
# Close the socket connection
s.close()
