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
			sentence = Lib.readTextTCP(connectionSocket)
			print "Client beder om: ", sentence
			file_name = Lib.extractFilename(sentence)
			print "Filnavn: ", file_name
			file_size = Lib.check_File_Exists(sentence)

			if file_size !=0:
				print "Filen findes!"
				print "Filen fylder: ", file_size

				Lib.writeTextTCP(str(file_size), connectionSocket)

				sendFile(sentence, file_size, connectionSocket)
				print "Filen er sendt!"

			else:
				print "Kuk kuk - tom fil eller er den bare tom?"
				Lib.writeTextTCP("Ingen fil..", connectionSocket)

			connectionSocket.close()
			print "Disconnected from", address

	finally:
	    serverSocket.close()

def sendFile(fileName,  fileSize,  conn):
	# TO DO Your Code
	Lib.writeTextTCP("Sender Fil...", conn)
	filepoint = 1
	file = open(fileName, 'rb')
	sizeLeft = fileSize

	while(sizeLeft > 0):
		if sizeLeft < BUFSIZE:
			Lib.writeTextTCP(str(sizeLeft),conn)
			filepoint = file.read(sizeLeft)
		
		else:
			Lib.writeTextTCP(str(BUFSIZE), conn)
			filepoint = file.read(BUFSIZE)
		
		print "Sender...."
		conn.send(filepoint)
		sizeLeft = sizeLeft - BUFSIZE
	
	Lib.writeTextTCP('0',conn)
	file.close()

if __name__ == "__main__":
	main(sys.argv[1:])