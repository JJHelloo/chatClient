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

modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())

sentence = input("Enter message to send to server:" )
clientSocket.sendto(sentence.encode(),(serverName, serverPort))
modifiedSentence = clientSocket.recv(1024)
print("From Server: ", modifiedSentence.decode())
clientSocket.close()
