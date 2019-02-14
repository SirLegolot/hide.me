#Steganography for hiding text inside images

from PIL import Image
import imghdr
import math
import ast
import random

# the structure of the for loops for the encoding functions was inspired by:
# https://hackernoon.com/simple-image-steganography-in-python-18c7b534854f
# particularly how an iterator is used to iterate through the bits of the secret message


class StegoImg():
    def __init__(self, filePath):
        self.filePath = filePath
        self.imgType = imghdr.what(filePath)
        with Image.open(filePath) as tmpImg:
            self.imgMode = "".join(tmpImg.getbands())
            
    ### Encode Section ###
        
    def getASCII(self,s):
        binary = ""
        for char in s:
            binary+=str(bin(ord(char))[2:].zfill(8))
        return binary
    
    def alterPixel(self, value, bit):
        listValue = list(bin(value)[2:])
        listValue[-1] = bit
        binResult = ""
        for num in listValue:
            binResult+=str(num)
        result = int(binResult, 2)
        return result
        
    def randomize(self, width, height, binMsg, pixelWeight):
        numChoices = math.ceil(len(binMsg)/pixelWeight)
        coordSet = set()
        while len(coordSet)<numChoices:
            newCoord = (random.randint(width//2,width-1), random.randint(0,height-1))
            if newCoord not in coordSet:
                coordSet.add(newCoord)
        coordList = list(coordSet)
        return coordList
    
    def jumble(self, lst, key):
        s = str(lst).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","")
        jumbledString = ""
        for i in range(len(s)):
            jumbledString+=chr(((ord(s[i])+ord(key[i%len(key)]))%126)+33)
        return jumbledString
    
    def encodeMsgLinearLSB_L(self, imagePath, msg, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        newIm = im.copy()
        zeroCount = 0
        for row in range(width):
            for col in range(height):
                grd = im.getpixel((row,col))
                nextBit = next(iterBinMsg,0)
                newGrd = self.alterPixel(grd, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                newIm.putpixel((row, col), (newGrd))
                if zeroCount >20:
                    tmpPathString = imagePath.split("/")[-1].split(".")
                    newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
                    newIm.save(newImagePath)
                    adjImg = StegoImg(newImagePath)
                    return adjImg
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg
        
    def encodeMsgRandomLSB_L(self, imagePath, msg, key, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height/2<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        coordList = self.randomize(width, height, binMsg, 1)
        keyString = self.jumble(coordList, key)
        self.encodeMsgLinearLSB_L(imagePath,keyString, savePath)
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm = Image.open(newImagePath)
        finalIm = newIm.copy()
        for coord in coordList:
            grd = newIm.getpixel(coord)
            newGrd = self.alterPixel(grd, next(iterBinMsg,0))
            finalIm.putpixel(coord, (newGrd))
        finalIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg
    
    def encodeMsgLinearLSB_RGB(self, imagePath, msg, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height*3<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        newIm = im.copy()
        zeroCount = 0
        for row in range(width):
            for col in range(height):
                r,g,b = im.getpixel((row,col))
                nextBit = next(iterBinMsg,0)
                newR = self.alterPixel(r, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                nextBit = next(iterBinMsg,0)
                newG = self.alterPixel(g, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                nextBit = next(iterBinMsg,0)
                newB = self.alterPixel(b, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                newIm.putpixel((row, col), (newR, newG, newB))
                if zeroCount >20:
                    tmpPathString = imagePath.split("/")[-1].split(".")
                    newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
                    newIm.save(newImagePath)
                    adjImg = StegoImg(newImagePath)
                    return adjImg
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg
        
    def encodeMsgRandomLSB_RGB(self, imagePath, msg, key, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height*3/2<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        coordList = self.randomize(width, height, binMsg, 3)
        keyString = self.jumble(coordList, key)
        self.encodeMsgLinearLSB_RGB(imagePath,keyString, savePath)
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm = Image.open(newImagePath)
        finalIm = newIm.copy()
        for coord in coordList:
            r,g,b = newIm.getpixel(coord)
            newR = self.alterPixel(r, next(iterBinMsg,0))
            newG = self.alterPixel(g, next(iterBinMsg,0))
            newB = self.alterPixel(b, next(iterBinMsg,0))
            finalIm.putpixel(coord, (newR, newG, newB))
        finalIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg

    def encodeMsgLinearLSB_RGBA(self, imagePath, msg, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height*3<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        newIm = im.copy()
        zeroCount = 0
        for row in range(width):
            for col in range(height):
                r,g,b,a = im.getpixel((row,col))
                nextBit = next(iterBinMsg,0)
                newR = self.alterPixel(r, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                nextBit = next(iterBinMsg,0)
                newG = self.alterPixel(g, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                nextBit = next(iterBinMsg,0)
                newB = self.alterPixel(b, nextBit)
                if nextBit == "1":
                    zeroCount = 0
                else:
                    zeroCount +=1
                newIm.putpixel((row, col), (newR, newG, newB))
                if zeroCount >20:
                    tmpPathString = imagePath.split("/")[-1].split(".")
                    newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
                    newIm.save(newImagePath)
                    adjImg = StegoImg(newImagePath)
                    return adjImg
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg
    
    def encodeMsgRandomLSB_RGBA(self, imagePath, msg, key, savePath):
        binMsg = self.getASCII(msg)
        iterBinMsg = iter(binMsg)
        im = Image.open(imagePath)
        width, height = im.size
        if width*height*3/2<len(binMsg):
            raise Exception("Cannot hide a message that is too large for the image")
        coordList = self.randomize(width, height, binMsg, 3)
        keyString = self.jumble(coordList, key)
        self.encodeMsgLinearLSB_RGBA(imagePath,keyString, savePath)
        tmpPathString = imagePath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm = Image.open(newImagePath)
        finalIm = newIm.copy()
        for coord in coordList:
            r,g,b,a = newIm.getpixel(coord)
            newR = self.alterPixel(r, next(iterBinMsg,0))
            newG = self.alterPixel(g, next(iterBinMsg,0))
            newB = self.alterPixel(b, next(iterBinMsg,0))
            finalIm.putpixel(coord, (newR, newG, newB, a))
        finalIm.save(newImagePath)
        adjImg = StegoImg(newImagePath)
        return adjImg
        
    ### Decode section ###
    
    def getString(self, bits):
        binLetters = []
        for i in range(0,len(bits), 8):
            if i+8<len(bits):
                binLetters.append(bits[i:i+8])
            else:
                binLetters.append(bits[i:])
        msg = ""
        for i in range(len(binLetters)):
            if "1" in binLetters[i]:
                msg += chr(int(binLetters[i],2))
        return msg
    
    def unjumble(self, s, key):
        unjumbledString = ""
        for i in range(len(s)):
            unjumbledString+=chr((ord(s[i])-ord(key[i%len(key)])-33)%126)
        unjumbledList = list(map(int,unjumbledString.split(",")))
        coordList = []
        for i in range(0,len(unjumbledList),2):
            coordList.append((unjumbledList[i],unjumbledList[i+1]))
        return coordList
    
    def decodeMsgLinearLSB_L(self):
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        # structure of the for loops for the decoding functions was also inspired by:
        # https://hackernoon.com/simple-image-steganography-in-python-18c7b534854f 
        # this was altered to be much quicker by creating a flag of 20+ zeroes
        # to signify that the entire message data has been read
        for row in range(width):
            for col in range(height):
                grd = im.getpixel((row,col))
                bits+=bin(grd)[-1]
                try:
                    if bits[-20:]==("0"*20):
                        msg = self.getString(bits)
                        return msg
                except:
                    pass
        msg = self.getString(bits)
        return msg
        
    def decodeMsgRandomLSB_L(self, key):
        keyString = self.decodeMsgLinearLSB_L()
        keyList = self.unjumble(keyString, key)
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        for item in keyList:
            grd = im.getpixel(item)
            bits+=bin(grd)[-1]
        msg = self.getString(bits)
        return msg
    
    def decodeMsgLinearLSB_RGB(self):
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        for row in range(width):
            for col in range(height):
                r,g,b = im.getpixel((row,col))
                bits+=bin(r)[-1]
                bits+=bin(g)[-1]
                bits+=bin(b)[-1]
                try:
                    if bits[-20:]==("0"*20):
                        msg = self.getString(bits)
                        return msg
                except:
                    pass
        msg = self.getString(bits)
        return msg
    
    def decodeMsgRandomLSB_RGB(self, key):
        keyString = self.decodeMsgLinearLSB_RGB()
        keyList = self.unjumble(keyString, key)
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        for item in keyList:
            r,g,b = im.getpixel(item)
            bits+=bin(r)[-1]
            bits+=bin(g)[-1]
            bits+=bin(b)[-1]
        msg = self.getString(bits)
        return msg
    
    def decodeMsgLinearLSB_RGBA(self):
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        for row in range(width):
            for col in range(height):
                r,g,b,a = im.getpixel((row,col))
                bits+=bin(r)[-1]
                bits+=bin(g)[-1]
                bits+=bin(b)[-1]
                try:
                    if bits[-20:]==("0"*20):
                        msg = self.getString(bits)
                        return msg
                except:
                    pass
        msg = self.getString(bits)
        return msg
    
    def decodeMsgRandomLSB_RGBA(self, key):
        keyString = self.decodeMsgLinearLSB_RGBA()
        keyList = self.unjumble(keyString, key)
        im = Image.open(self.filePath)
        width, height = im.size
        bits = ""
        for item in keyList:
            r,g,b,a = im.getpixel(item)
            bits+=bin(r)[-1]
            bits+=bin(g)[-1]
            bits+=bin(b)[-1]
        msg = self.getString(bits)
        return msg
    
    ### Overarching encode/decode functions ###
    
    def encode(self, msg, savePath, method="linearLSB", key=None):
        if method=="linearLSB":
            if self.imgType not in {"png", "tiff", "bmp"}:
                raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
            if self.imgMode == "L":
                newImg = self.encodeMsgLinearLSB_L(self.filePath, msg, savePath)
            elif self.imgMode == "RGB":
                newImg = self.encodeMsgLinearLSB_RGB(self.filePath, msg, savePath)
            elif self.imgMode == "RGBA":
                newImg = self.encodeMsgLinearLSB_RGBA(self.filePath, msg, savePath)
            else:
                raise Exception("Image must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
            return newImg
        elif method=="randomLSB":
            if self.imgType not in {"png", "tiff", "bmp"}:
                raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
            if self.imgMode == "L":
                newImg = self.encodeMsgRandomLSB_L(self.filePath, msg, key, savePath)
            elif self.imgMode == "RGB":
                newImg = self.encodeMsgRandomLSB_RGB(self.filePath, msg, key, savePath)
            elif self.imgMode == "RGBA":
                newImg = self.encodeMsgRandomLSB_RGBA(self.filePath, msg, key, savePath)
            else:
                raise Exception("Image must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
            return newImg
        elif method=="DFT":
            pass
            # perform discrete fourier transform LSB
            # IDK how to do this
        elif method=="DCT":
            pass
            # perform discrete cosine transform LSB
            # IDK how to do this
        
            
    def decode(self, method="linearLSB", key = None):
        if method=="linearLSB":
            if self.imgType not in {"png", "tiff", "bmp"}:
                raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
            if self.imgMode == "L":
                message = self.decodeMsgLinearLSB_L()
            elif self.imgMode == "RGB":
                message = self.decodeMsgLinearLSB_RGB()
            elif self.imgMode == "RGBA":
                message = self.decodeMsgLinearLSB_RGBA()
            else:
                raise Exception("Image must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        elif method=="randomLSB":
            if self.imgType not in {"png", "tiff", "bmp"}:
                raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
            if self.imgType not in {"png", "tiff", "bmp"}:
                raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
            if self.imgMode == "L":
                message = self.decodeMsgRandomLSB_L(key)
            elif self.imgMode == "RGB":
                message = self.decodeMsgRandomLSB_RGB(key)
            elif self.imgMode == "RGBA":
                message = self.decodeMsgRandomLSB_RGBA(key)
            else:
                raise Exception("Image must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        elif method=="DFT":
            pass
            # perform discrete fourier transform LSB
            # IDK how to do this
        elif method=="DCT":
            pass
            # perform discrete cosine transform LSB
            # IDK how to do this
        return message