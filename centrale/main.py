import tkinter as tk
from tkinter import messagebox
import backend
import serial.tools.list_ports


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


class Homepage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        lframe = tk.LabelFrame(self, padx=5, pady=5)
        rframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row=0, column=0, padx=5, pady=5)
        rframe.grid(row=0, column=1, padx=5, pady=5, rowspan=10)
        self.datastore = self.master.getdata()
        self.toggle = False

        # add the modules that are used in the homepage
        welcome = tk.Label(rframe, wraplength=150, height=36, width=80, text="Welkom!")
        rooms = tk.Label(lframe, text="Kamers")
        add = tk.Button(lframe, text="  +  ", command=lambda: self.master.showroom('addroom'), width=7)
        remove = tk.Button(lframe, text="  -  ", command=lambda: self.removeRoom(), width=7)
        self.listbox = tk.Listbox(lframe, height=30)
        scrollbar = tk.Scrollbar(lframe)
        self.updatelist()
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.event_generate('<<ListBoxSelect>>')
        self.listbox.bind('<<ListboxSelect>>', self.selector)
        scrollbar.config(command=self.listbox.yview)

        welcome.pack(expand="true")
        # building the grid`s for all the modules
        rooms.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0, padx=5, pady=5)
        scrollbar.grid(row=1, column=1, sticky="NS")
        add.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        remove.grid(row=2, column=0, padx=0, pady=5, sticky="E")

    def updatelist(self):
        self.listbox.delete(0, 'end')
        for values in self.datastore.getjson()["Kamers"]:
            self.listbox.insert(tk.END, values)

    def removeRoom(self):
        if not self.toggle:
            self.toggle = True
            self.listbox.config(foreground="red")
        else:
            self.toggle = False
            self.listbox.config(foreground="black")

    def selector(self, event):
        item = self.listbox.get(self.listbox.curselection())
        if self.toggle:
            message = messagebox.askquestion(title="Weet u het zeker?", message="Wilt u de kamer "+item+" Verwijderen?")
            if message == "yes":
                data = self.datastore.getjson()
                for i in data["Kamers"]:
                    if item == i:
                        data["Kamers"].pop(item)
                        self.datastore.writejson(data)
                        self.updatelist()
                        break
        else:
            self.master.setselectedroom(item)
            self.master.showroom("roommenu")


class AddRoom(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.data = self.master.getdata()

        # add frame around all the coponents
        frame = tk.LabelFrame(self, padx=5, pady=5)
        frame.grid(row=0, column=0, padx=5, pady=5,)
        # all the modules for the layout
        label = tk.Label(frame, text="kamer toevoegen")
        labelname = tk.Label(frame, text="Naam:")
        inputbox = tk.Entry(frame)
        add = tk.Button(frame, text="Toevoegen", width=25, command=lambda: self.addRoomJson(inputbox.get()))
        back = tk.Button(frame, text="Annuleren", width=25, command=lambda: self.master.showroom("homepage"))
        # added a font and biger size for the label on the top
        label.config(font=("Courier", 30))

        # adding all the modules to the grid
        label.grid(row=0, columnspan=10)
        inputbox.grid(row=1, column=1)
        labelname.grid(row=1, column=0)
        add.grid(row=2, column=0)
        back.grid(row=2, column=1)

        # center the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def addRoomJson(self, name):
        datajson = self.data.getjson()
        if name in datajson["Kamers"]:
            messagebox.showerror(title="Kamer toevoegen", message="Deze kamer bestaat al!")
        else:
            datajson["Kamers"][name] = {"Scherm": {}}
            self.data.writejson(datajson)
            self.master.showroom("homepage")


class RoomMenu(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        lframe = tk.LabelFrame(self, padx=5, pady=5)
        rframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row=0, column=0, padx=5, pady=5)
        rframe.grid(row=0, column=1, padx=5, pady=5, rowspan=10)
        self.datastore = self.master.getdata()
        self.toggle = False
        self.room = ""
        # add the modules that are used in the homepage
        welcome = tk.Label(rframe, wraplength=150, height=36, width=80, text="Selecteer een sensor aan de linker kant om data te zien")
        rooms = tk.Label(lframe, text="Schermen")
        add = tk.Button(lframe, text="  +  ", command=lambda: self.master.showroom('addsensor'), width=7)           # word pop-up ipv framelayer
        remove = tk.Button(lframe, text="  -  ", command=lambda: self.removeSensor(), width=7)     # word pop-up ipv framelayer
        self.listbox = tk.Listbox(lframe, height=30)
        scrollbar = tk.Scrollbar(lframe)

        self.updatelist()

        # added some listbox config and added the events for selections
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.event_generate('<<ListBoxSelect>>')
        self.listbox.bind('<<ListboxSelect>>', self.selector)
        scrollbar.config(command=self.listbox.yview)

        welcome.pack(expand="true")
        # building the grid`s for all the modules
        rooms.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0, padx=5, pady=5)
        scrollbar.grid(row=1, column=1, sticky="NS")  # sticky NS so he can streatch the whole grid. otherwise it would be  a small scrollbar :)
        add.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        remove.grid(row=2, column=0, padx=0, pady=5, sticky="E")

    def updatelist(self):
        self.listbox.delete(0, 'end')
        if not self.room == "":
            for v in self.datastore.getjson()["Kamers"][self.room]["Scherm"]:
                self.listbox.insert(tk.END, v)

    def removeSensor(self):
        if not self.toggle:
            self.toggle = True
            self.listbox.config(foreground="red")
        else:
            self.toggle = False
            self.listbox.config(foreground="black")

    def selector(self, event):
        item = self.listbox.get(self.listbox.curselection())
        print(self.room)
        if self.toggle:
            message = messagebox.askquestion(title="Weet u het zeker?", message="Wilt u de sensor "+item+" Verwijderen?")
            if message == "yes":
                data = self.datastore.getjson()
                for i in data["Kamers"]:
                    if item == i:
                        data["Kamers"].pop(item)
                        self.datastore.writejson(data)
                        self.updatelist()
                        break
        else:
            self.sensor = item
    
    def updateroom(self):
        self.room = self.master.getselectedroom()


class Addsensor(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.data = self.master.getdata()
        self.listport = ["Niks gevonden"]

        # add frame around all the coponents
        frame = tk.LabelFrame(self, padx=5, pady=5)
        frame.grid(row=0, column=0, padx=5, pady=5,)

        # dropdown menu
        comport = tk.StringVar()
        comport.set(self.listport[0])
        dropdown = tk.OptionMenu(frame,comport,self.listport)
        # all the modules for the layout
        label = tk.Label(frame, text="Scherm toevoegen")
        labelname = tk.Label(frame, text="Naam:")
        labelcom = tk.Label(frame, text="Scherm:")
        inputbox = tk.Entry(frame)
        add = tk.Button(frame, text="Toevoegen", width=25, command=lambda: self.addSensorJson(inputbox.get(),comport.get()))
        back = tk.Button(frame, text="Annuleren", width=25, command=lambda: self.master.showroom("homepage"))
        # added a font and biger size for the label on the top
        label.config(font=("Courier", 30))

        # adding all the modules to the grid
        label.grid(row=0, columnspan=10)
        inputbox.grid(row=1, column=1)
        labelname.grid(row=1, column=0)
        labelcom.grid(row=2, column=0)
        dropdown.grid(row=2, column=1)
        add.grid(row=3, column=0)
        back.grid(row=3, column=1)

        # center the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def addSensorJson(self, name, comport):
        datajson = self.data.getjson()
        if name in datajson["Kamers"][self.master.room()]["scherm"]:
            messagebox.showerror(title="Scherm toevoegen", message="Deze is al in gebruik")
        else:
            datajson["Kamers"][self.master.room()]["Scherm"][name] = comport
            self.data.writejson(datajson)
            self.master.showroom("homepage")
    def updatecoms(self):
        self.listport = serial.tools.list_ports.comports()
        if self.listport == []:
            self.listport.append("niet gevonden")
            messagebox.showerror(title="Geen schermen gevonden", message="Er zijn geen schermen aangesloten")

        
        


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.rooms = dict()
        self.data = backend.Data("config.json", "Kamers")
        self.datastore = self.data.getjson()
        self.lastroom = ""

        self.rooms['homepage'] = Homepage(self)  # call homepage
        self.rooms['addroom'] = AddRoom(self)    # Add a room page
        self.rooms['roommenu'] = RoomMenu(self)  # Add the room page for sensors
        self.rooms['addsensor'] = Addsensor(self)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        for i in self.rooms:
            self.rooms[i].place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.rooms['homepage'].show()       # show homepage first

    def showroom(self, room):
        if room == "homepage":
            self.rooms[room].updatelist()
        if room == "roommenu":
            self.rooms[room].updateroom()
            self.rooms[room].updatelist()
        if room == "addsensor":
            self.rooms[room].updatecoms()
        self.rooms[room].show()

    def getdata(self):
        self.data = backend.Data("config.json", "Kamers")
        return self.data

    def setselectedroom(self, room):
        self.lastroom = room

    def getselectedroom(self):
        return self.lastroom

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
