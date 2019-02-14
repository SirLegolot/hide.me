Hide.Me
Created by Neel Gandhi

Description:
This is a messaging application that allows users to hide secret messages and images inside other images
without any visual changes using a process called Steganography. To a person who happens to glimpse at the
app, all they would see are normal images being sent from one person to another, not realizing that there
are secret messages being transferred within the images. 


HOW TO RUN THE PROJECT:

First there needs to be a computer that is the desginated server. Run the "Chat Server.py" file on that 
computer after changing the host(IP address) in the code to the IP address of the computer. It is indicated
in the file where the IP address goes.

For the clients, you can run it on any computer that is connected to the same network as the server. 
The computers that will run the application will have to install pillow in python ("pip install pillow"). 
Make sure that the  "stegoImgTxt.py" and the "stegoImgImage.py" files are in the same directory as 
"Chat Client.py". Clients will run this file.

The only images that can be sent and received are png, bmp, and tiff images because they are lossless
compression formats which are not subject to compression and loss of the least significant bits of the 
pixel values in an image. In the program itself, I have set it to only accept png files since this is
the most common of the 3 types of images above.

There are also some limitation as to the band types of the images. You can only use images that are 
grayscale(type L only... not type I, which is 16 bits, or type P), RGB, or RGBA(RGB with transparency).


HOW TO USE THE APP:
Once you connect to a server, click the help tab and then click documentation. This will give an
explanation for all the features in the app.

VIDEO DEMO:
https://youtu.be/tNvcPIFNuao