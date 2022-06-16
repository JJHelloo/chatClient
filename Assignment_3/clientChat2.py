# client.py
# CST 311: Introduction to Computer Networks
# May 31, 2022
# Programming Assignment #3EC
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Client that connects to a server
# Sends a message to the server
# receives messages from the server
# sends message from one client to another

from socket import *
import time
import threading
import multiprocessing

import sys, select

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())

running = True
turnOff = False

def sendMessage():
  global running
  global turnOff
  while(running):
    sentence = "undo"
    undo = "undo"
    i, o, e = select.select([sys.stdin], [], [], 5)
    if (i):
      sentence = sys.stdin.readline().strip()
    #sentence = input()
    if (sentence!=undo):
      clientSocket.sendto(sentence.encode(),(serverName, serverPort))
    if(sentence=="bye"):
      turnOff = True;
    if(turnOff):
      time.sleep(.5)
      #clientSocket.close()
      break
    if(running):
      time.sleep(.5)
      #clientSocket.close()
      break
  
    #if(sentence == "bye"):
    #  running = False

def receiveMessage():
  global running
  while(running):
    modifiedSentence = clientSocket.recv(1024)
    response = modifiedSentence.decode()
    if(response == "bye"): #ERROR: message is received as "Client Y: bye" not "bye"
      running = False
    else:
      print(response)
    if(turnOff):
      time.sleep(.5)
      #clientSocket.close()
      break
    if(running):
      time.sleep(.5)
      #clientSocket.close()
      break
    

sendThread = threading.Thread(target=sendMessage)
receiveThread = threading.Thread(target=receiveMessage)

#start threads
sendThread.start()
receiveThread.start()

#run until complete
receiveThread.join()
#sendThread.terminate()

# sendThread.join()

clientSocket.close()

