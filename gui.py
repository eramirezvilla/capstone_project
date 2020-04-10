#imports
import socket	
import sys
import time

#const vars 
portNumber = 8080	
IPAddress = '127.0.0.1'
bufferSize = 1024

nameIndex = 0
balanceIndex = 1
foundStatusIndex = 2
balanceStatusIndex = 3

dataIndex = 0

delimiter = ','
dataEnd = b'\0'

guiScreenDelay = 3000                                                       #3 seconds

def main():
    guiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #create socket
    serverAddress = (IPAddress, portNumber)                                  #create socket info with IP address and port #
    guiSocket.bind(serverAddress)                                           #bind

    guiSocket.listen(16)                                                    #listen TODO: unsure what argument does/is

    while True: 
        
        #TODO: Launch GUI IDLE screen 

        connection, clientAddress = guiSocket.accept()	                    #connection made with client (val)
        
        try:
            #Incoming data in order: "<Acct Name>, <Acct Balance>, <Acct Found Status>, <Acct Balance Status>"
            #-----------------------------------------------------------------------------------------------#

            rawBytes = connection.recv(bufferSize)                          #get all of the incoming data (size of buffer)

            cleanBytes = rawBytes.split(dataEnd)                            #find the null terminator that ends the desired data in the buffer

            strData = cleanBytes[dataIndex].decode("utf-8")                 #deconde to string type and keep whatever is in front of the null terminator
            
            data = strData.split(delimiter)                                 #split data into vars

                                                                            #set new vars
            acctName = data[nameIndex]
            acctBalance = data[balanceIndex]
            acctFoundStatus = int(data[foundStatusIndex])
            acctBalanceStatus = int(data[balanceStatusIndex])


            if(not acctFoundStatus):
                #TODO: Launch GUI NO ACCT screen
                print("ACCT NOT FOUND")
            elif(not acctBalanceStatus):
                #TODO: Launch GUI NO BALANCE screen 
                print("NOT ENOUGH ACCT BALANCE")
            else:
                #TODO: Launch GUI ACCEPTED screen
                print("ACCT ACCEPTED")

            Timer(guiScreenDelay)                                           #delays to keep screen displayed
                                                                            #will catch up if a new beacon arrives will still displaying 
                                                                            #as long as there is enough space in buffer
                                                                            #TODO: should open gate after GUI display completes
                                                                            #maybe find a better way to keep screen up using GUI library
        finally:
            connection.close()                                              #close connection


def Timer(milliseconds):
    startTime = int(round(time.time()) * 1000)
    timerFlag = True

    while(timerFlag):
        millisecondsPassed = (int(round(time.time()) * 1000) - startTime)
        if(millisecondsPassed >= milliseconds):
            timerFlag = False
    




if __name__ == "__main__":
    main()