import tkinter as tk

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

       # rightside text label
       welcome = tk.Label(rframe, wraplength = 150,height=36,width=80, text = "balkbalssjhdgfsajd gfasjdfg sajdhfgasdkjhf gasdjhf gaskdlfjg askldfgaskldjf hasjkdfh")
       #list for the rooms
       rooms = tk.Label(lframe, text = "Kamers")
       add = tk.Button(lframe, text = "  +  ", command = lambda: self.master.showroom('addroom'),width=7)           #word pop-up ipv framelayer
       remove = tk.Button(lframe, text = "  -  ", command = lambda: self.master.showroom('removeroom'),width=7)     #word pop-up ipv framelayer


       listbox = tk.Listbox(lframe,height=30)
       for values in range(100):                           #placeholder "list"
           listbox.insert(tk.END, values) 
       scrollbar = tk.Scrollbar(lframe,)

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
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.rooms = dict()
        self.rooms['homepage'] = Homepage(self) #call homepage
        self.rooms['addroom'] = AddRoom(self)    #Add a room page
        print(self.rooms)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.rooms['homepage'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        self.rooms['addroom'].place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #als je hier een button maakt kan ik wel switchen tussen de pages.

        self.rooms['homepage'].show()       #show homepage first

    def showroom(self, room):
        self.rooms[room].show()


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