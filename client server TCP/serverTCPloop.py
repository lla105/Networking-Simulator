import sys
import random
print (sys.version)
from socket import *
serverHost = ''
serverPort = 50007
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(( serverHost, serverPort))
serverSocket.listen(1)

random_one = random.random()
# random_one < packet lost prob, then it's lost
# if packet lost prob <= random_one < packet corrupt, 
#  then it's corrupt
seedTiming = int(input("1)Define seedTiming [2,32000]: ") )
if seedTiming<2 or seedTiming>32000: seedTiming = 555

packCorrupt = float(input("2)Define packCorrupt [0,1): "))
if packCorrupt<0 or packCorrupt>=1: packCorrupt = 0.001

packLost = float(input("3)Define packLost [0,packCorrupt): "))
if packLost<0 or packLost>=packCorrupt: packLost = 0.0005

field_two = 0 #state of server
field_one = "" #waiting to be received
sequence_number = 999
packet_array=[0,0,True]
print ( 'The server is ready to receive ' )

while True:
	is_corrupt = False
	connectionID, addr = serverSocket.accept()
	print ("The server connected to: " + str(addr) )
	while True:
		print("~~~~RECEIVER STATE NOW: " + str(field_two))#!!
		sentence = connectionID.recv(1024).decode()

		for i in range(len(sentence)):
			if sentence[i] == " ":
				break
			else:
				field_one=field_one+sentence[i]

		for i in range(len(sentence)):
			if sentence[i] == " ":
				sequence_number = sentence[i+1]
				#print("field two is: " + str(sequence_number))
				break

		#"print msg IMMEDIATELY after pkt received"
		if packLost<=random_one and random_one<packCorrupt:
			print("A Corrupted packet has just been received")
			is_corrupt = True
		elif random_one<packLost:
			print("A packet has been lost")
		else:
			if str(field_two) == str(sequence_number):
				print("A packet with sequence number "+str(sequence_number)
				+"has been received")
				print("Packet received contains: data "+str(field_one)
				+" seq = "+str(sequence_number)+" isack = FALSE")
			else:
				print("Aduplicate packet with sequence number "
				+str(sequence_number)+" has been received")

		if( sentence == "stop client" ): 
			break
		if( sentence == "stop both" ): 
			break
		
		

		print ("Message received: " + str(sentence ))
		capitalizedSentence = sentence.upper()
		print ("upcased: " + str(capitalizedSentence ))


		#SENDING ACK (under diff circumstances):
		if packLost<=random_one and random_one<packCorrupt:
			print("An ACK"+str(field_two)+" is about to be resent")
		elif random_one<packLost:
			print(" ")
		else: # the received pkt is GOOD
			#print msg before sending ACK
			print("An ACK"+str(sequence_number)+" is about to be sent")
		print("ACK packet to send contains: data = 0 seq = "
		+str(sequence_number)+" isack = True")
		#SENDING ACK BELOW
		connectionID.send(capitalizedSentence.encode())
		#finish sending

		#SWITCH STATE
		if is_corrupt or str(field_two)!=str(sequence_number): 
			#PACKET is CORRUPT 
			#or IS repeating
			print("The receiver is moving back to state WAIT FOR "
			+str(field_two)+" FROM BELOW")
		else: #repeating 
			if field_two ==1:
				field_two = 0
			else:
				field_two = 1
			print("The receiver is moving to state WAIT FOR "
			+str(field_two)+ " FROM BELOW")
				

	connectionID.close()
	if( sentence == "stop both"): break

serverSocket.close()
