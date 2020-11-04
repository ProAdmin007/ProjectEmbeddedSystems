import tkinter as tk


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Trollluik Interface")
        self.resizable(0, 0)
        self.geometry('800x600')
        self.iconbitmap('logo.ico')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomeScreen, RoomPage, ScreenPage, AddRoom, AddScreen):         
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeScreen")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    #def welcomeMessage(self):

class HomeScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lframe = tk.LabelFrame(self, padx=5, pady=5)
        rframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row= 0, column = 0, padx=5, pady=5)
        rframe.grid(row= 0, column = 1, padx=5, pady=5, rowspan = 10)
        # de tekst die op de rechter kant komt te staan.
        welcome = tk.Label(rframe, wraplength = 150,height=36,width=80, text = "balkbalssjhdgfsajd gfasjdfg sajdhfgasdkjhf gasdjhf gaskdlfjg askldfgaskldjf hasjkdfh")
        rooms = tk.Label(lframe, text = "Kamers")
        add = tk.Button(lframe, text = "  +  ", command = lambda: controller.show_frame("AddRoom"),width=7)           #word pop-up ipv framelayer ?
        remove = tk.Button(lframe, text = "  -  ", command = lambda: controller.show_frame("RemoveRoom"),width=7)     #word pop-up ipv framelayer
        listbox = tk.Listbox(lframe,height=30)
        for values in range(100):                           #placeholder "list"
            listbox.insert(tk.END, values) 
        scrollbar = tk.Scrollbar(lframe,)

          
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview) 

        welcome.pack(expand="true")
        rooms.grid(row = 0, column = 0)
        listbox.grid(row = 1, column = 0, padx = 5, pady =5)
        scrollbar.grid(row = 1, column = 1,sticky="NS") # sticky NS so he can streatch the whole grid. otherwise it would be  a small scrollbar :)
        add.grid(row = 2, column = 0, padx = 0, pady = 5,sticky="W")
        remove.grid(row = 2, column = 0, padx = 0, pady = 5,sticky="E")


#    def removeRoomWindow(self):
#        self.newWindow2 = tk.Toplevel(self.master)
#        self.main = RemoveRoom(self.removeRoomWindow)


class RoomPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

    def addScreenWindow(self):
        self.newWindow3 = tk.Toplevel(self.master)
        self.app = RemoveScreen(self.addScreenWindow)

    def removeScreenWindow(self):
        self.newWindow4 = tk.Toplevel(self.master)
        self.app = RemoveScreen(self.removeScreenWindow)

class ScreenPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class AddRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


        #RoomMessage = tk.Label(self, text = "Kamer toevoegen")
        #Name = tk.Label(text = "Naam:")
        #NameEntry = tk.Entry()
        #AddButton = tk.Button()
        #CancelButton = tk.Button()
    
        #RoomMessage.pack()
        #Name.grid()
        #NameEntry.grid()
        #AddButton.grid()
        #CancelButton.grid()


class RemoveRoom(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        RoomMessage = tk.Label(self, text = "Kamer toevoegen")
        RoomMessage.pack()


class AddScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

class RemoveScreen(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

class room:

    def __init__(self, name):
        self.name = name

class screen:
    
    def __init__(self, name, room, device):
        self.name = name
        self.room = room
        self.device = device


if __name__ == "__main__":
    root = Main()
    root.mainloop()