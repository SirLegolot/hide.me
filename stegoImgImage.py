# Steganography for hiding images inside images
# unless otherwise indicated, this code was written by myself

from PIL import Image
import imghdr
import math
import ast
import random

class StegoImgImage():
    def __init__(self, filePath):
        self.filePath = filePath
        self.imgType = imghdr.what(filePath)
        with Image.open(filePath) as tmpImg:
            self.imgMode = "".join(tmpImg.getbands())
            
    def alterPixelRGB(self, pixel1, pixel2):
        r1, g1, b1 = pixel1
        r2, g2, b2 = pixel2
        newR = int((str(bin(r1)[2:]).zfill(8))[:4]+(str(bin(r2)[2:]).zfill(8))[:4],2)
        newG = int((str(bin(g1)[2:]).zfill(8))[:4]+(str(bin(g2)[2:]).zfill(8))[:4],2)
        newB = int((str(bin(b1)[2:]).zfill(8))[:4]+(str(bin(b2)[2:]).zfill(8))[:4],2)
        newPixel = (newR,newG,newB)
        return newPixel
        
    def alterPixelRGBA(self, pixel1, pixel2):
        r1, g1, b1, a1 = pixel1
        r2, g2, b2, a2 = pixel2
        newR = int((str(bin(r1)[2:]).zfill(8))[:4]+(str(bin(r2)[2:]).zfill(8))[:4],2)
        newG = int((str(bin(g1)[2:]).zfill(8))[:4]+(str(bin(g2)[2:]).zfill(8))[:4],2)
        newB = int((str(bin(b1)[2:]).zfill(8))[:4]+(str(bin(b2)[2:]).zfill(8))[:4],2)
        newPixel = (newR,newG,newB, a1)
        return newPixel
    
    def encodeRGB(self, imgHostPath, imgMsgPath, savePath):
        imHost = Image.open(imgHostPath)
        if ("".join(imHost.getbands()))=="L":
            imHost = Image.open(imgHostPath).convert("RGB")
        imMsg = Image.open(imgMsgPath)
        if ("".join(imMsg.getbands()))=="L":
            imMsg = Image.open(imgMsgPath).convert("RGB")
        elif ("".join(imMsg.getbands()))=="RGB":
            pass
        elif ("".join(imMsg.getbands()))=="RGBA":
            # taken from: 
            # https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
            imMsg.load()
            tmpIm = Image.new("RGB",imMsg.size, (255,255,255))
            tmpIm.paste(imMsg, mask = imMsg.split()[3])
            imMsg = tmpIm
        else:
            Exception("Image that is being encoded must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        hostW, hostH = imHost.size
        width, height = imMsg.size
        if width+5>hostW or height+5>hostH:
            raise Exception("Cannot hide an image that is large than the carrier image.")
        newIm = imHost.copy()
        for row in range(width+5):
            for col in range(height+5):
                hostPixel = imHost.getpixel((row,col))
                try:
                    msgPixel = imMsg.getpixel((row,col))
                except:
                    msgPixel = (136,136,136)
                newPixel = self.alterPixelRGB(hostPixel,msgPixel)
                newIm.putpixel((row, col), newPixel)
        tmpPathString = imgHostPath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm.save(newImagePath)
        adjImg = StegoImgImage(newImagePath)
        return adjImg
        
    def encodeRGBA(self, imgHostPath, imgMsgPath, savePath):
        imHost = Image.open(imgHostPath)
        imMsg = Image.open(imgMsgPath)
        if ("".join(imMsg.getbands()))=="L":
            imMsg = Image.open(imgMsgPath).convert("RGBA")
        elif ("".join(imMsg.getbands()))=="RGB":
            imMsg = Image.open(imgMsgPath).convert("RGBA")
        elif ("".join(imMsg.getbands()))=="RGBA":
            pass
        else:
            Exception("Image that is being encoded must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        hostW, hostH = imHost.size
        width, height = imMsg.size
        if width+5>hostW or height+5>hostH:
            raise Exception("Cannot hide an image that is large than the carrier image.")
        newIm = imHost.copy()
        for row in range(width+5):
            for col in range(height+5):
                hostPixel = imHost.getpixel((row,col))
                try:
                    msgPixel = imMsg.getpixel((row,col))
                except:
                    msgPixel = (136,136,136, hostPixel[3])
                newPixel = self.alterPixelRGBA(hostPixel,msgPixel)
                newIm.putpixel((row, col), newPixel)
        tmpPathString = imgHostPath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_adjusted."+tmpPathString[1]
        newIm.save(newImagePath)
        adjImg = StegoImgImage(newImagePath)
        return adjImg
        
        
    def extractPixelRGB(self, pixel):
        r,g,b = pixel
        newR = int((str(bin(r)[2:]).zfill(8))[4:]+"1000",2)
        newG = int((str(bin(g)[2:]).zfill(8))[4:]+"1000",2)
        newB = int((str(bin(b)[2:]).zfill(8))[4:]+"1000",2)
        newPixel = (newR,newG,newB)
        return newPixel
        
    def extractPixelRGBA(self, pixel):
        r,g,b,a = pixel
        newR = int((str(bin(r)[2:]).zfill(8))[4:]+"1000",2)
        newG = int((str(bin(g)[2:]).zfill(8))[4:]+"1000",2)
        newB = int((str(bin(b)[2:]).zfill(8))[4:]+"1000",2)
        newPixel = (newR,newG,newB,255)
        return newPixel

    def decodeRGB(self, imgPath, savePath):
        im = Image.open(imgPath)
        width, height = im.size
        widthCount=0
        heightCount=0
        newWidth=width
        newHeight=height
        for i in range(width):
            pixel = self.extractPixelRGB(im.getpixel((i,1)))
            if pixel==(136,136,136):
                widthCount+=1
            else:
                widthCount=0
            if widthCount==5:
                newWidth = i-5
        for j in range(height):
            pixel = self.extractPixelRGB(im.getpixel((1,j)))
            if pixel==(136,136,136):
                heightCount+=1
            else:
                heightCount=0
            if heightCount==5:
                newHeight = j-5
        newIm = Image.new("RGB", (newWidth+1,newHeight+1))
        for row in range(newWidth+1):
            for col in range(newHeight+1):
                pixel = im.getpixel((row,col))
                newPixel = self.extractPixelRGB(pixel)
                newIm.putpixel((row,col),newPixel)
        tmpPathString = imgPath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_revealed."+tmpPathString[1]
        newIm.save(newImagePath)
        outputImg = StegoImgImage(newImagePath)
        return outputImg
        
    def decodeRGBA(self, imgPath, savePath):
        im = Image.open(imgPath)
        width, height = im.size
        widthCount=0
        heightCount=0
        newWidth=width
        newHeight=height
        for i in range(width):
            pixel = self.extractPixelRGBA(im.getpixel((i,1)))
            if pixel==(136,136,136,255):
                widthCount+=1
            else:
                widthCount=0
            if widthCount==5:
                newWidth = i-5
        for j in range(height):
            pixel = self.extractPixelRGBA(im.getpixel((1,j)))
            if pixel==(136,136,136,255):
                heightCount+=1
            else:
                heightCount=0
            if heightCount==5:
                newHeight = j-5
        newIm = Image.new("RGBA", (newWidth+1,newHeight+1))
        for row in range(newWidth+1):
            for col in range(newHeight+1):
                pixel = im.getpixel((row,col))
                newPixel = self.extractPixelRGBA(pixel)
                newIm.putpixel((row,col),newPixel)
        tmpPathString = imgPath.split("/")[-1].split(".")
        newImagePath = savePath+"/"+tmpPathString[0]+"_revealed."+tmpPathString[1]
        newIm.save(newImagePath)
        outputImg = StegoImgImage(newImagePath)
        return outputImg
        
    def encode(self, imgMsgPath, savePath):
        if self.imgType not in {"png", "tiff", "bmp"}:
            raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
        if self.imgMode == "RGB":
            newImg = self.encodeRGB(self.filePath, imgMsgPath, savePath)
        elif self.imgMode == "RGBA":
            newImg = self.encodeRGBA(self.filePath, imgMsgPath, savePath)
        elif self.imgMode == "L":
            # i'll be converting the grayscale image to RGB in the function
            newImg = self.encodeRGB(self.filePath, imgMsgPath, savePath)
        else:
            raise Exception("Image must be have one of these modes: 'L', 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        return newImg
            
    def decode(self, savePath):
        if self.imgType not in {"png", "tiff", "bmp"}:
            raise Exception("Image must be a lossless compression format ('png', 'tiff', 'bmp') for LSB. The image type was '{}'".format(self.imgType))
        if self.imgMode == "RGB":
            newImg = self.decodeRGB(self.filePath, savePath)
        elif self.imgMode == "RGBA":
            newImg = self.decodeRGBA(self.filePath, savePath)
        else:
            raise Exception("Image must be have one of these modes: 'RGB', or 'RGBA'. The mode of selected image was '{}'".format(self.imgMode))
        return newImg
            