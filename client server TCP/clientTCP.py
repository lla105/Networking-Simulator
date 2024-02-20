# sender side??
print("CLIENT TCP RUNNING NOW")
from socket import *
import random
import time


serverName = 'localhost'

serverPort = 50007
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (serverName, serverPort) )
count = 0
field_one = random.randint(25,100)
# for packet, range [25,100]
# for ACK, = 0
field_two = 0
# for packets, it's the sequence # (1 or 0)
# for ACK, it's the acknowledgement #
field_three = False 
# True if ACK, False if not ACK
#packet0 = str(field_one) + " " + str(field_two) + " " + str(field_three) #ANSWER
packet_array = [field_one,field_two,field_three]

# REQUIREMENT 4
# CHANGE these to input() afterwards

tempseedTiming = random.seed(random.random())
seedTiming = int(input("1)Define seedTiming [2,32000]: ") )
if seedTiming<2 or seedTiming>32000: seedTiming = 111

tempACKCorr = random.seed(random.random())
seedACKCorr = int(input("2)Define seedACKCorr (2,32000): ") )
if seedACKCorr <=2 or seedACKCorr >=32000: seedACKCorr = 222

tempseedDefault = random.seed(random.random())
seedDefault = int(input("3)Define seedDefault (2,32000): "))
if seedDefault<=2 or seedDefault>=32000: seedDefault = 333

numPackets = int(input("4)Define numPackets (1,100): "))
if numPackets<=1 or numPackets>=100: numPackets = 10

ACKcorrupt = float(input("5)Define ACKcorrupt [0,1)"))
if ACKcorrupt<0 or ACKcorrupt>=1: ACKcorrupt = 0.001

ACKlost = float(input("6)Define ACKlost [0,ACKcorrupt)"))
if ACKlost<0 or ACKlost>=ACKcorrupt: ACKlost = 0.0005
#RoundTripTravel. Expires if ACK not received.

RRT = float(input("7)Determine RRT (0.1,10]: "))
if RRT<=0.1 or RRT>10: RRT = 5

client_state = 1 # 1,2,3, or 4
# state 1 = IDLE 0. Wait for data
# state 2 = WAIT for ACK 0
# state 3 = IDLE 1. wait for data
# state 4 = WAIT for ACK 1

sequence_number = 999

random_one = random.uniform(0.0,6.0) #randomizing timer number
deadline = time.time() + random_one # timeout function. this deadline helps
# the count down by seconds.

#del later

turns = 0

sentence = " "
while True:
    if turns>numPackets:
        sentence = "stop client"
        
    print("==================starting at state: " +str(field_two)
    + "====================")
    

    field_one = random.randint(25,100)
    is_corrupt = False
    is_lost = False
    # print ("connected to: " + str(serverName) + str(serverPort) ) #GIVEN
    #sentence = input('Input lowerecase sentence:')
    
    if sentence == "stop client":
        sentence = "stop client"
    elif sentence == "stop both":
        sentence = "stop client"
    else:
        sentence = str(field_one)+" "+str(field_two)+" "+str(field_three)
    if field_two==1:
        if str(field_two)!=str(sequence_number): # no duplicate
            print("A packet with sequence number 1 is about to be sent\n") #ANSWER
        else: # is a duplicate
            print("A packet with sequence number 0 is about to be resent\n")
    else:
        if str(field_two)!=str(sequence_number): #no duplicate
            print("A packet with sequence number 0 is about to be sent\n") #ANSWER
        else: # is a duplicate
            print("A packet with sequence number 1 is about to be resent\n")
    print("Packet to send contains: data = "+str(field_one)+" seq = "
    +str(field_two)+" isack="+str(field_three)) #ANSWER
    #insert ACK0 or ACK1 if statement here later
    print("Starting timeout timer for ACK"+str(field_two))

    clientSocket.send(sentence.encode())
    # >>>>>>> SENT OUT ACK packet here
    #!!!
    print("The sender is moving to state WAIT FOR ACK"+str(field_two))
    
    random_two = random.random()
    #determine if ACK is corrupt or lost.
    #if this # < ACK lost prob, then it's considered LOST
    #if ACK lost prob <= this # < ACK corrupt prob, then it's CORRUPTED
    random_three = random.randint(25,100)
    #packet data

    # random_one = random.uniform(0.0,6.0) . this is written above
    # we crash when we reach a -ve number. find out what janice wants.
    #fstring <--- google this later
    duration = deadline - time.time()
    clientSocket.settimeout(duration) # SET TIME OUT HERE !!!!!
    time_now = random_one - time.time()
    # still works even packet not lost or corrupt or received on time.
    print(duration)
    if duration <= 0.1 :
        print("ACK"+str(field_two)+" timeout timer expired (packet lost")
        deadline = time.time() + random_one
    # >>>> RECEIVED ACK packet below
    modifiedSentence = clientSocket.recv(1024) #GIVEN
    
    temp_msg = modifiedSentence.decode()
    for i in range(len(temp_msg)):
        if temp_msg[i] == " ":
            sequence_number = temp_msg[i+1]
            #print("field two is: " + str(sequence_number))
            break
    #DELETE LATER. TEST PURPOSE:
    #ACKcorrupt = 0.9
    #ACKlost = 0.1
    #random_two = 0.7
    #if ACK is corrupted:
    if random_two<=ACKcorrupt and random_two>ACKlost:
        #print("ACK is corrupt") # is corrupt
        print("A Corrupted ACK packet has just been received")
        is_corrupt = True
        if str(field_two)==0: client_state=2
        if str(field_two)==1: client_state=4
    elif random_two<ACKlost: #ACK IS LOST
        #print("ACK is lost")
        # INSERT TIMER FUNCTION HERE
        is_lost = True
        print("ACK"+str(field_two)+" timeout timer expired (ACK lost)")
    elif str(field_two) != str(sequence_number):
        if str(field_two)==0: client_state=2
        if str(field_two)==1: client_state=4
        print("A duplicate ACK"+str(sequence_number)+" has just been received")
    else:
        print("ACK is perfect!")
        print("An ACK"+str(field_two)+" packet has just been received")
        print("Packet received contains: data = "+str(field_one)
        +" seq = "+str(field_two)+" isack= "+str(field_three) ) #ANSWER
        print("stopping timeout timer for ACK"+str(field_two)) #ANSWER
    
    print( "From Server: " + modifiedSentence.decode())

    # TIMER
    #print("current socket timeout:" + str(clientSocket.gettimeout()))

    #SWITCH STATE
    if is_corrupt or str(field_two)!=str(sequence_number) or is_lost: 
        #ACK is CORRUPT or out of order
        print("The sender is moving back to state WAIT FOR ACK"
        +str(field_two) )
    else: # package is NOT corrupt, and is in order
        if field_two == 1:
            print("The sender is moving to state WAIT FOR CALL 0 FROM ABOVE")
            field_two=0

        else:
            print("The sender is moving to state WAIT FOR CALL 1 FROM ABOVE")
            field_two = 1

    print("==================ending at state: " +str(field_two)
    + "====================")

    turns = turns +1
    #print (" TURN NOW IS :     " + str(turns))


#C:\Users\aaaal\Documents\SFU 2021\CMPT 371\ass2
# rdt_rcv(packet)
# extract(packet, data)
# deliver_data(data)