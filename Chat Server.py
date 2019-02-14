# this is the server that the clients will connect to

import socket
from threading import Thread
import time

# intial setup of the server and creation of the socket
host = "128.237.162.118" ###INSERT IP ADDRESS HERE### <<<<<<<<<--------------|||||||
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
print("Waiting for a connection...")
s.listen(2)

# dictionary contain clients that are connected to the server
connections = {}
imgBytes=None

# accepts up to 2 connections
# the structure of these function is inspired by the work on this website:
# https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
# however, my code is different in that it deals with sending and receiving of 
# images. 
def acceptConnections():
    while True:
        conn, addr = s.accept()
        print("Connection from: "+str(addr))
        conn.send(str.encode("Hello! Enter your name."))
        Thread(target = handleClient, args = (conn,addr)).start()
        
        
# receives data from client and acts appropriately
def handleClient(conn, addr):
    name = conn.recv(1024).decode("utf-8").upper()
    connections[conn]=name 
    instructions = "Welcome "+name+"! Refer to the documentation under the 'Help' tab if you need any help!"
    conn.send(str.encode(instructions))
    for client in connections:
        if client!=conn:
            msg = name+" has joined the chat!"
            client.send(str.encode(msg))
    while True:
        global imgBytes
        data = conn.recv(1024).decode("utf-8")
        if data.startswith("<<<{size}>>>"):
            sizeOrig = int(data.split(":")[1])
            size = int(data.split(":")[1])
            conn.send(str.encode("<<<{GOT SIZE}>>>"))
            imgBytes = b''
            while size > 0:
                data = conn.recv(4096)
                if not data:
                    break
                size-=len(data)
                imgBytes+=data
            for client in connections:
                if client!=conn:
                    sizeMsg = "<<<{SIZE}>>>:"+str(sizeOrig)
                    client.send(str.encode(sizeMsg))
        elif data=="<<<{got size}>>>":
            conn.sendall(imgBytes)
        elif data=="<<<{quit}>>>":
            conn.close()
            del connections[conn]
            print("Connection from "+str(addr)+" has been terminated.")
            for client in connections:
                msg = name+" has left the chat."
                client.send(str.encode(msg))
            break
        elif data=="<<<{got image}>>>":
            for client in connections:
                if client!=conn:
                    msg1 = "Image was succesfully sent!"
                    client.send(str.encode(msg1))
                    msg2 = connections[client]+" sent you an image!"
                    conn.send(str.encode(msg2))
        else:
            for client in connections:
                msg = name+": "+data
                client.send(str.encode(msg))
            


startThread = Thread(target = acceptConnections)
startThread.start()
startThread.join()
s.close()