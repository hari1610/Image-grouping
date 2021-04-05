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

        def select_folder():
            filePath = tkinter.filedialog.askdirectory()
            self.filename.set(filePath)
            #print(filePath)

        def get_filename():
            return self.filename

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


class ResultFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)

        p1 = SearchFolderFrame(parent, controller)
        self.path = p1.filename
       # self.path.set(p1.filename)
        print(self.path)

        pathLabel = tkinter.Label(self, text = self.path)
        pathLabel.grid(row=0,column=1)
        pathLabel.columnconfigure(1,weight=1)
        pathLabel.rowconfigure(1,weight=1)

        # def path_reload():
        #     upText = p1.filename.get()
        #     pathLabel.configure(text = upText)
        #     pathLabel.after(400,path_reload)
        
        # path_reload()
        
        

        # file_dir = controller.frame["SearchFolderFrame"].get_filename()
        # print(file_dir)

       # for images in os.listdir(file_dir):
    
    
class Model():
    import torch
    import torchvision
    from torchvision import models
    import torchvision.transforms as transforms
    import numpy as np
    import torch.nn.functional as F
    import matplotlib.pyplot as plt
    import urllib
    from PIL import Image

    PATH = "/Users/hari/Desktop/image grouping/FRCNN.pth"
    model = torch.load(PATH)
    model.eval()
    
    
    


app = ImageGroupingApp()
app.title("Image Grouping")
app.geometry('700x500')
app.mainloop()