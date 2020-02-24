#!/usr/bin/env python

# Help: https://pymotw.com/2/socket/tcp.html
# Help: https://www.bogotobogo.com/python/python_network_programming_server_client_file_transfer.php

import sys
from socket import *
from lib import Lib


HOST = '10.0.0.1'
PORT = 9000
BUFSIZE = 1000


def main(argv):
	# TO DO Your Code

	# Create a TCP/IP socket
	serverSocket = socket(AF_INET,SOCK_STREAM)

	# Bind the socket to the port
	server_address = (HOST, PORT)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
	serverSocket.bind(server_address)
	
	# Listen for incoming connections
	serverSocket.listen(1)
	
	print("Server are ready to recieve")

	# loop waiting for connections (terminate with Ctrl-C)
	try:
		while True:
			connectionSocket, address = serverSocket.accept()
			print "Connected from", address
			# loop serving the new client
			# sentence = connectionSocket.recv(100).decode() [Next line is function from lib.py - read whole string]

			sentence = Lib.readTextTCP(connectionSocket)
			print "Client beder om: ", sentence

			file_name = Lib.extractFilename(sentence)


			file_size = Lib.check_File_Exists(file_name)
			print "Filen findes da!"
			print "Filen fylder: ", file_size

			if file_size !=0:
				sendFile(file_name, file_size, connectionSocket)

				Lib.writeTextTCP("Filen er sendt du!", connectionSocket)
				print "Filen er sendt!"

			else:
				print "Kuk kuk lille fil eller er den bare tom?"

				Lib.writeTextTCP("Ingen fil..", connectionSocket)

			connectionSocket.close()
			print "Disconnected from", address

	finally:
	    serverSocket.close()

def sendFile(fileName,  fileSize,  conn):
	# TO DO Your Code
	Lib.writeTextTCP("Sender Fil...", conn)
	
	file = open(fileName, 'rb')
	filepoint = file.read(BUFSIZE)

	while(filepoint):
		conn.send(filepoint)
		filepoint = file.read(BUFSIZE)
		print "Sender...."
	file.close()


   
if __name__ == "__main__":
	main(sys.argv[1:])