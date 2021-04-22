"""Model
This module is required to create a faster R-CNN model and pass through every image from the user directory
through the model and predict the feature each image contains.

This module requires pytorch, pillow and torchvision to be installed in the users python environment.

functions
---------
getDog() - returns a list of paths to an image containing dogs
getCar() - returns a list of paths to an image containing cars
getPerson() - returns a list of paths to an image containing person
getCat() - returns a list of paths to an image containing cat
load_images() - returns a list of all the images in an directory
predict() - returns a set of image paths that have the same features
predictForRecentFrame() - appends the dog,car,person and cat lists with their appropriate image paths
"""
import torch
import torchvision
from torchvision import models
import torchvision.transforms as transforms
import numpy as np
import torch.nn.functional as F
import matplotlib.pyplot as plt
import urllib
from PIL import Image    
import os

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]
threshold = 0.7
imgDir = ""
def transformImgToTensor(image):
    transform = transforms.Compose([transforms.ToTensor()])
    return transform(image)
def set_ImgPath(self,imgPath):
    imgDir = imgPath
    
PATH = "/Users/hari/Desktop/image grouping/FRCNN.pth"

model = torch.load(PATH) #load in the faster R-CNN model
model.eval()#put the model in evaluation mode
#print(model)
#print(imgDir)
files = [] #create files list
#imgs = []
car = [] #create car list
person = [] #create a person list
cat = [] #create  a cat list
dog = [] #create a dog list


pathrere = "/Users/hari/Downloads"
#valid_images = [".jpg",".gif",".png",".jpeg"]
def getDog():
    """gets and returns the dog list"""
    return dog

def getCar():
    """gets and returns the car list"""
    return car

def getPerson():
    """gets and returns the person list"""
    return person

def getCat():
    """gets and returns the cat list"""
    return cat

def load_images(path,valid_images = [".jpg",".gif",".png",".jpeg"]):
    """
    searches through all the files in a directory for files that have the valid images extensions
    Parameters
    ----------
    path : str
        the location to where are all the images
    valid_images : list, optional
        a list of image file formats the method accepts

    Returns
    -------
    imgs : list
        a list of paths for the supported images only
    """
    imgs = []
    files.clear() # making sure the files list is empty
    for f in os.listdir(path):
        #files.append(os.path.join(path,f))
        ext = os.path.splitext(f)[1] # takes only the file format
        
        if ext.lower() not in valid_images:
            print(ext)
            #continue
        if ext.lower() in valid_images: # only if the file format is in the valid images list then add that path
            imgs.append(Image.open(os.path.join(path,f)))
            files.append(os.path.join(path,f))
    print(files)
    return imgs
# print(len(imgs))
# for i in range(len(imgs)):
#     imgplot = plt.imshow(imgs[i])
#     plt.show()


def predict(imgs,feat,threshold=0.7):
    """
    puts each
    """

    print(len(imgs))
    pather = []
    for i in range(len(imgs)):
    
        
        transform = transforms.Compose([transforms.ToTensor()])
        imgs[i] = transform(imgs[i])
        pred = model([imgs[i]])
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())] # Get the Prediction Score
        pred_score = list(pred[0]['scores'].detach().numpy())#?
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1] # Get list of index with score greater than threshold.
        pred_class = pred_class[:pred_t+1]
        pred_score = pred_score[:pred_t+1]
        #print(pred_class)
        #print(pred_score)
        for t in range(len(pred_class)):
            #print(pred_class[t], pred_score[t])
            #print(pred_class)
            if(pred_class[t]==feat) & (pred_score[t] >= threshold):
                print(pred_class[t], pred_score[t])
                print("feature found")
                #pic = Image.open(files[i])
                pather.append(files[i])
                #print(pather)
                #plt.imshow(pic)
                #plt.show()
                #return pred_class,pred_score
                break

        print("next image")
        if(i == (len(imgs)-1)):
            return pather

def predictForRecentFrame(imgs, threshold = 0.7):

    print(len(imgs))
    for i in range(len(imgs)):
    
        
        transform = transforms.Compose([transforms.ToTensor()])
        imgs[i] = transform(imgs[i])
        pred = model([imgs[i]])
        pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())] # Get the Prediction Score
        pred_score = list(pred[0]['scores'].detach().numpy())#?
        pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1] # Get list of index with score greater than threshold.
        pred_class = pred_class[:pred_t+1]
        pred_score = pred_score[:pred_t+1]
        #print(pred_class)
        #print(pred_score)
        for t in range(len(pred_class)):
            #print(pred_class[t], pred_score[t])
            #print(pred_class)
            if(pred_class[t]=='car') & (pred_score[t] >= threshold):
                print(pred_class[t], pred_score[t])
                print("feature found")
                #pic = Image.open(files[i])
                car.append(files[i])
                #print(pather)
                #plt.imshow(pic)
                #plt.show()
                #return pred_class,pred_score
            
            if(pred_class[t]=='person') & (pred_score[t] >= threshold):
                person.append(files[i])
            
            if(pred_class[t]=='cat') & (pred_score[t] >= threshold):
                cat.append(files[i])
            
            if(pred_class[t]=='dog') & (pred_score[t] >= threshold):
                dog.append(files[i])

        print("next image")
        


#get = predict(imgs,feature)
#print(get)
#print(pather)

#a = load_images(pathrere)
# get = predict(a,feature)
#print(len(a))