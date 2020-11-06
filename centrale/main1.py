import tkinter as tk
import backend

#default usage for all pages
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

#First page of the program
class Homepage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        lframe = tk.LabelFrame(self, padx=5, pady=5)
        rframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row= 0, column = 0, padx=5, pady=5)
        rframe.grid(row= 0, column = 1, padx=5, pady=5, rowspan = 10)
        datastore = self.master.getdata().getjson()

        # add the modules that are used in the homepage
        welcome = tk.Label(rframe, wraplength = 150,height=36,width=80, text = "balkbalssjhdgfsajd gfasjdfg sajdhfgasdkjhf gasdjhf gaskdlfjg askldfgaskldjf hasjkdfh")
        rooms = tk.Label(lframe, text = "Kamers")
        add = tk.Button(lframe, text = "  +  ", command = lambda: self.master.showroom('addroom'),width=7)           #word pop-up ipv framelayer
        remove = tk.Button(lframe, text = "  -  ", command = lambda: self.master.showroom('removeroom'),width=7)     #word pop-up ipv framelayer
        listbox = tk.Listbox(lframe,height=30)
        scrollbar = tk.Scrollbar(lframe)
        
        #################test for listbox##########################
        for values in datastore["Kamers"]:                           
            listbox.insert(tk.END, values["naam"])
        ########################################################### 

        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview) 

        welcome.pack(expand="true")
        #building the grid`s for all the modules
        rooms.grid(row = 0, column = 0)
        listbox.grid(row = 1, column = 0, padx = 5, pady =5)
        scrollbar.grid(row = 1, column = 1,sticky="NS") # sticky NS so he can streatch the whole grid. otherwise it would be  a small scrollbar :)
        add.grid(row = 2, column = 0, padx = 0, pady = 5,sticky="W")
        remove.grid(row = 2, column = 0, padx = 0, pady = 5,sticky="E")


#placeholder for second page
class AddRoom(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        # add frame around all the coponents
        frame = tk.LabelFrame(self, padx=5, pady=5)
        frame.grid(row= 0, column = 0, padx=5, pady=5,)
        #all the modules for the layout
        label = tk.Label(frame, text="kamer toevoegen")
        labelname = tk.Label(frame, text="Naam:")
        add = tk.Button(frame,text="Toevoegen",width=25,command= None)
        back = tk.Button(frame,text="Annuleren",width=25,command=self.master.showroom("homepage"))
        inputbox = tk.Entry(frame)
        #added a font and biger size for the label on the top
        label.config(font=("Courier", 30))
        #adding all the modules to the grid
        label.grid(row=0,columnspan = 10)   #span == future updates
        inputbox.grid(row=1, column=1)
        labelname.grid(row=1,column=0)
        add.grid(row=2,column=0)
        back.grid(row=2,column=1)
        #center the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.rooms = dict()
        self.data = backend.Data("config.json","Kamers")
        self.datastore = self.data.getjson()

        self.rooms['homepage'] = Homepage(self) #call homepage
        self.rooms['addroom'] = AddRoom(self)    #Add a room page
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.rooms['homepage'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.rooms['addroom'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #als je hier een button maakt kan ik wel switchen tussen de pages.

        self.rooms['homepage'].show()       #show homepage first

    def showroom(self, room):
        self.rooms[room].show()
    def getdata(self):
        return self.data

# init for the tkinter screen
if __name__ == "__main__":
    root = tk.Tk()
    tk.Tk.wm_title(root, "Trollluik Interface")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.resizable(0, 0)
    root.geometry('800x600')
    root.iconbitmap('logo.ico')
    root.mainloop()