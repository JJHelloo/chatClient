# server.py
# CST 311: Introduction to Computer Networks
# May 31, 2022
# Programming Assignment #3
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics

# Explain why you need multithreading to solve this problem.
# Multithreading is required to solve this problem because otherwise the second client would be blocked until the first client was finished. In this case, if the first client never terminated its connection, the second client would never establish a connection.  A single threaded server can only handle one connection at a time. Multithreading allows a server to communicate with multiple clients at the same time independently.

# Program description: Server that receives connection from two devices. Assigns a letter X to first device and Y to the second device waits for both devices to connect. Accepts a message from both devices. Prints out the message as the message is sent. Sends the combined message to the client. Closes the connection.

from socket import *
#for time.wait() in letterValueOfFirstClientResponse
import time

#allow threading
import threading

#global variables
# isFirstClient is bool to keep track if thread has the isFirstClient or client y
# true because isFirstClient is true at first
isFirstClient = True;

# Lock is the client that first responds can be x or y
# Set to A to tell if it is working
letterValueOfFirstClientResponse = "A"
# Lock2 is the client that responds second
letterValueOfSecondClientResponse = "A"

#semaphore lock
#nothing at 0, go at 1, loop until 2
proceedLock = 0
continueLock = 0

# response from the clients
# responseFromFirstClient the message sent from the first client to respond
responseFromFirstClient = "A"
# responseFromSecondClient the message sent from the second client to respond
responseFromSecondClient = "A"

# not currently used, check to see that both went
connectStatus = 0;

def join():
  #declare global variables so locals don't take precedent
  global isFirstClient
  global letterValueOfFirstClientResponse
  global letterValueOfSecondClientResponse
  global proceedLock
  global continueLock
  global responseFromFirstClient
  global responseFromSecondClient
  # not currently used
  global connectStatus

  # placeOfConnection is holder where x is first or second, for Accepted placeOfConnection connection, 
  placeOfConnection = ""
  # initialLetter defines if it is X or Y client, initialize as A to know if it works
  initialLetter = "A"
  # isFirstClient is iniatially true global variable
  # flips to false, after first pass of if statement
  # First client will be set to X, and second client set to Y
  if (isFirstClient == True):
    initialLetter = "X"
    placeOfConnection = "first"
  else:
    initialLetter = "Y"
    placeOfConnection = "second"
  isFirstClient = False

  # Setup greeting by server with variables initialLetter and placeOfConnection
  # announced by both threads
  greetingOne = "Accepted "+placeOfConnection+" connection, calling it client "+initialLetter

  # wait message is sent back to client
  wait = "Client "+initialLetter+" connected"
   
  connectionSocket, addr = serverSocket.accept()
  
  # print Accepted first connection, calling client x or
  # print Accepted second connection, calling client y
  print(greetingOne)
  
  # semaphore type lock
  continueLock += 1
  # on first loop check first clients letter
  
  # first client to answer loops until second client answers
  # proceedLock becomes 2 on second response
  while(continueLock<2):
    time.sleep(0.1)
  
  connectionSocket.send(wait.encode())
  
  # if this threrad is client Y 
  # then print out a waiting to receive message once by the Server
  # This is printed after both have connections have been accepted
  if(initialLetter == "Y"):
    print ("")
    print ("Waiting to receive message from client X and client Y....")
    print ("")

  # get response from client
  # print out client letter and message
  response = connectionSocket.recv(1024).decode()
  if (proceedLock==0):
    responseFromFirstClient = response
    print("Client "+initialLetter+" sent message 1: "+responseFromFirstClient)
  else:
    responseFromSecondClient = response
    print("Client "+initialLetter+" sent message 2: "+responseFromSecondClient)

  # semaphore type lock
  proceedLock += 1
  # on first loop check first clients letter
  if (proceedLock == 1):
    # set letterValueOfFirstClientResponse to letter of Client who first responds
    letterValueOfFirstClientResponse = initialLetter
  if (letterValueOfFirstClientResponse=="X"):
    # if first client response is an X then second must be a Y
    letterValueOfSecondClientResponse = "Y"
  else:
    # if first client response is not an X then second must be a X
    letterValueOfSecondClientResponse = "X"

  # first client to answer loops until second client answers
  # proceedLock becomes 2 on second response
  while(proceedLock<2):
    time.sleep(0.1)

  # print which person responded first based on letterValueOfFirstClientResponse, letterValueOfSecondClientResponse  
  # response 1 is the first response
  # response 2 is the second response
  newResponse = (letterValueOfFirstClientResponse + ": " + responseFromFirstClient +" received before " + letterValueOfSecondClientResponse + ": " + responseFromSecondClient)

  # send newResponse to both clients so they can display it
  connectionSocket.send(newResponse.encode())

  # Only print on second thread
  if (initialLetter == letterValueOfSecondClientResponse):
    print(" ")
    print("Waiting a bit for clients to close their connections")
  # wait two seconds
  time.sleep(2)
  if (initialLetter == letterValueOfSecondClientResponse):
    print("Done.")
  # close connection to both
  connectionSocket.close()
  

if __name__ == "__main__":
  serverPort = 12000
  serverSocket = socket(AF_INET, SOCK_STREAM)
  serverSocket.bind(('', serverPort))
  serverSocket.listen(1)

  #greeting message
  print("The server is ready to receive 2 connections....")
  print("")

  #create threads
  one = threading.Thread(target=join)
  two = threading.Thread(target=join)

  #start threads
  one.start()
  two.start()

  #run until complete
  one.join()
  two.join()
  
  