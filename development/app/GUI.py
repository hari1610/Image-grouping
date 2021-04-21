import tkinter
import tkinter.filedialog
import os
import model
from PIL import Image,ImageTk
import subprocess
from tkinter import ttk
import fileMonitor

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

        for F in (SplashScreenFrame, MainMenuFrame,SearchFolderFrame,ResultFrame,RecentlyAddedFrame,Car,Dog,Cat,Person):
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
        
        
        
        self.searchBtn = tkinter.Button(self,text= "Please Select a Default Folder to Search", command = self.select_folder)
        self.searchBtn.pack()

        self.startBtn = tkinter.Button(self, text="Start App",
                                 command=lambda: controller.show_frame(MainMenuFrame))
        self.startBtn.pack()
    
    def select_folder(self):
            filepath = tkinter.filedialog.askdirectory()
            a = str(filepath)
            print(a)
            f = open("pathway.txt","w")
            f.write(str(a))
            f.close()
            print("created file")


class MainMenuFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        #creating a text that says Main Menu
        mainMenuLabel = tkinter.Label(self, text= "Main Menu")
        mainMenuLabel.pack()
        #creating a recently added button
        recentlyAddedBtn = tkinter.Button(self, text="Recently Added Images",
                                             command = lambda: controller.show_frame(RecentlyAddedFrame))
        recentlyAddedBtn.pack()
        #creating a search button for searching in folders
        searchFolderBtn = tkinter.Button(self,text="Search Folder",
                                        command=lambda: controller.show_frame(SearchFolderFrame))
        searchFolderBtn.pack()

class RecentlyAddedFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
    
        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(MainMenuFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")

        dogsBtn = tkinter.Button(self, text="Dogs",command=lambda:controller.show_frame(Dog))
        dogsBtn.pack()

        catsBtn = tkinter.Button(self, text="Cats",command=lambda:controller.show_frame(Cat))
        catsBtn.pack()

        carsBtn = tkinter.Button(self, text="Cars",command=lambda:controller.show_frame(Car))
        carsBtn.pack()

        personsBtn = tkinter.Button(self, text="People",command=lambda:controller.show_frame(Dog))
        personsBtn.pack()

class SearchFolderFrame(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)

        # backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(MainMenuFrame))
        # backBtn.pack(side = tkinter.TOP,anchor="nw")

        # homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        # homeBtn.pack(side =tkinter.TOP,anchor="ne")
        
        self.filename = tkinter.StringVar()
        self.features = ''
        self.finalImages = []

        def select_folder():
            filePath = tkinter.filedialog.askdirectory()
            self.filename.set(filePath)
            #print(filePath)

        def get_filename():
            return self.filename

        self.thresholdVar = tkinter.StringVar()
        self.thresholdVar.set(0.7) # default value

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
                                   command=lambda:self.searchBtn(controller))
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

        self.personVar = tkinter.IntVar()
        self.carVar = tkinter.IntVar()
        self.dogVar = tkinter.IntVar()
        self.catVar = tkinter.IntVar()
        self.personCb = tkinter.Checkbutton(self, text='Person',variable=self.personVar, onvalue=1, offvalue=0, command=self.checkboxSelection)
        self.carCb = tkinter.Checkbutton(self, text='Car',variable=self.carVar, onvalue=1, offvalue=0, command=self.checkboxSelection)
        self.dogCb = tkinter.Checkbutton(self, text='Dog',variable=self.dogVar, onvalue=1, offvalue=0, command=self.checkboxSelection)
        self.catCb = tkinter.Checkbutton(self, text='Cat',variable=self.catVar, onvalue=1, offvalue=0, command=self.checkboxSelection)
        self.personCb.grid(row=2,column=1)
        self.carCb.grid(row=2,column=2)
        self.dogCb.grid(row=2,column=3)
        self.catCb.grid(row=2,column=4)

        

        thresholdSelection = tkinter.OptionMenu(self, self.thresholdVar, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1)
        thresholdSelection.grid(row = 1, column = 1)

        testinglabel = tkinter.Label(self, textvariable = self.thresholdVar)
        testinglabel.grid(row = 4, column = 4)
    
    def searchBtn(self,controller):
        file = self.filename.get()
        thres =float(self.thresholdVar.get())
        #print(thresholdVar.get())
        print(thres)
        photos = model.load_images(file)
        answersPath = model.predict(photos,self.features,thres)
        print('success')
        print(answersPath)
        self.finalImages = answersPath
        controller.show_frame(ResultFrame)

    def checkboxSelection(self):
        #print("hello")
        if(self.personVar.get() == 1) & (self.carVar.get() == 0) & (self.dogVar.get() == 0) & (self.catVar.get() == 0):
            self.features = 'person'
            print(self.features)
        elif(self.personVar.get() == 0) & (self.carVar.get() == 1) & (self.dogVar.get() == 0) & (self.catVar.get() == 0):
            self.features = 'car'
            print(self.features)
        elif(self.personVar.get() == 0) & (self.carVar.get() == 0) & (self.dogVar.get() == 1) & (self.catVar.get() == 0):
            self.features = 'dog'
            print(self.features)
        elif(self.personVar.get() == 0) & (self.carVar.get() == 0) & (self.dogVar.get() == 0) & (self.catVar.get() == 1):
            self.features = 'cat'
            print(self.features)

class Car(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(RecentlyAddedFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")


        

        #self.images = fileMonitor.getImages(fileMonitor.openImageDirJson())
        self.sortImage = fileMonitor.sortImages(fileMonitor.openImageDirJson())
        model.files = self.sortImage
        self.openSortImages = fileMonitor.openImageList(self.sortImage)
        self.carPic = model.predict(self.openSortImages,'car')




        my_canvas = tkinter.Canvas(self)
        my_canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand = 1)


        my_scrollbar = ttk.Scrollbar(self,orient = tkinter.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)


        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))


        secondFrame = tkinter.Frame(my_canvas)

        my_canvas.create_window((0,0),window = secondFrame, anchor="nw")


        self.photos = []
        def open_image(imagePath):
            if os.name == 'posix':
                #rwre = ('"%s"' % imagePath)
                #subprocess.call(['/usr/bin/open' ,rwre])
                subprocess.run(['open', imagePath])
            elif os.name == 'win32' :
                subprocess.run(['explorer', imagePath])
        #def displayImg(img):
        for directories in self.carPic:
            self.image = Image.open(directories)
            self.image = self.image.resize((100,100))
            self.photo = ImageTk.PhotoImage(self.image)
            self.photos.append(self.photo)
            #newPhoto_label = tkinter.Label(self,image=photo)
            #newPhoto_label.pack()
            newBtn = tkinter.Button(secondFrame,image = self.photo, command = lambda: open_image(directories))
            newBtn.pack()

        # for directories in self.carPic:
        #     print(directories)
        #     displayImg(directories) 


class Dog(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        
        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(RecentlyAddedFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")

        my_canvas = tkinter.Canvas(self)
        my_canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand = 1)


        my_scrollbar = ttk.Scrollbar(self,orient = tkinter.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)


        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))


        secondFrame = tkinter.Frame(my_canvas)

        my_canvas.create_window((0,0),window = secondFrame, anchor="nw")

class Cat(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)

        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(RecentlyAddedFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")

        my_canvas = tkinter.Canvas(self)
        my_canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand = 1)


        my_scrollbar = ttk.Scrollbar(self,orient = tkinter.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)


        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))


        secondFrame = tkinter.Frame(my_canvas)

        my_canvas.create_window((0,0),window = secondFrame, anchor="nw")

class Person(tkinter.Frame):
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)

        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(RecentlyAddedFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")

        my_canvas = tkinter.Canvas(self)
        my_canvas.pack(side=tkinter.LEFT,fill=tkinter.BOTH, expand = 1)


        my_scrollbar = ttk.Scrollbar(self,orient = tkinter.VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=tkinter.RIGHT,fill=tkinter.Y)


        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))


        secondFrame = tkinter.Frame(my_canvas)

        my_canvas.create_window((0,0),window = secondFrame, anchor="nw")

class ResultFrame(tkinter.Frame):
    
    def __init__(self,parent, controller):
        tkinter.Frame.__init__(self,parent)
        #self.path = tkinter.StringVar()
        print(os.name)
        
        # if(controller.visible == 'SplashScreenFrame'):
        #     print(self.path)
        # else:
        #     print("different frame")
        #     print(controller.visible)
        backBtn = tkinter.Button(self,text="Back",command=lambda:controller.show_frame(SearchFolderFrame))
        backBtn.pack(side = tkinter.TOP,anchor="nw")

        homeBtn = tkinter.Button(self,text="Home",command=lambda:controller.show_frame(MainMenuFrame))
        homeBtn.pack(side =tkinter.TOP,anchor="ne")

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
    
    


app = ImageGroupingApp()
app.title("Image Grouping")
app.geometry('700x500')
app.mainloop()