#!/usr/bin/env python3

import sys
from socket import *
from lib import Lib

PORT = 9000
BUFSIZE = 1000

def main(argv):
	# TO DO Your Code
	host = sys.argv[1]
	file = sys.argv[2]
	# Create a TCP/IP socket
	clientSocket = socket(AF_INET, SOCK_STREAM)
	server_address = (host, PORT)
	clientSocket.connect(server_address)

	#clientSocket.sendall(msg)
	Lib.writeTextTCP(file,clientSocket)
	msg = Lib.readTextTCP(clientSocket)
	print msg
	#sentence = raw_input('input lowercase sentence:')
	#clientSocket.send(sentence.encode())
	#modifiedSentence = clientSocket.recv(1024)


def receiveFile(fileName,  conn):
	# TO DO Your Code
	print("receiveFile")

if __name__ == "__main__":
   main(sys.argv[1:])
