#!/usr/bin/env python

import sys
from socket import *
from lib import Lib

HOST = '10.0.0.1'
PORT = 9000
BUFSIZE = 1024

def main(argv):
	
	# Create a UDP socket
	serverSocket = socket(AF_INET,SOCK_DGRAM)

	# Bind the socket to the port
	server_address = (HOST, PORT)
	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
	serverSocket.bind(server_address)
	
	print("Server are ready to recieve")

	# loop waiting for connections (terminate with Ctrl-C)
	while True:
		recievedMessage = serverSocket.recvfrom(BUFSIZE)
		ClientMessage = recievedMessage[0]
		ClientAddress = recievedMessage[1]

		print ClientMessage 
		print ClientAddress  
		if ClientMessage == 'U' or ClientMessage == 'u':
			file = open("/proc/uptime", 'rb')
			content = file.read()
			contentList = content.split()
			sendMsg = "Uptime: " + contentList[0] + " Idle: " + contentList[1]
			print sendMsg
			serverSocket.sendto(sendMsg, ClientAddress)
		elif ClientMessage == 'L' or ClientMessage == 'l':
			file = open("/proc/loadavg", 'rb')
			content = file.read()
			contentList = content.split()
			content1 = "CPU 1 minute: " + contentList[0] + "%\n"
			content2 = "CPU 5 minutes: " + contentList[1] + "%\n"
			content3 = "CPU 15 minutes: " + contentList[2] + "%\n"
			content4 = "Processes in use: " + contentList[3] + "\n"
			content5 = "Last process ID: " + contentList[4]

			sendMsg = content1 + content2 + content3 + content4 + content5
			print sendMsg
			serverSocket.sendto(sendMsg, ClientAddress)
		else: 
			serverSocket.sendto('404 - Not Found', ClientAddress)
			
		#sendFile(sentence, file_size, connectionSocket)

if __name__ == "__main__":
	main(sys.argv[1:])