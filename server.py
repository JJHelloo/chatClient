# Server.py
# CST 311: Introduction to Computer Networks
# May 17, 2022
# Programming Assignment #2
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Server that receives pings and outputs message received
# and message sent. Labels the ping successful number.
#
# We will need the following module to generate
# randomized lost packets
import random
from socket import *
# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)  
# set port to a variable
serverPort = 12000
# Assign IP address and port number to socket
serverSocket.bind(('', serverPort))
pingnum = 0
# Count successful pings
pingSuccess = 0
print("Waiting for Client....")
print("")
while True:
    # Count the pings received
    pingnum += 1
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the
    # amount of bytes
    message, address = serverSocket.recvfrom(1024)
    # If rand is less is than 4, and this not the
    # first "ping" of a group of 10, consider the
    # packet lost and do not respond
    if rand < 4 and pingnum % 10 != 1:
        #formatted with white space
        print("")
        #announce packet is lost
        print("Packet was lost.")
        print("")
        print("")
        continue
    # Otherwise, the server responds
    # increment successful ping
    pingSuccess += 1
    #print ping successful number
    print("PING " + str(pingnum) + " Received")
    #output message received at server
    print(message.decode())
    modifiedMessage = message.decode().upper()
    #output message sentback to client
    print(modifiedMessage)
    serverSocket.sendto(modifiedMessage.encode(), address)
    print(" ")


