"""
create directory json file and save
store all the images in that directory in a seperate txt file
search through the directory for recently added images

"""
import os
import json
import model
import time
from PIL import Image
#folderPathway = []
folderPathway = '/Users/hari/Desktop/image grouping/images'

def getPathDirectory(folderPath):
    if os.path.exists('/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt'):
        print("file exists")
        #f = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","r" )
        #print(f.read())
        #rere = f.read()
        #.join(rere)
        read_json = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","r")
        pathJson = json.load(read_json)
        print(pathJson)
        print("whats in the text file:")        
        if pathJson == folderPath:
            read_json.close()
            print("the path in the file is the same")
        else:
            read_json.close()
            f = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","w")
            json.dump(folderPath,f)
            print("wrote the path to the text file")
            f.close()    
    
    else:
        f = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","w")
        # f.write("hello")
        # print(f.readlines())
        # f.close()
        json.dump(folderPath,f)
        print("wrote the path to the text file")
        f.close()  

def openImageDirJson():
    f = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","r")
    pathJson = json.load(f)
    f.close()
    return pathJson

def getImages(dir,valid_images = [".jpg",".gif",".png",".jpeg"]):
    images=[]
    # if not images:
    #     print("the list is empty")
    #     return None
        

    for f in os.listdir(dir):
        #files.append(os.path.join(dir,f))
        ext = os.path.splitext(f)[1]
        
        if ext.lower() not in valid_images:
            print(ext)
        if ext.lower() in valid_images:
            images.append(os.path.join(dir,f))
    
    return images

def setOriginalJsonImageData():
    imageDir = openImageDirJson()
    images = getImages(imageDir)
    
    imagesData = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/originalImagesData.txt","w")
    json.dump(images,imagesData)
    imagesData.close()

def getNewJsonImageData():
    imageDir = openImageDirJson()
    images = getImages(imageDir)
    imagesData = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/newImagesData.txt","w")
    json.dump(images,imagesData)
    imagesData.close()

def compareImageFile():

    originalImages = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/originalImagesData.txt", "r")
    originalPath = json.load(originalImages)
    originalImages.close()

    newImages = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/newImagesData.txt","r")
    newImagesPath = json.load(newImages)
    newImages.close()

    #for images in newImagesPath:

    if originalPath == newImagesPath:
        print("the images are the same")
    else:
        print("not the same")


def sortImages(direc):
    #currenttime = 0
    list = getImages(direc)
    # for i in os.listdir(direc):
    #     imgStat = os.stat(os.path.join(direc,i))
    #     if imgStat.st_birthtime > currenttime:
    #         currenttime = imgStat.st_birthtime
    #         list.append(os.path.join(direc,i))
    #     else:
    #         list.insert(0,os.path.join(direc,i))
    lists = sorted(list,key=os.path.getctime,reverse=True)
    for i in os.listdir(direc):
        imgStat = os.path.join(direc,i)
        print(imgStat)
        print(time.ctime(os.path.getctime(imgStat)))
        print("now to print out in order:")
        for x in range(len(lists)):
            print(lists[x])
            print(time.ctime(os.path.getctime(lists[x])))
    return lists

    # return list
    
def openImageList(imageList):
    images = []
    for i in imageList:
        images.append(Image.open(i))
    return images



#a=getPathDirectory(folderPathway)
#setOriginalJsonImageData()
#getNewJsonImageData()
#compareImageFile()
#a = sortImages(folderPathway)
#print(a)
# json_file = open("/Users/hari/Desktop/image grouping/Code/Image-grouping/development/app/imagesDir.txt","w")
# json.dump(folderPathway,json_file)
# json_file.close()
# print("json file created")
# #print(files)


# if movie == folderPathway:
#     print("its the same")
# else:
#     print("I fucked up")