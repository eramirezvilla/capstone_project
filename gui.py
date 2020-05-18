#imports
import socket	
import sys
import time
import tkinter as tkr

#const vars 
portNumber = 8080	
IPAddress = '127.0.0.1'
bufferSize = 1024

smallScreenMax = 1024

nameIndex = 0
balanceIndex = 1
foundStatusIndex = 2
balanceStatusIndex = 3

ticketPrice = 2.5

dataIndex = 0

delimiter = ','
dataEnd = b'\0'

guiScreenDelay = 3000                                                       #3 seconds
guiMachineDelay = 400                                                       #4 milliseconds

def main():

#   SOCKET INIT
    guiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           #create socket
    serverAddress = (IPAddress, portNumber)                                 #create socket info with IP address and port #
    guiSocket.bind(serverAddress)                                           #bind
    guiSocket.listen(16)                                                    #listen TODO: unsure what argument does/is


#   TKINTER INIT
    tk = tkr.Tk()

    screenWidth = tk.winfo_screenwidth()
    screenHeight = tk.winfo_screenheight()

    #this bool is used to determine what size monitor (based on pixels) the gui is being displayed on
    #if smallScreen = true very small raspberry pi monitor 
    #if smallScreen = false standard computer screen size
    if(screenWidth <= smallScreenMax):
        smallScreen = True
    else:
        smallScreen = False

    tk.title("San Diego Metro Station")
    tk.bind("<F11>", lambda event: tk.attributes("-fullscreen", not tk.attributes("-fullscreen")))
    tk.bind("<Escape>", lambda event: tk.attributes("-fullscreen", False))
    tk.attributes('-fullscreen', True)

#   CANVAS INIT
    canvas = tkr.Canvas(
        tk, 
        width = screenWidth, 
        height = screenHeight, 
        bg = 'white')

    canvas.grid()

#   CANVAS IMG
    cubicImg = tkr.PhotoImage(file = 'cubicImgSmall.png' if smallScreen else 'cubicImg.png')

    canvasCubicImg = canvas.create_image(
        (screenWidth - cubicImg.width()), 
        (screenHeight - cubicImg.height()), 
        image = cubicImg, 
        anchor = 'nw')

#   CANVAS TEXT
    canvasTitleText = canvas.create_text(
        (screenWidth / 8), 
        10, 
        fill = "darkblue", 
        font = "Times 50" if smallScreen else "Times 100", 
        text = "San Diego Metro Station", 
        anchor = 'nw')

    canvasAcctInfoRect = canvas.create_rectangle(
        (screenWidth / 2), 
        (screenHeight / 4), 
        (screenWidth - 10), 
        (screenHeight - cubicImg.height()), 
        outline = "darkblue", 
        width = 7)

    canvasAcctInfoText = canvas.create_text(
        (screenWidth / 2) + (screenWidth / 20), 
        (screenHeight / 4) + 10, 
        fill = "darkblue", 
        font = "Times 30" if smallScreen else "Times 60", 
        text = "Account Information:", 
        anchor = 'nw')

#   TKINTER UPDATE
    tk.update_idletasks()
    tk.update()
#    i = 0

    while True: 
        tk.update_idletasks()
        tk.update()
        Timer(guiMachineDelay)                                              #not sure if necessary because program will wait for connection from client                                           

#        connection, clientAddress = guiSocket.accept()	                    #connection made with client (val)
        
        try:
            #Incoming data in order: "<Acct Name>, <Acct Balance>, <Acct Found Status>, <Acct Balance Status>"
            #-----------------------------------------------------------------------------------------------#
            
            rawBytes = connection.recv(bufferSize)                          #get all of the incoming data (size of buffer)
            
            cleanBytes = rawBytes.split(dataEnd)                            #find the null terminator that ends the desired data in the buffer

            strData = cleanBytes[dataIndex].decode("utf-8")                 #decode the string type and keep whatever is in front of the null terminator
            
            data = strData.split(delimiter)                                 #split

            #Code to test w/o validator socket, comment out all socket code 
#            strData = ["Akila,34.0,1,1", "Edgar,34.0,0,1", "Tessa,2.0,1,0", "Cassidy,34.0,1,1"]	            

#            data = strData[i].split(delimiter)                      
#            i = i + 1	
#            if(i >= 4):	
#                i = 0

            acctName = data[nameIndex]	
            acctBalance = float(data[balanceIndex])
            acctFoundStatus = int(data[foundStatusIndex])
            acctBalanceStatus = int(data[balanceStatusIndex])


            if(not acctFoundStatus):
                invalidImg = tkr.PhotoImage(file = 'XSmall.png' if smallScreen else 'X.png')

                #status image
                canvasInvalidImg = canvas.create_image(
                    (invalidImg.width() / 4), 
                    (screenHeight - (invalidImg.height() + (invalidImg.height() / 4))), 
                    image = invalidImg, 
                    anchor = 'nw') 

                #Status text
                canvasDeniedText = canvas.create_text(
                    ((invalidImg.width() / 4) + (invalidImg.width() / 20)), 
                    ((screenHeight * 3) / 8), 
                    fill = "red", 
                    font = "Times 20" if smallScreen else "Times 40", 
                    text = "ACCESS DENIED", 
                    anchor = 'nw')

                #Acct Info text
                canvasNotFoundText = canvas.create_text(
                    (screenWidth / 2) + (screenWidth / 20), 
                    (screenHeight / 3) + (screenHeight / 10),
                    fill = "black", 
                    font = "Times 20" if smallScreen else "Times 40",
                    text = "Your account was not found.", 
                    anchor = 'nw')  
                
            elif(not acctBalanceStatus):
                invalidImg = tkr.PhotoImage(file = 'XSmall.png' if smallScreen else 'X.png')

                #status Image
                canvasInvalidImg = canvas.create_image(
                    (invalidImg.width() / 4), 
                    (screenHeight - (invalidImg.height() + (invalidImg.height() / 4))), 
                    image = invalidImg, 
                    anchor = 'nw') 

                #status text
                canvasDeniedText = canvas.create_text(
                    ((invalidImg.width() / 4) + (invalidImg.width() / 20)), 
                    ((screenHeight * 3) / 8), 
                    fill = "red", 
                    font = "Times 20" if smallScreen else "Times 40", 
                    text = "ACCESS DENIED", 
                    anchor = 'nw')

                #Acct Info text
                canvasNoBalanceText = canvas.create_text(
                    (screenWidth / 2) + (screenWidth / 20), 
                    (screenHeight / 3) + (screenHeight / 10), 
                    fill = "black", 
                    font = "Times 20" if smallScreen else "Times 40", 
                    text = "Welcome " + acctName + ".\nYou have $" 
                        + str(round(acctBalance, 3)) + "0 in your account.\nYou need $" 
                        + str(round((ticketPrice - acctBalance), 2)) 
                        + "0 to purchase a ticket.", 
                    anchor = 'nw')

            else:
                validImg = tkr.PhotoImage(file = 'checkSmall.png' if smallScreen else 'check.png')

                #status image
                canvasValidImg = canvas.create_image(
                    (validImg.width() / 4), 
                    (screenHeight - (validImg.height() + (validImg.height() / 4))), 
                    image = validImg, 
                    anchor = 'nw') 

                #status text
                canvasAcceptedText = canvas.create_text(
                    ((validImg.width() / 4) + (validImg.width() / 20)), 
                    ((screenHeight * 3) / 8),
                    fill = "green", 
                    font = "Times 20" if smallScreen else "Times 40", 
                    text = "ACCESS GRANTED", 
                    anchor = 'nw')

                #acct info text
                canvasWelcomeText = canvas.create_text(
                    (screenWidth / 2) + (screenWidth / 20), 
                    (screenHeight / 3) + (screenHeight / 10), 
                    fill = "black", 
                    font = "Times 20" if smallScreen else "Times 40", 
                    text = "Welcome " + acctName + ".\nYour new balance is $" 
                        + str(round(acctBalance, 2)) + "0.\nEnjoy your trip.", 
                    anchor = 'nw')

            tk.update_idletasks()
            tk.update()
            Timer(guiScreenDelay)                                   #TODO: make dynamic, different delay times for different screens or if beacon is waiting
                                                                    #unsure how to check if beacon info is waiting in buffer or waiting for connection

            #clear specific images after delay
            if(not acctFoundStatus):
                canvas.delete(canvasInvalidImg)
                canvas.delete(canvasNotFoundText)
                canvas.delete(canvasDeniedText)
            elif(not acctBalanceStatus):
                canvas.delete(canvasInvalidImg)
                canvas.delete(canvasNoBalanceText)
                canvas.delete(canvasDeniedText)
            else:
                canvas.delete(canvasValidImg)
                canvas.delete(canvasWelcomeText)
                canvas.delete(canvasAcceptedText)

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
