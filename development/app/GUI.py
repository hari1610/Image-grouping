import tkinter

class imageGroupingApp(tkinter.Tk):
   
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tkinter.Frame(self)
        
        # initializing frames to an empty array
        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainMenu, RecentlyAdded):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(MainMenu)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


window =tkinter.Tk()
window.title("Object Detection and Sorting")
window.geometry('700x500')

mainMenuFrame = tkinter.Frame(window)
mainMenuFrame.pack()

def searchFolder():
    searchWindowFrame = tkinter.Frame(window)
    searchWindowFrame.pack()
    searchWindowFrame.tkraise()
    mainMenu = tkinter.Label(searchWindowFrame,text="Hello")
    
mainMenu = tkinter.Label(mainMenuFrame,text="Main Menu")
recent = tkinter.Button(mainMenuFrame, text = 'Recently Added',bg="black",fg='black')
search = tkinter.Button(mainMenuFrame, text = 'Search Folder',command = searchFolder)
mainMenu.grid(column = 5, row = 1)
recent.grid(column = 1, row = 5)
search.grid(column = 10, row = 5)
window.mainloop()