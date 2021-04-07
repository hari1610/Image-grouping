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

model = torch.load(PATH)
model.eval()
print(model)
print(imgDir)
files = []
#imgs = []
feature = 'dog'

pathrere = "/Users/hari/Desktop/image grouping/images"
#valid_images = [".jpg",".gif",".png",".jpeg"]
def load_images(path,valid_images = [".jpg",".gif",".png",".jpeg"]):
    imgs = []
    for f in os.listdir(path):
        files.append(os.path.join(path,f))
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs.append(Image.open(os.path.join(path,f)))
    return imgs
# print(len(imgs))
# for i in range(len(imgs)):
#     imgplot = plt.imshow(imgs[i])
#     plt.show()


def predict(imgs,feat,threshold=0.7):
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
                print(pather)
                #plt.imshow(pic)
                #plt.show()
                #return pred_class,pred_score
                break

        print("next image")
        if(i == (len(imgs)-1)):
            return pather

#get = predict(imgs,feature)
#print(get)
#print(pather)

#a = load_images(pathrere)
#print(len(a))