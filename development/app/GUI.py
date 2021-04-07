import tkinter
import tkinter.filedialog
import os


class ImageGroupingApp(tkinter.Tk):
    #initalise variables in the class
    def __init__(self, *args, **kwargs):
        #initalise tkinter
        tkinter.Tk.__init__(self,*args,**kwargs)
        #creating a frame to contain everything in the app
        container = tkinter.Frame(self)
        #declaring the position of the frame
        container.pack(fill="both",expand = True)
        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #specifing a dictionary that contains all the frames
        self.frames = {}
        self.visible =tkinter.StringVar()

        for F in (SplashScreenFrame, MainMenuFrame,SearchFolderFrame,ResultFrame):
            #setting frame to the first frame the user sees
            frame = F(container,self)

            self.frames[F] = frame
            #sticky is used for alinment
            frame.grid(row=0, column=0, sticky="nsew")
            
        
        
        self.show_frame(SplashScreenFrame)
        
    #creating a method to show frames
    def show_frame(self,cont):
        frame = self.frames[cont]
        self.visible.set(frame)
        frame.tkraise()


class SplashScreenFrame(tkinter.Frame):

    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        label = tkinter.Label(self, text= "Welcome to the Image Grouping Application")
        label.pack()

        startBtn = tkinter.Button(self, text="Start App",
                                 command=lambda: controller.show_frame(MainMenuFrame))
        startBtn.pack()


class MainMenuFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        #creating a text that says Main Menu
        mainMenuLabel = tkinter.Label(self, text= "Main Menu")
        mainMenuLabel.pack()
        #creating a recently added button
        recentlyAddedBtn = tkinter.Button(self, text="Recently Added Images")
        recentlyAddedBtn.pack()
        #creating a search button for searching in folders
        searchFolderBtn = tkinter.Button(self,text="Search Folder",
                                        command=lambda: controller.show_frame(SearchFolderFrame))
        searchFolderBtn.pack()

class RecentlyAddedFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
    

class SearchFolderFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        self.filename = tkinter.StringVar()
        self.features = []

        def select_folder():
            filePath = tkinter.filedialog.askdirectory()
            self.filename.set(filePath)
            #print(filePath)

        def get_filename():
            return self.filename

        def searchBtn():
            self.path = self.filename
            controller.show_frame(ResultFrame)

        def checkboxSelection():
            #print("hello")
            if(personVar.get() == 1) & (carVar.get() == 0) & (dogVar.get() == 0) & (catVar.get() == 0):
                print("person")
            elif(personVar.get() == 0) & (carVar.get() == 1) & (dogVar.get() == 0) & (catVar.get() == 0):
                print("car")
            elif(personVar.get() == 0) & (carVar.get() == 0) & (dogVar.get() == 1) & (catVar.get() == 0):
                print("dog")
            elif(personVar.get() == 0) & (carVar.get() == 0) & (dogVar.get() == 0) & (catVar.get() == 1):
                print("cat")

        selectFolderLabel = tkinter.Label(self, text = "Select Folder:")
        selectFolderLabel.grid(row=0,column=0)
        selectFolderLabel.columnconfigure(1,weight=1)
        selectFolderLabel.rowconfigure(1,weight=1)

        thresholdLabel = tkinter.Label(self, text = "Threshold(%):")
        thresholdLabel.grid(row=1,column=0)
        thresholdLabel.columnconfigure(1,weight=1)
        thresholdLabel.rowconfigure(1,weight=1)

        featuresLabel = tkinter.Label(self, text = "Features:")
        featuresLabel.grid(row=2,column=0)
        featuresLabel.columnconfigure(1,weight=1)
        featuresLabel.rowconfigure(1,weight=1)

        searchBtn = tkinter.Button(self,text="Search",
                                   command=lambda: controller.show_frame(ResultFrame))
        searchBtn.grid(row=3,column=1)
        searchBtn.columnconfigure(1,weight=1)
        searchBtn.rowconfigure(1,weight=1)

        selectFolderBtn = tkinter.Button(self,text="...",command = select_folder)
        selectFolderBtn.grid(row=0,column=2)
        selectFolderBtn.columnconfigure(1,weight=1)
        selectFolderBtn.rowconfigure(1,weight=1)

        folderPathLabel = tkinter.Label(self, textvariable = self.filename)
        folderPathLabel.grid(row=0,column=1)
        folderPathLabel.columnconfigure(1,weight=1)
        folderPathLabel.rowconfigure(1,weight=1)

        personVar = tkinter.IntVar()
        carVar = tkinter.IntVar()
        dogVar = tkinter.IntVar()
        catVar = tkinter.IntVar()
        personCb = tkinter.Checkbutton(self, text='Person',variable=personVar, onvalue=1, offvalue=0, command=checkboxSelection)
        carCb = tkinter.Checkbutton(self, text='Car',variable=carVar, onvalue=1, offvalue=0, command=checkboxSelection)
        dogCb = tkinter.Checkbutton(self, text='Dog',variable=dogVar, onvalue=1, offvalue=0, command=checkboxSelection)
        catCb = tkinter.Checkbutton(self, text='Cat',variable=catVar, onvalue=1, offvalue=0, command=checkboxSelection)
        personCb.grid(row=2,column=1)
        carCb.grid(row=2,column=2)
        dogCb.grid(row=2,column=3)
        catCb.grid(row=2,column=4)

        thresholdVar = tkinter.IntVar()
        thresholdVar.set(0.7) # default value

        thresholdSelection = tkinter.OptionMenu(self, thresholdVar, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
        thresholdSelection.grid(row = 1, column = 1)

        testinglabel = tkinter.Label(self, textvariable = thresholdVar)
        testinglabel.grid(row = 4, column = 4)


class ResultFrame(tkinter.Frame):
    
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        #self.path = tkinter.StringVar()
        p1 = controller.frames[SearchFolderFrame]
        self.path = p1.filename
        if(controller.visible == 'SplashScreenFrame'):
            print(self.path)
        else:
            print("different frame")
            print(controller.visible)

        pathLabel = tkinter.Label(self, textvariable = self.path)
        pathLabel.grid(row=0,column=1)
        pathLabel.columnconfigure(1,weight=1)
        pathLabel.rowconfigure(1,weight=1)

        
        
        # button1 = tkinter.Button(self, text="click", command=sayhello())
        # button1.grid(row=0,column=2)
        # button1.columnconfigure(1,weight=1)
        # button1.rowconfigure(1,weight=1)

        



        # file_dir = controller.frame["SearchFolderFrame"].get_filename()
        # print(file_dir)

       # for images in os.listdir(file_dir):
    # def sayhello(self):
    #     return print("hello")
    
    
class Model:
    import torch
    import torchvision
    from torchvision import models
    import torchvision.transforms as transforms
    import numpy as np
    import torch.nn.functional as F
    import matplotlib.pyplot as plt
    import urllib
    from PIL import Image

#    # def __init__(self,transforms):
        
#     imgDir = ""
#     def transformImg(transforms):
#         transform = transforms.Compose([transforms.ToTensor()])

#     def set_ImgPath(self,imgPath):
#         imgDir = imgPath
    
#     PATH = "/Users/hari/Desktop/image grouping/FRCNN.pth"
    
#     model = torch.load(PATH)
#     model.eval()
#     print(model)
#     print(imgDir)
#     imgs = []
# path = "/Users/hari/Desktop/image grouping/images"
# valid_images = [".jpg",".gif",".png",".jpeg"]
# for f in os.listdir(path):
#     ext = os.path.splitext(f)[1]
#     if ext.lower() not in valid_images:
#         continue
    # imgs.append(Image.open(os.path.join(path,f)))
    


app = ImageGroupingApp()
app.title("Image Grouping")
app.geometry('700x500')
app.mainloop()