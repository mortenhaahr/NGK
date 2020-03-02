#!/usr/bin/env python

#Help: https://pythontic.com/modules/socket/udp-client-server-example

import sys
from socket import *
from lib import Lib

PORT = 9000
BUFSIZE = 1024

def main(argv):
	host = sys.argv[1]
	sendMsg = sys.argv[2]

	# Create a UDP socket
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	server_address = (host, PORT)

	clientSocket.sendto(sendMsg, server_address)

	fromServer = clientSocket.recvfrom(BUFSIZE)

	rcvMsg = "From Server: {}".format(fromServer[0])

	print rcvMsg

if __name__ == "__main__":
   main(sys.argv[1:])
