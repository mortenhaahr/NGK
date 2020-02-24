#!/usr/bin/env python

import sys
from socket import *
from lib import Lib

PORT = 9000
BUFSIZE = 1000

def main(argv):
	host = sys.argv[1]
	file = sys.argv[2]

	# Create a TCP/IP socket
	clientSocket = socket(AF_INET, SOCK_STREAM)
	server_address = (host, PORT)
	clientSocket.connect(server_address)

	fileName = Lib.extractFilename(file)
	
	Lib.writeTextTCP(file,clientSocket)

	fileSize = Lib.readTextTCP(clientSocket)
	fileSize = int(fileSize)
	print fileSize

	msg = Lib.readTextTCP(clientSocket)
	if msg == "Sender Fil...":
		receiveFile(fileName, fileSize, clientSocket)
	else:
		print "Fejl 40 -", msg

	clientSocket.close()

def receiveFile(fileName, size, conn):
	recievedData = 0
	with open(fileName, 'wb') as file:
		print "RECEIVING - File lader sig fylde af dejlig data."
		
		while True:
			modtag = Lib.readTextTCP(conn)
			if modtag == '0':
				break
			recievedData = recievedData + int(modtag)
			print "Modtaget:", recievedData, "B /", size, "B"
			data = conn.recv(int(modtag))
			file.write(data)
	
	file.close()
	print "COMPLETE - Filen er fyldt af modtaget data og derfor lukket."

if __name__ == "__main__":
   main(sys.argv[1:])
