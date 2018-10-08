# SocketDemo.py
# Code for messing around with sockets in Python to enable communication
# between Android app and the simulation

# CHANGE LOG
# Date       Name       Changes
# -------------------------------------------------------------------------
# 11/13/16   Libbey     File creation
# -------------------------------------------------------------------------

from socket import *
from sys import *
from thread import *

def receive_data(connection):
	while 1:
		data = connection.recv(1024)
		if not data:
			break
		print (data)

	connection.close()

def main():
	HOST = ''
	PORT = 8888

	s = socket(AF_INET, SOCK_STREAM)
	print('Socket created')

	#Bind socket to local host and port
	try:
	    s.bind((HOST, PORT))
	except error as msg:
	    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	    exit()

	print ('Socket bind complete')

	#Start listening on socket
	s.listen(10)
	print ('Socket now listening')

	#now keep talking with the client
	while 1:
	    #wait to accept a connection - blocking call
	    conn, addr = s.accept()
	    print ('Connected with ' + addr[0] + ':' + str(addr[1]))

	    start_new_thread(receive_data, (conn,))

	s.close()

if __name__ == '__main__':
    main()