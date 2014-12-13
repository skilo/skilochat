#Skilo Chat Encrypted Instant Messenger
#Developed by Skilo, skilo47@gmail.com
#GPLV3 Free Software
#License: http://gnu.org/copyleft/gpl.html

#This program is free software: you can redistribute it and/or modify
    #it under the terms of the GNU General Public License as published by
    #the Free Software Foundation, either version 3 of the License, or
    #(at your option) any later version.

    #This program is distributed in the hope that it will be useful,
    #but WITHOUT ANY WARRANTY; without even the implied warranty of
    #MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    #GNU General Public License for more details.

    #You should have received a copy of the GNU General Public License
    #along with this program.  If not, see <http://www.gnu.org/licenses/>.



import string
import traceback
import random
import socket   
from threading import Thread
from tkinter import *
from pyDes import *

def deKey():
    global topDeKey
    topDeKey = Toplevel()
    topDeKey.title("Enter Decryption Key")
    topDeKey.geometry("300x100")
    topDeKey.resizable(width=FALSE, height=FALSE)
    innerText = Message(topDeKey, text="Enter a friends decryption key here")
    innerText.pack(side=TOP)
    global deKey
    global deKeyBox
    deKey = StringVar()
    deKeyBox = Entry(topDeKey, textvariable=deKey, bg="white", width="45")
    deKeyBox.pack()
    button = Button(topDeKey, bg="green", text="Set", command=saveDecKey)
    button.pack(side=BOTTOM)

def saveDecKey():
    global deKey
    global deKeyBox
    global topDeKey
    global decKeyFile
    deKey = deKeyBox.get()
    topDeKey.destroy()
    decKeyFile = open('deckey.txt', 'w')
    decKeyFile.write(deKey)
    decKeyFile.close()
    

def keyGen(size=8, chars=string.hexdigits):
    global key
    global keyFile
    key = "".join(random.choice(chars) for _ in range(size))
    keyFile = open('keyfile.txt', 'w')
    keyFile.write(key)
    keyFile.close()
    textDisplayBox.configure(state=NORMAL)
    textDisplayBox.insert(END, "\n" + "This is your encryption key: " + key + "\n" + "It is stored in keyfile.txt" + "\n")
    textDisplayBox.configure(state=DISABLED)

def about():
    textDisplayBox.configure(state=NORMAL)
    textDisplayBox.insert(END, "\n" + "Skilo Chat, Encrypted p2p instant messenger")
    textDisplayBox.configure(state=DISABLED)
    

def setIp():
    global topSetIp
    topSetIp = Toplevel()
    topSetIp.title("Connect to")
    topSetIp.geometry("300x100")
    topSetIp.resizable(width=FALSE, height=FALSE)
    innerText = Message(topSetIp, text="Enter the IP you wish to connect to")
    innerText.pack(side=TOP)
    global ipEntry
    ipEntry = StringVar()
    ipEntryBox = Entry(topSetIp, textvariable=ipEntry, bg="white", width="45")
    ipEntryBox.pack()
    button = Button(topSetIp, bg="green", text="Set", command=saveIp)
    button.pack(side=BOTTOM)

def saveIp():
    global host
    host = StringVar()
    global ipEntry
    host = ipEntry.get()
    global topSetIp
    topSetIp.destroy()


def setUsername():
    global topSetUsername
    topSetUsername = Toplevel()
    topSetUsername.title("Set Username")
    topSetUsername.geometry("300x100")
    topSetUsername.resizable(width=FALSE, height=FALSE)
    global usernameEntry
    usernameEntry = StringVar()
    usernameEntryBox = Entry(topSetUsername, textvariable=usernameEntry, bg="white", width="45")
    usernameEntryBox.pack()
    usernameButton = Button(topSetUsername, bg="green", text="set", command=saveUsername)
    usernameButton.pack(side=BOTTOM)


def saveUsername():
    global username
    username = StringVar()
    global usernameEntry
    username = usernameEntry.get()
    global topSetUsername
    topSetUsername.destroy()

def stop():
    root.destroy()
    

def recvData():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 8888))
        s.listen(10)
        while 1:
            conn, addr = s.accept()
            data = conn.recv(1024)
            k = des(decryptionKey, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
            decMessage = k.decrypt(data)
            reply = decMessage.decode("UTF-8")
            textDisplayBox.configure(state=NORMAL)
            textDisplayBox.insert(END, '\n' + reply)
            textDisplayBox.yview(END)
            textDisplayBox.configure(state=DISABLED)
    except:
        e = traceback.format_exc()
        with open("error_log.txt", "a") as f:
            f.write(e)
    finally:
        s.close()
        

def sendData():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        global host
        port = 8888
        global username 
        spacer = ": "
        msg = entryText.get()
        msg.encode("UTF-8")
        spacer.encode("UTF-8")
        username.encode("UTF-8") 
        textDisplayBox.configure(state=NORMAL)
        textDisplayBox.insert(END, '\n' + username + spacer + msg)
        textDisplayBox.yview(END)
        textDisplayBox.configure(state=DISABLED)
        textEntryBox.delete(0, END)
        global key
        k = des(key, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
        encMessage = k.encrypt(username + spacer + msg)
        s.connect((host, 8888))
        s.send(bytes(encMessage))
    except:
        e = traceback.format_exc()
        with open("error_log.txt", "a") as f:
            f.write(e)
    

def pressAction(event):
    textEntryBox.config(state=NORMAL)
    sendData()

def disableEntry(event):
    textEntryBox.config(state=DISABLED)

#main function begins here
         
username = "Anonymous"
host = "192.168.1.0" #value set to internal ip to prevent errors when no IP is set.

#read decryption key from file
decryptionKey = open("deckey.txt", "r").read()

#start listening for incoming connections
recvDataThread = Thread(target=recvData)
recvDataThread.daemon = True
recvDataThread.start()

#read encryption key from file 
with open("keyfile.txt", "r") as readKey:
    global key
    key = readKey.read()


#create root window
root = Tk()
root.resizable(width=FALSE, height=FALSE)

#other variables
entryText = StringVar()
usernameEntry = StringVar()

#modify root window
root.title("Skilo Chat")
root.geometry("800x600")

#create the menu bar
menubar = Menu(root)
    
#menubar file label
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=stop)

#menubar options label
optionsmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Options", menu=optionsmenu)
optionsmenu.add_command(label="Set Username", command=setUsername)
optionsmenu.add_command(label="Connect to IP", command=setIp)

#encryption key label
keymenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Encryption", menu=keymenu)
keymenu.add_command(label="Generate new key", command=keyGen)

#decryption label
dekeymenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Decryption", menu=dekeymenu)
dekeymenu.add_command(label="Enter a decryption key", command=deKey)

#menubar about/help label
helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=helpmenu)
helpmenu.add_command(label="About...", command=about)

#create scroll bars for textdisplaybox
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

	
#create the text display area
textDisplayBox = Text(root, bg="#F0F0F0", width="100", height="34",yscrollcommand=scrollbar.set)
scrollbar.config(command=textDisplayBox.yview)
textDisplayBox.configure(state=DISABLED)
textDisplayBox.pack(side=TOP)

#add buttons
button1 = Button(root, command=sendData, text="Send", bg="green", font="sans-serif", width="100")
button1.pack(side=BOTTOM)
	
#create entry widget
textEntryBox = Entry(root, textvariable=entryText, bg="white", width="135")
textEntryBox.bind("<Return>", disableEntry)
textEntryBox.bind("<KeyRelease-Return>", pressAction)
textEntryBox.pack(side=BOTTOM)

#kick off the event loop
root.config(menu=menubar)
root.mainloop()

#end of main function

    
    


     
    
