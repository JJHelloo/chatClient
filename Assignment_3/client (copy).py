# client.py
# CST 311: Introduction to Computer Networks
# May 31, 2022
# Programming Assignment #3
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Client that connects to a server
# Sends a message to the server
# receives messages from the server

from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
# sentence = input("Input lowercase sentence:")
greeting = "hello"
clientSocket.sendto(greeting.encode(),(serverName, serverPort))
modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())
# holdingPattern = clientSocket.recv(1024)
# time.sleep(.1)
# toll = "stop"
# while(toll == "stop"):
#  toll = clientSocket.recv(1024)
sentence = input("Enter message to send to server:" )
clientSocket.sendto(sentence.encode(),(serverName, serverPort))
modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())
clientSocket.close()
