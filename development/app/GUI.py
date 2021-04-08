import tkinter
import tkinter.filedialog
import os
import model
from PIL import Image,ImageTk
import subprocess
from tkinter import ttk

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
        filename = tkinter.StringVar()
        def select_folder():
            filepath = tkinter.filedialog.askdirectory()
            filename.set(filepath)
        
        searchBtn = tkinter.Button(self,text= "Please Select a Default Folder to Search", command = select_folder)
        searchBtn.pack()

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
        self.features = ''
        self.finalImages = []

        def select_folder():
            filePath = tkinter.filedialog.askdirectory()
            self.filename.set(filePath)
            #print(filePath)

        def get_filename():
            return self.filename

        def searchBtn():
            file = self.filename.get()
            thres =float(thresholdVar.get())
            #print(thresholdVar.get())
            print(thres)
            photos = model.load_images(file)
            answersPath = model.predict(photos,self.features,thres)
            print('success')
            print(answersPath)
            self.finalImages = answersPath
            controller.show_frame(ResultFrame)

        def checkboxSelection():
            #print("hello")
            if(personVar.get() == 1) & (carVar.get() == 0) & (dogVar.get() == 0) & (catVar.get() == 0):
                self.features = 'person'
                print(self.features)
            elif(personVar.get() == 0) & (carVar.get() == 1) & (dogVar.get() == 0) & (catVar.get() == 0):
                self.features = 'car'
                print(self.features)
            elif(personVar.get() == 0) & (carVar.get() == 0) & (dogVar.get() == 1) & (catVar.get() == 0):
                self.features = 'dog'
                print(self.features)
            elif(personVar.get() == 0) & (carVar.get() == 0) & (dogVar.get() == 0) & (catVar.get() == 1):
                self.features = 'cat'
                print(self.features)

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
                                   command=searchBtn)
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

        thresholdVar = tkinter.StringVar()
        thresholdVar.set(0.7) # default value

        thresholdSelection = tkinter.OptionMenu(self, thresholdVar, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
        thresholdSelection.grid(row = 1, column = 1)

        testinglabel = tkinter.Label(self, textvariable = thresholdVar)
        testinglabel.grid(row = 4, column = 4)


class ResultFrame(tkinter.Frame):
    
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        #self.path = tkinter.StringVar()
        print(os.name)
        
        if(controller.visible == 'SplashScreenFrame'):
            print(self.path)
        else:
            print("different frame")
            print(controller.visible)
        photos = []
        def open_image(imagePath):
            if os.name == 'posix':
                #rwre = ('"%s"' % imagePath)
                #subprocess.call(['/usr/bin/open' ,rwre])
                subprocess.run(['open', imagePath])
            elif os.name == 'win32' :
                subprocess.run(['explorer', imagePath])
        def displayImg(img):
            image = Image.open(img)
            image = image.resize((100,100))
            photo = ImageTk.PhotoImage(image)
            photos.append(photo)
            #newPhoto_label = tkinter.Label(self,image=photo)
            #newPhoto_label.pack()
            newBtn = tkinter.Button(secondFrame,image = photo, command = lambda: open_image(img))
            newBtn.pack()

        def refresh():
            p1 = controller.frames[SearchFolderFrame]
            self.path = p1.finalImages
            #images = Image.open(self.path[0])
            #photo = ImageTk.PhotoImage(images)
            #pathLabel.config(text=("\n".join(self.path)))
            #pathLabel.config(image = photo)
            for directories in self.path:
                 displayImg(directories)
                 print('success')
       # ghghf = Image.open('/Users/hari/Desktop/image grouping/images/newimage.jpeg')
        #jyttj = ImageTk.PhotoImage(ghghf)
        #pathLabel = tkinter.Label(self, image = jyttj )
        #pathLabel.grid(row=0,column=1)
        #pathLabel.pack()
        #pathLabel.columnconfigure(1,weight=1)
        #pathLabel.rowconfigure(1,weight=1)


        my_canvas = tkinter.Canvas(self)
        my_canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand = 1)


        my_scrollbar = ttk.Scrollbar(self,orient = tkinter.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)


        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))


        secondFrame = tkinter.Frame(my_canvas)

        my_canvas.create_window((0,0),window = secondFrame, anchor="nw")


        refreshbtn = tkinter.Button(secondFrame, text = "refresh", command = refresh)
        #refreshbtn.grid(row = 2, column = 2)
        refreshbtn.pack()

        
        
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