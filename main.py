# CST 311: Introduction to Computer Networks
# May 17, 2022
# Programming Assignment #2
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Client sends pings out. Times out if longer than a second.
# Calculates a host of values such as:
# min, max, avg RTT; packet loss, estimated RTT, Dev RTT, and
# Timeout Interval
#
# for time library
import time
from socket import *
# server on H2 is located @ 10.0.0.2
# 127.0.0.1 for home server 
# 10.0.0.2
serverName = "10.0.0.2"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

# initialize variables
successfulPing = 0
numberPing = 0
packetLoss = 0
# initialize min and max RTT
minRTT = 0
maxRTT = 0
avgRTTSum = 0

# print spacer
print(" ")

# loop for 10 ping attempts

# need timeout and calculate values
for x in range(0, 10):
    responseReceived = False
    clientSocket.settimeout(1.0)
    # increment numberPing
    numberPing +=1
    # create ping message
    message = "ping"+str(numberPing)
    # need e12 seconds
    # before or after sendto? start time?
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    # start timer
    startTime = time.time()
    # try catch timout greater than 1 second error
    # if it doesn't time out then response received is true
    try:
        clientSocket.settimeout(1)
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        # end timer
        returnTime = time.time()
        responseReceived = True
    # if catch fails then response received is negative
    except Exception as e:
        print("Mesg sent: " + message)
        responseReceived = False
    if responseReceived == True:
        successfulPing += 1
        clientSocket.settimeout(0)
        print("Mesg sent: " + message)
        print("Mesg rcvd: " + modifiedMessage.decode())
        # format time for scientific notation
        
        print("Start time: " + "{:e}".format(startTime))
        print("Return time: " + "{:e}".format(returnTime))
        
        # non scientific start and return below
        
        # print("Start time: " + str(startTime))
        # print("Return time: " + str(returnTime))
        # multiply by a thousand for milli seconds
        # convert string to float
        timeDifference = ((returnTime) - (startTime)) * 1000
        # if first ping set to min and max RTT
        if numberPing == 1:
          maxRTT = timeDifference
          minRTT = timeDifference
        # check if min or max RTT
        if timeDifference > maxRTT:
          maxRTT = timeDifference
        if timeDifference < minRTT:
          minRTT = timeDifference
        # calculate avg RTT
        # only calculates non-timed values
        avgRTTSum = timeDifference + avgRTTSum
        print("PONG " + str(numberPing) + " RTT " + str(timeDifference) + " ms")
        print(" ")
    # if false
    else:
        # increment packet loss
        packetLoss += 1
        print("No Mesg rcvd")
        print("PONG " + str(numberPing) + " Request Timed out")
        print(" ")
clientSocket.close()

# after closing printout calculations
# print min
print("Min RTT:          " + str(minRTT) )
# print max
print("Max RTT:          " + str(maxRTT) )
# calculate RTT 
# sum divided by number of successful pings
avgRTT = avgRTTSum/successfulPing
print("Avg RTT:          " + str(avgRTT) )
# packet loss will always be X0.0%
# where x is loss packets
print("Packet Loss:      " + str(packetLoss) + "0.0%")
print("Estimated RTT:    x")
print("Dev RTT:          x")
print("Timeout Interval: x")