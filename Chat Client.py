# This is the client application. You run this code.


# The following website was utilized in understanding tkinter gui construction
# http://effbot.org/tkinterbook/
# this is sort of like documentation for tkinter with some examples
# Given that the implementation of gui widgets in tkinter is pretty standard, 
# any of the tkinter stuff is my code.

### Importing 
from tkinter import *
import socket
from threading import Thread
from tkinter import filedialog, messagebox
import time
from PIL import Image, ImageTk
from stegoImgTxt import *
from stegoImgImage import *
import os

### Setting up global variables
imgCounter = 1
basename = "image%s.png"
filePath = None
s= None
receivedImages = {}
receivedCounter=1
sentImages = {}
sentCounter=1

### Automatically creating folders to save images
currPath = os.getcwd().replace("\\","/")
receivedPath = currPath+"/Received Images"
encodedPath = currPath+"/Encoded Images"
decodedPath = currPath+"/Decoded Images"
try:
    os.mkdir(receivedPath)
except FileExistsError:
    pass
try:
    os.mkdir(encodedPath)
except FileExistsError:
    pass
try:
    os.mkdir(decodedPath)
except FileExistsError:
    pass

### Setting default theme
bgColor = "#009688"
buttonColor = "#FF5722"
txtColor = "#FFFFFF"
chatColor = "#FFFFFF"
chatTxtColor = "#000000"

### Connect Window
def start():
    global bgColor
    global buttonColor
    global txtColor
    global chatColor
    global chatTxtColor
    
    #Connect Screen window
    connectScreen = Tk()
    connectScreen.configure(bg=bgColor)
    connectScreen.title("Connect")
    connectScreen.geometry("300x300+150+150")
    
    
    # Connect functionality
    def connect():
        host = hostTxt.get()
        port = portTxt.get()
        print("Connecting to "+host+" on port "+port+"...")
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((host, int(port)))
            print("Connected!!")
            connectScreen.destroy()
            chat()
        except:
            error = Toplevel()
            error.withdraw()
            messagebox.showerror("Error", "Could not connect to the specified server and port")
    
    #connect button
    connectButton = Button(connectScreen, text = "Connect", command=connect, bg=buttonColor, fg=txtColor)
    connectButton.place(relx=.5, rely=.75, anchor="c")
    
    
    #host/port entry fields
    hostTxt = StringVar()
    portTxt = StringVar()
    hostTxt.set("127.0.0.1")
    portTxt.set("5555")
    hostInput = Entry(connectScreen, textvariable = hostTxt)
    portInput = Entry(connectScreen, textvariable = portTxt)
    hostInput.place(relx = .6, rely = .5, anchor="c")
    portInput.place(relx = .6, rely = .6, anchor="c")
    
    
    # Host/Port/Title labels
    hostLabel = Label(connectScreen, text = "Host:", bg=bgColor, fg=txtColor)
    portLabel = Label(connectScreen, text = "Port:", bg=bgColor, fg=txtColor)
    titleLabel = Label(connectScreen, text = "Hide.me", font = "Arial 34", bg=bgColor, fg=txtColor)
    hostLabel.place(relx = .3, rely = .5, anchor="c")
    portLabel.place(relx = .3, rely = .6, anchor="c")
    titleLabel.place(relx = .5, rely = .25, anchor = "c")
    
    # running
    connectScreen.mainloop()
   
### Chat window
def chat():
    global s
    global bgColor
    global buttonColor
    global txtColor
    global chatColor
    global chatTxtColor
    chatScreen = Tk()
    chatScreen.configure(bg=bgColor)
    chatScreen.title("Chat")
    chatScreen.geometry("506x500+150+150")
    
    # returns back to connect screen
    def newConnect():
        s.send(str.encode("<<<{quit}>>>"))
        chatScreen.destroy()
        start()
       
    # safely close the socket connection and window
    def close():
        s.send(str.encode("<<<{quit}>>>"))
        receivedImages.clear()
        sentImages.clear()
        chatScreen.destroy()
        
    # process for sending an image
    def sendImg(imgPath=None):
        global filePath
        def saidYes():
            file = open(filePath, 'rb')
            bytes = file.read()
            size = len(bytes)
            sizeMsg = "<<<{size}>>>:"+str(size)
            s.send(str.encode(sizeMsg))
            imgWindow.destroy()
            
        def saidNo():
            imgWindow.destroy()
        
        try:
            if imgPath==None:
                filePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            else:
                filePath=imgPath
            imgWindow = Toplevel()
            imgWindow.configure(bg=bgColor)
            imgWindow.title("Selected Image")
            selectedIm = Image.open(filePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(imgWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1)
            noButton = Button(imgWindow, text="No", command=saidNo, bg=buttonColor, fg=txtColor)
            yesButton = Button(imgWindow, text="Yes", command=saidYes, bg=buttonColor, fg=txtColor)
            questionLabel = Label(imgWindow, text = "Send this image?", bg=bgColor, fg=txtColor)
            noButton.pack(side=BOTTOM)
            yesButton.pack(side=BOTTOM)
            questionLabel.pack(side=BOTTOM)
            imgLabel.mainloop()
        except:
            imgWindow.destroy()
        
    # linear encoding image window
    def encodeImgLinear():
        global encodedPath
        
        def encodeLinear():
            encodingIm = StegoImg(encodePath)
            msg = entryTxtBox.get("1.0",END)
            encodedImg = encodingIm.encode(msg, encodedPath)
            linEncodeWindow.destroy()
            sendImg(encodedImg.filePath)
            
        try:
            encodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            linEncodeWindow = Toplevel()
            linEncodeWindow.configure(bg=bgColor)
            linEncodeWindow.title("Linear LSB Encoding")
            selectedIm = Image.open(encodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(linEncodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            entryLabel = Label(linEncodeWindow, text = "Enter the text you wish to encode:", bg=bgColor, fg=txtColor)
            entryTxtBox = Text(linEncodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            encodeButton = Button(linEncodeWindow, text="Encode!", command=encodeLinear, bg=buttonColor, fg=txtColor)
            encodeButton.pack(side=BOTTOM, pady=5)
            entryTxtBox.pack(side=BOTTOM, padx=10, pady=5)
            entryLabel.pack(side=BOTTOM)
            linEncodeWindow.mainloop()
        except:
            linEncodeWindow.destroy()
        
    # linear decoding image window
    def decodeImgLinear():
        def decodeLinear():
            decodingIm = StegoImg(decodePath)
            msg = decodingIm.decode()
            decodedTxtBox.delete("1.0", END)
            decodedTxtBox.insert(END, msg)
          
        try:
            decodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            linDecodeWindow = Toplevel()
            linDecodeWindow.configure(bg=bgColor)
            linDecodeWindow.title("Linear LSB Decoding")
            selectedIm = Image.open(decodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(linDecodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            decodedLabel = Label(linDecodeWindow, text = "Output:", bg=bgColor, fg=txtColor)
            decodedTxtBox = Text(linDecodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            decodeButton = Button(linDecodeWindow, text="Decode!", command=decodeLinear, bg=buttonColor, fg=txtColor)
            decodedTxtBox.pack(side=BOTTOM, padx=10, pady=10)
            decodedLabel.pack(side=BOTTOM, pady=5)
            decodeButton.pack(side=BOTTOM)
            linDecodeWindow.mainloop()    
        except:
            linDecodeWindow.destroy()
        
    # random encode image window
    def encodeImgRandom():
        global encodedPath
        def encodeRandom():
            encodingIm = StegoImg(encodePath)
            msg = entryTxtBox.get("1.0",END)
            password = passwordTxt.get()
            encodedImg = encodingIm.encode(msg, encodedPath, "randomLSB", password)
            ranEncodeWindow.destroy()
            sendImg(encodedImg.filePath)
        
        try:    
            encodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            ranEncodeWindow = Toplevel()
            ranEncodeWindow.configure(bg=bgColor)
            ranEncodeWindow.title("Randomized LSB Encoding")
            selectedIm = Image.open(encodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(ranEncodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            entryLabel = Label(ranEncodeWindow, text = "Enter the text you wish to encode:", bg=bgColor, fg=txtColor)
            entryTxtBox = Text(ranEncodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            passwordTxt = StringVar()
            passwordLabel = Label(ranEncodeWindow, text = "Enter your secret password:", bg=bgColor, fg=txtColor)
            passwordEntry = Entry(ranEncodeWindow, textvariable = passwordTxt, bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            encodeButton = Button(ranEncodeWindow, text="Encode!", command=encodeRandom, bg=buttonColor, fg=txtColor)
            encodeButton.pack(side=BOTTOM, pady=5)
            passwordEntry.pack(side=BOTTOM, pady=5)
            passwordLabel.pack(side=BOTTOM)
            entryTxtBox.pack(side=BOTTOM, padx=10, pady=5)
            entryLabel.pack(side=BOTTOM)
            ranEncodeWindow.mainloop()
        except:
            ranEncodeWindow.destroy()
    
    # random decode image window
    def decodeImgRandom():
        def decodeRandom():
            decodingIm = StegoImg(decodePath)
            password = passwordTxt.get()
            try:
                msg = decodingIm.decode("randomLSB", password)
                decodedTxtBox.delete("1.0", END)
                decodedTxtBox.insert(END, msg)
            except:
                error = Toplevel()
                error.withdraw()
                messagebox.showerror("Error", "Couldn't decode with the given password'")
          
        try:
            decodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            ranDecodeWindow = Toplevel()
            ranDecodeWindow.configure(bg=bgColor)
            ranDecodeWindow.title("Random LSB Decoding")
            selectedIm = Image.open(decodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(ranDecodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            passwordTxt = StringVar()
            passwordLabel = Label(ranDecodeWindow, text = "Enter your secret password:", bg=bgColor, fg=txtColor)
            passwordEntry = Entry(ranDecodeWindow, textvariable = passwordTxt, bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            decodedLabel = Label(ranDecodeWindow, text = "Output:", bg=bgColor, fg=txtColor)
            decodedTxtBox = Text(ranDecodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            decodeButton = Button(ranDecodeWindow, text="Decode!", command=decodeRandom, bg=buttonColor, fg=txtColor)
            decodedTxtBox.pack(side=BOTTOM, padx=10, pady=10)
            decodedLabel.pack(side=BOTTOM)
            decodeButton.pack(side=BOTTOM, pady=5)
            passwordEntry.pack(side=BOTTOM, pady=5)
            passwordLabel.pack(side=BOTTOM)
            ranDecodeWindow.mainloop() 
        except:
            ranDecodeWindow.destroy()
        
    # hiding images inside images window
    def encodeImgImage():
        global encodedPath
        
        def chooseImage():
            global imMsgPath
            imMsgPath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            imMsgTmp = Image.open(imMsgPath)
            w, h = imMsgTmp.size
            imMsg = ImageTk.PhotoImage(imMsgTmp.resize((250,int(250/w*h)), Image.ANTIALIAS))
            entryTxtBox.image = imMsg
            entryTxtBox.delete("1.0",END)
            entryTxtBox.image_create(END, image=imMsg)
            
        def encodeImage():
            encodingIm = StegoImgImage(encodePath)
            encodedImg = encodingIm.encode(imMsgPath,encodedPath)
            imgEncodeWindow.destroy()
            sendImg(encodedImg.filePath)
            
        try:
            encodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            imgEncodeWindow = Toplevel()
            imgEncodeWindow.configure(bg=bgColor)
            imgEncodeWindow.title("Merge Image")
            selectedIm = Image.open(encodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(imgEncodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            entryLabel = Label(imgEncodeWindow, text = "Image that you wish to encode:", bg=bgColor, fg=txtColor)
            entryTxtBox = Text(imgEncodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            chooseImgButton = Button(imgEncodeWindow, text="Choose secret image", command=chooseImage, bg=buttonColor, fg=txtColor)
            encodeButton = Button(imgEncodeWindow, text="Encode!", command=encodeImage, bg=buttonColor, fg=txtColor)
            encodeButton.pack(side=BOTTOM, pady=5)
            entryTxtBox.pack(side=BOTTOM, padx=10, pady=5)
            chooseImgButton.pack(side=BOTTOM, pady=5)
            entryLabel.pack(side=BOTTOM)
            imgEncodeWindow.mainloop()
        except:
            imgEncodeWindow.destroy()
            
    # extracting an image from an image
    def decodeImgImage():
        global decodedPath
        def decodeLinear():
            decodingIm = StegoImgImage(decodePath)
            msg = decodingIm.decode(decodedPath)
            imMsgTmp = Image.open(msg.filePath)
            w, h = imMsgTmp.size
            imMsg = ImageTk.PhotoImage(imMsgTmp.resize((250,int(250/w*h)), Image.ANTIALIAS))
            decodedTxtBox.image = imMsg
            decodedTxtBox.delete("1.0", END)
            decodedTxtBox.image_create(END, image=imMsg)
          
        try:
            decodePath = filedialog.askopenfilename(filetypes = (("png files","*.png"),("all files","*.*")))
            imgDecodeWindow = Toplevel()
            imgDecodeWindow.configure(bg=bgColor)
            imgDecodeWindow.title("Unmerge Image")
            selectedIm = Image.open(decodePath)
            width, height = selectedIm.size
            im = ImageTk.PhotoImage(selectedIm.resize((250,int(250/width*height)), Image.ANTIALIAS))
            imgLabel = Label(imgDecodeWindow, image = im, bg=bgColor)
            imgLabel.pack(side = TOP, fill=BOTH, expand = 1, pady=10)
            decodedLabel = Label(imgDecodeWindow, text = "Output:", bg=bgColor, fg=txtColor)
            decodedTxtBox = Text(imgDecodeWindow, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
            decodeButton = Button(imgDecodeWindow, text="Decode!", command=decodeLinear, bg=buttonColor, fg=txtColor)
            decodedTxtBox.pack(side=BOTTOM, padx=10, pady=10)
            decodedLabel.pack(side=BOTTOM, pady=5)
            decodeButton.pack(side=BOTTOM)
            imgDecodeWindow.mainloop()    
        except:
            imgDecodeWindow.destroy()        
         
    # sends any text message
    def sendMsg(event=None):
        msg = msgInput.get("1.0",END).strip()
        msgInput.delete("1.0",END)
        s.send(str.encode(msg))
    
    # the structure of the send and receive functions is inspired by:
    # https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
    # however, my code deals with the sending and receiving of images in addition to 
    # text messages. My code is extremely modified and I wrote it myself.
    def receiveMsg():
        while True:
            try:
                global imgCounter
                global basename
                global filePath
                global receivedImages
                global receivedCounter
                global sentImages
                global sentCounter
                global receivedPath
                data = s.recv(1024).decode("utf-8")
                if data.startswith("<<<{SIZE}>>>"):
                    size = int(data.split(":")[1])
                    s.send(str.encode("<<<{got size}>>>"))
                    imgBytes = b''
                    while size > 0:
                        data = s.recv(4096)
                        if not data:
                            break
                        size-=len(data)
                        imgBytes+=data
                    savePath = receivedPath+"/"+basename % imgCounter
                    file = open(savePath, "wb+")
                    file.write(imgBytes)
                    file.close()
                    s.send(str.encode("<<<{got image}>>>"))
                elif data=="<<<{GOT SIZE}>>>":
                    file = open(filePath, 'rb')
                    bytes = file.read()
                    s.sendall(bytes)
                    time.sleep(0.5)
                elif data.endswith(" sent you an image!"):
                    chosenIm = Image.open(savePath)
                    w, h = chosenIm.size
                    receivedImages["received"+str(receivedCounter)] = ImageTk.PhotoImage(chosenIm.resize((250,int(250/w*h)), Image.ANTIALIAS))
                    chatBox.configure(state=NORMAL)
                    chatBox.insert(END, data+"\n")
                    chatBox.image_create(END, image=receivedImages["received"+str(receivedCounter)])
                    chatBox.insert(END, "\n")
                    chatBox.configure(state=DISABLED)
                    imgCounter+=1
                    receivedCounter+=1
                elif data=="Image was succesfully sent!":
                    chosenIm = Image.open(filePath)
                    w, h = chosenIm.size
                    sentImages["sent"+str(sentCounter)] = ImageTk.PhotoImage(chosenIm.resize((250,int(250/w*h)), Image.ANTIALIAS))
                    chatBox.configure(state=NORMAL)
                    chatBox.insert(END, data+"\n")
                    chatBox.image_create(END, image=sentImages["sent"+str(sentCounter)])
                    chatBox.insert(END, "\n")
                    chatBox.see(END)
                    chatBox.configure(state=DISABLED)
                    sentCounter+=1
                else:
                    chatBox.configure(state=NORMAL)
                    chatBox.insert(END, data+"\n")
                    chatBox.see(END)
                    chatBox.configure(state=DISABLED)
                
            except:
                break    
    
    # about page function
    def aboutPage():
        def run():
            aboutTxt1 = "Hello!"
            aboutTxt2 = "Welcome to Hide.me!"
            aboutTxt3 = "This is like a normal txt messaging app..."
            aboutTxt4 = "Except users can send secret messages to each other by encoding them in images!"
            aboutTxt5 = "This project was coded by Neel Gandhi for 15-112."
            aboutBox.delete("1.0",END)
            aboutBox.insert(END, aboutTxt1+"\n")
            aboutBox.insert(END, aboutTxt2+"\n")
            aboutBox.insert(END, aboutTxt3+"\n")
            aboutBox.insert(END, aboutTxt4+"\n")
            aboutBox.insert(END, aboutTxt5+"\n")
        
        about = Tk()
        about.configure(bg=bgColor)
        about.title("About")
        
        aboutFrame = Frame(about, bg=bgColor)
        scrollBarA = Scrollbar(aboutFrame)
        aboutBox = Text(aboutFrame, yscrollcommand = scrollBarA.set, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        scrollBarA.config(command=aboutBox.yview)
        scrollBarA.pack(side=RIGHT, fill=Y)
        aboutButton = Button(about, text="Click Here!", command=run, bg=buttonColor, fg=txtColor)
        aboutBox.pack(side=LEFT, fill=BOTH, expand=1)
        aboutFrame.pack(side=BOTTOM, fill=BOTH, expand=1, padx = 5, pady = 5)
        aboutButton.pack(side=TOP, pady=5)
        about.mainloop()
    
    
    # text entry
    entireFrame = Frame(chatScreen, bg=bgColor)
    msgFrame = Frame(entireFrame, bg=bgColor)
    msgInput = Text(msgFrame, height = 1, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
    sendButton = Button(msgFrame, text = "Send", command=sendMsg, bg=buttonColor, fg=txtColor)
    msgInput.bind("<Return>", sendMsg)
    sendButton.pack(side=RIGHT, padx=5)
    msgInput.pack(side=LEFT, fill=X, padx=5)
    msgFrame.pack(side=BOTTOM, pady=5)
    
    # chat (msgs and imgs)
    chatFrame = Frame(entireFrame, bg=bgColor)
    scrollBar = Scrollbar(chatFrame)
    chatBox = Text(chatFrame, yscrollcommand = scrollBar.set, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
    scrollBar.config(command=chatBox.yview)
    scrollBar.pack(side=RIGHT, fill=Y)
    chatBox.pack(side=LEFT, fill=BOTH, expand=1)
    chatFrame.pack(side=TOP, fill=BOTH, expand=1, padx = 5, pady = 5)
    entireFrame.pack(fill=BOTH, expand=1, padx=5, pady=5)
    
    # docs page function
    def docsPage():
        docs = Tk()
        docs.configure(bg=bgColor)
        docs.title("Documentation")
        
        
        docsFrame = Frame(docs, bg=bgColor)
        scrollBarD = Scrollbar(docsFrame)
        docsBox = Text(docsFrame, yscrollcommand = scrollBarD.set, wrap="word", bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        scrollBarD.config(command=docsBox.yview)
        scrollBarD.pack(side=RIGHT, fill=Y)
        docsBox.pack(side=LEFT, fill=BOTH, expand=1)
        docsFrame.pack(side=BOTTOM, fill=BOTH, expand=1, padx = 5, pady = 5)
        
        docsTxt = """Documentation:
        
Click any of the button in the menu bar above to discover their features!
        """
        
        dTxt1 = """File--> Connect 
        
This exits the chat and returns you to the connect screen, where you can connect to a different server and port."""
        
        dTxt2 = """File--> SendImg 
        
Short Explanation: Users select an image from their computer and send it.
        
Long Explanation:
This prompts a user to select an image to send. Once the user selects an image, a window will pop up displaying the selected image. The user must confirm "Yes" to send the image.
        
The image is sent through sockets using a three way confirmation. First, the size of the image is sent to the server. The server then sends a response indicating it has received the size of the image. Then the client sends all the data bits of the image in small packets until the entire image is sent. Finally, the server responds back indicating that it has succesfully received the image. The same 3-way confirmation process is used to transfer the image from the server to the other client."""
        
        dTxt3 = """File--> Exit 
        
This safely closes the app and terminates the connection to the server."""
        
        dTxt4 = """Steganography--> Encode--> Linear LSB
        
Short Explanation: Users can select and image, type their secret message, and send the encoded image.
        
Long Explanation:
This prompts the user to select an image that they wish to encode a secret txt message inside. A window will then pop up displaying the image and an empty text box where they user can type in the message they want to hide. Upon clicking the encode button, the user is prompted with another window to confirm if they wish to send the encoded image.
        
The Linear LSB algorithm works by converting the the text message into its binary form, and then looping through each row and column of the image to alter the pixel values by the bits of the secret message."""
        
        dTxt5 = """Steganography--> Encode--> Randomized LSB
        
Short Explanation: Users can select an image, type their secret message and a secret password, and sent the encoded image.
        
Long Explanation:
This prompts the user to select an image that they wish to encode a secret txt message inside. A window will then pop up displaying the image and two empty text boxes (one for typing the message and the other for typing a secret password). Upon clicking the encode button, the user is prompted with another window to confirm if they wish to send the encoded image.
        
The Randomized LSB algorithm works by converting the the text message into its binary form, and then pseudo-randomly selecting the pixels in the image to be altered to hide the message. The list of the coordinates of this image is encrypted using an altered Vigenere cipher with the password inputted by the user, and it is then linearly encoded into the image."""
        
        dTxt6 = """Steganography--> Encode--> Merge image
        
Short Explanation: Users can select two images, one of which will be hidden inside the other, and send the encoded image. 
        
Long Explanation:
This prompts the user to select an image that they wish to encode another image inside. A window will then pop up displaying the image, as well as button that, when clicked, allows the user to select the image they want to hide inside. The selected image then appears inside a text box on the window. Upon clicking the encode button, the user is prompted with another window to confirm if they wish to send the encoded image.
        
The Merge Image algorithm works by merging the first four bits of the each pixel of the two images so that the first four bits are of the host image and the last 4 bits are of the secret image. This method does result in lower image quality and some artifacts, but it is much faster and is able to store larger images compared to other methods."""
        
        dTxt7 = """Steganography--> Decode--> Linear LSB
        
Short Explanation: Users select an image and decode it to reveal a secret message.
        
Long Explanation:
This prompts the user to select an image that they wish to decode. A window will then pop up displaying the image and upon pressing the decode button, the secret message is outputted in a text box.
        
The Linear LSB algorithm works by looping through each pixel and extracting the last bit and appending it to a string until it reaches a stop sequence of 20 zeroes. These bits are then translated into ascii characters."""
        
        dTxt8 = """Steganography--> Decode--> Randomized LSB
        
Short Explanation: Users select an image, enter the password, and decode it to reveal a secret message.
        
Long Explanation:
This prompts the user to select an image that they wish to decode. A window will then pop up displaying the image and two empty text boxes (one for typing a secret password and the other for the output message). Upon clicking the decode button, the message is displayed in a textbox.
        
The Randomized LSB algorithm works by extracting an encrypted coordinates list from the image using the linear algorithm, unencryptng it using the Vigenere Cipher and the password, and then looping through all the coordinates to extract the last bit from each pixel. This binary string is then converted to ascii characters."""
        
        dTxt9 = """Steganography--> Decode--> Merge image
        
Short Explanation: Users select an image and decode it to reveal a secret image hidden inside.
        
Long Explanation:
This prompts the user to select an image that they wish to decode. A window will then pop up displaying the image and upon pressing the decode button, the secret image is outputted in a text box.
        
The Merge Image algorithm works by extracting the last 4 bits of every pixel and adding the bits "1000" to the end to create a new pixel value. These pixels are then accumulated to create the output image. The output image will have artifacts due to losing the last four bits, but it attempts to mitigate the loss by putting an average value for the last 4 bits."""
        
        dTxt10 = """Themes-->
There are a variety of themes to choose from: Default, Hacker, Light, Ocean, Grass, and Dim. Changing the theme will change any pop-up windows as well."""
        
        dTxt11 = """Help--> Documentation
        
You are here!"""
        
        dTxt12 = """Help--> About 
        
Displays a brief desription of the app.
        """
        def connectDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt1)
        def imgDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt2)
        def closeDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt3)
        def encodeImgLinearDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt4)
        def encodeImgRandomDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt5)
        def encodeImgImageDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt6)
        def decodeImgLinearDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt7)
        def decodeImgRandomDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt8)
        def decodeImgImageDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt9)
        def themerDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt10)
        def documentationDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt11)
        def aboutPageDocs():
            docsBox.delete("1.0",END)
            docsBox.insert(END, dTxt12)
        menubarD = Menu(docs)
        
        filemenuD = Menu(menubarD, tearoff=0)
        filemenuD.add_command(label="Connect", command=connectDocs)
        filemenuD.add_command(label="Send Image", command=imgDocs)
        filemenuD.add_separator()
        filemenuD.add_command(label="Exit", command=closeDocs)
        menubarD.add_cascade(label="File", menu=filemenuD)
        
        stegmenuD = Menu(menubarD, tearoff=0)
        menubarD.add_cascade(label="Steganography", menu=stegmenuD)
        
        encodemenuD = Menu(stegmenuD, tearoff=0)
        encodemenuD.add_command(label="Linear LSB", command=encodeImgLinearDocs)
        encodemenuD.add_command(label="Randomized LSB", command=encodeImgRandomDocs)
        encodemenuD.add_command(label="Merge Image", command=encodeImgImageDocs)
        stegmenuD.add_cascade(label = "Encode Image", menu = encodemenuD)
        
        decodemenuD = Menu(stegmenuD, tearoff=0)
        decodemenuD.add_command(label="Linear LSB", command=decodeImgLinearDocs)
        decodemenuD.add_command(label="Randomized LSB", command=decodeImgRandomDocs)
        decodemenuD.add_command(label="Unmerge Image", command=decodeImgImageDocs)
        stegmenuD.add_cascade(label = "Decode Image", menu = decodemenuD)
        
        thememenuD = Menu(menubarD, tearoff=0)
        thememenuD.add_command(label="Default", command=themerDocs)
        thememenuD.add_command(label="Hacker", command=themerDocs)
        thememenuD.add_command(label="Light", command=themerDocs)
        thememenuD.add_command(label="Ocean", command=themerDocs)
        thememenuD.add_command(label="Grass", command=themerDocs)
        thememenuD.add_command(label="Dim", command=themerDocs)
        menubarD.add_cascade(label="Themes", menu=thememenuD)
        
        helpmenuD = Menu(menubarD, tearoff=0)
        helpmenuD.add_command(label="Documentation", command=documentationDocs)
        helpmenuD.add_command(label="About", command=aboutPageDocs)
        menubarD.add_cascade(label="Help", menu=helpmenuD)
        
        docs.config(menu=menubarD)    
        
        docsBox.insert(END, docsTxt)
        docs.mainloop()

    # theming Functions
    def themerHacker():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor= "#333333"
        buttonColor = "#505050"
        txtColor = "#FFFFFF"
        chatColor = "#000000"
        chatTxtColor = "#20C20E"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)    
            
    def themerLight():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor = "#eeeeee"
        buttonColor = "#eeeeee"
        txtColor = "#000000"
        chatColor = "#FFFFFF"
        chatTxtColor = "#000000"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
    
    def themerOcean():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor = "#6da5ff"
        buttonColor = "#0077be"
        txtColor = "#FFFFFF"
        chatColor = "#0077be"
        chatTxtColor = "#FFFFFF"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
    
    def themerGrass():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor = "#4CAF50"
        buttonColor = "#FF9800"
        txtColor = "#FFFFFF"
        chatColor = "#388E3C"
        chatTxtColor = "#FFFFFF"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
    
    def themerDim():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor = "#607D8B"
        buttonColor = "#9E9E9E"
        txtColor = "#FFFFFF"
        chatColor = "#455A64"
        chatTxtColor = "#FFFFFF"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor) 
            
    def themerDefault():
        global bgColor
        global buttonColor
        global txtColor
        global chatColor
        global chatTxtColor
        bgColor = "#009688"
        buttonColor = "#FF5722"
        txtColor = "#FFFFFF"
        chatColor = "#FFFFFF"
        chatTxtColor = "#000000"
        chatScreen.configure(bg=bgColor)
        entireFrame.configure(bg=bgColor)
        msgFrame.configure(bg=bgColor)
        msgInput.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        sendButton.configure(bg=buttonColor, fg=txtColor)
        chatFrame.configure(bg=bgColor)
        chatBox.configure(bg=chatColor, fg=chatTxtColor, insertbackground=chatTxtColor)
        
        
    # menubar
    menubar = Menu(chatScreen)
    
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Connect", command=newConnect)
    filemenu.add_command(label="Send Image", command=sendImg)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=close)
    menubar.add_cascade(label="File", menu=filemenu)
    
    stegmenu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Steganography", menu=stegmenu)
    
    encodemenu = Menu(stegmenu, tearoff=0)
    encodemenu.add_command(label="Linear LSB", command=encodeImgLinear)
    encodemenu.add_command(label="Randomized LSB", command=encodeImgRandom)
    encodemenu.add_command(label="Merge Image", command=encodeImgImage)
    stegmenu.add_cascade(label = "Encode Image", menu = encodemenu)
    
    decodemenu = Menu(stegmenu, tearoff=0)
    decodemenu.add_command(label="Linear LSB", command=decodeImgLinear)
    decodemenu.add_command(label="Randomized LSB", command=decodeImgRandom)
    decodemenu.add_command(label="Unmerge Image", command=decodeImgImage)
    stegmenu.add_cascade(label = "Decode Image", menu = decodemenu)
    
    thememenu = Menu(menubar, tearoff=0)
    thememenu.add_command(label="Default", command=themerDefault)
    thememenu.add_command(label="Hacker", command=themerHacker)
    thememenu.add_command(label="Light", command=themerLight)
    thememenu.add_command(label="Ocean", command=themerOcean)
    thememenu.add_command(label="Grass", command=themerGrass)
    thememenu.add_command(label="Dim", command=themerDim)
    menubar.add_cascade(label="Themes", menu=thememenu)
    
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Documentation", command=docsPage)
    helpmenu.add_command(label="About", command=aboutPage)
    menubar.add_cascade(label="Help", menu=helpmenu)
    
    chatScreen.config(menu=menubar)    
        
    # Initialization
    receiving = Thread(target=receiveMsg)
    receiving.start()
    chatScreen.protocol("WM_DELETE_WINDOW", close)
    chatScreen.mainloop()
    

start()