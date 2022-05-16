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
alpha = 0.125
beta = 0.25
estimatedRTT = 0
devRTT = 0

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
          avgRTTSum = timeDifference
          estimatedRTT = timeDifference
          devRTT = timeDifference / 2
        
        # calculate avg RTT
        # only calculates non-timed values
        else:
          avgRTTSum += timeDifference
          estimatedRTT = (1 - alpha) * estimatedRTT + (alpha * timeDifference)
          devRTT = (1 - beta) * devRTT + beta * abs(timeDifference - estimatedRTT)

        # check if min or max RTT
        if timeDifference > maxRTT:
          maxRTT = timeDifference
        if timeDifference < minRTT:
          minRTT = timeDifference
      
        print("PONG " + str(numberPing) + " RTT " + str(timeDifference) + " ms")
        print(" ")
    # if false
    else:
        # increment packet loss
        packetLoss += 1
        print("No Mesg rcvd")
        print("PONG " + str(numberPing) + " Request Timed out")
        print(" ")
# done with socket
clientSocket.close()

timeoutInterval = estimatedRTT + (4 * devRTT)

# after closing printout calculations
# print min
print("Min RTT:\t" + str(minRTT) )
# print max
print("Max RTT:\t" + str(maxRTT) )
# calculate RTT 
# sum divided by number of successful pings
avgRTT = avgRTTSum/successfulPing
print("Avg RTT:\t" + str(avgRTT) )
# packet loss will always be X0.0%
# where x is loss packets
print("Packet Loss:\t" + str(packetLoss) + "0.0%")
print("Estimated RTT:\t" + str(estimatedRTT) + " ms")
print("Dev RTT:\t" + str(devRTT) + " ms")
print("Timeout Interval: " + str(timeoutInterval) + " ms")