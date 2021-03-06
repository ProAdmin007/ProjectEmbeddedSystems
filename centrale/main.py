import tkinter as tk
from tkinter import messagebox
import backend
import grafieken
import serial.tools.list_ports


# Base class for all pages so they have the tk.frame and
# a simple show function to set the page to the front
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# Homepage class is the starter page of the program.
# it has a function to update the list with rooms
class Homepage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        lframe = tk.LabelFrame(self, padx=5, pady=5)
        rframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row=0, column=0, padx=5, pady=5)
        rframe.grid(row=0, column=1, padx=5, pady=5, rowspan=10)
        self.datastore = self.master.getdata()
        self.toggle = False

        # Rechter frame widgets
        welcome = tk.Label(rframe, height=36, width=80,
                           text="Welkom bij het startscherm van Trolluik")

        # linker frame widgets
        rooms = tk.Label(lframe, text="Kamers")
        add = tk.Button(lframe, text="+", width=7,
                        command=lambda: self.master.showroom('addroom'))
        remove = tk.Button(lframe, text="-", width=7,
                           command=lambda: self.RemRoom())
        self.listbox = tk.Listbox(lframe, height=30)
        scrollbar = tk.Scrollbar(lframe)

        # listbox update list with json value`s and event triggers
        self.updatelist()
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.event_generate('<<ListBoxSelect>>')
        self.listbox.bind('<<ListboxSelect>>', self.selector)
        scrollbar.config(command=self.listbox.yview)

        # Rechter frame pack
        welcome.pack(expand="true")

        # Linker frame grid
        rooms.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0, padx=5, pady=5)
        scrollbar.grid(row=1, column=1, sticky="NS")
        add.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        remove.grid(row=2, column=0, padx=0, pady=5, sticky="E")

    # Update the list on the left with the data found in the json.
    def updatelist(self):
        self.listbox.delete(0, 'end')   # delete all in listbox
        for values in self.datastore.getjson()["Kamers"]:  # get data from json
            self.listbox.insert(tk.END, values)  # add to listbox

    # toggle function to set the color for the listbox when removing items
    def RemRoom(self):
        if not self.toggle:
            self.toggle = True
            self.listbox.config(foreground="red")
        else:
            self.toggle = False
            self.listbox.config(foreground="black")

    # To select the items in the listbox
    # its also used for the remove function with the toggle value
    def selector(self, event):
        item = ""
        if not self.listbox.get(self.listbox.curselection()) == "":
            item = self.listbox.get(self.listbox.curselection())
        if self.toggle:
            title = "Weet u het zeker?"
            msg = "Wilt u de kamer "+item+" Verwijderen?"
            message = messagebox.askquestion(title=title, message=msg)
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
        add = tk.Button(frame, text="Toevoegen", width=25,
                        command=lambda: self.addRoomJson(inputbox.get()))

        back = tk.Button(frame, text="Annuleren", width=25,
                         command=lambda: self.master.showroom("homepage"))
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
            messagebox.showerror(title="Kamer toevoegen",
                                 message="Deze kamer bestaat al!")
        else:
            datajson["Kamers"][name] = {"Scherm": {}}
            self.data.writejson(datajson)
            self.master.showroom("homepage")


class RoomMenu(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.rframe = tk.LabelFrame(self, padx=5, pady=5)
        self.rframe.grid(row=0, column=1, padx=5, pady=5, rowspan=10)
        self.datastore = self.master.getdata()
        self.toggle = False
        self.room = ""
        self.sensor = ""
        self.serialconnections = {}

        lframe = tk.LabelFrame(self, padx=5, pady=5)
        lframe.grid(row=0, column=0, padx=5, pady=5)

        # Rechter frame widgets
        welcometxt = "Selecteer een sensor aan de linker kant om data te zien"
        welcome = tk.Label(self.rframe, wraplength=140, height=35, width=80,
                           text=welcometxt)
        backbtn = tk.Button(self.rframe, text="Terug naar kamers", width=70,
                            command=lambda: self.master.showroom('homepage'))

        # Linker frame widgets
        rooms = tk.Label(lframe, text="Schermen")
        add = tk.Button(lframe, text="+", width=7,
                        command=lambda: self.master.showroom('addsensor'))
        remove = tk.Button(lframe, text="-", width=7,
                           command=lambda: self.removeSensor())
        self.listbox1 = tk.Listbox(lframe, height=30)
        scrollbar = tk.Scrollbar(lframe)
        self.updatelist()

        # added some listbox config and added the events for selections
        self.listbox1.config(yscrollcommand=scrollbar.set)
        self.listbox1.event_generate('<<ListBoxSelect>>')
        self.listbox1.bind('<<ListboxSelect>>', self.selector)
        scrollbar.config(command=self.listbox1.yview)

        # Linker frame grid
        welcome.grid(row=1, column=0, sticky="NS")
        backbtn.grid(row=2, column=0)

        # Rechter frame grid
        rooms.grid(row=0, column=0)
        self.listbox1.grid(row=1, column=0, padx=5, pady=5)
        scrollbar.grid(row=1, column=1, sticky="NS")
        add.grid(row=2, column=0, padx=0, pady=5, sticky="W")
        remove.grid(row=2, column=0, padx=0, pady=5, sticky="E")

    def updatelist(self):
        self.listbox1.delete(0, 'end')
        if not self.room == "":
            for v in self.datastore.getjson()["Kamers"][self.room]["Scherm"]:
                self.listbox1.insert(tk.END, v)

    def removeSensor(self):
        if not self.toggle:
            self.toggle = True
            self.listbox1.config(foreground="red")
        else:
            self.toggle = False
            self.listbox1.config(foreground="black")

    def selector(self, event):
        item = ""
        if not self.listbox1.get(self.listbox1.curselection()) == "":
            item = self.listbox1.get(self.listbox1.curselection())
        if self.toggle:
            msg = "Wilt u de sensor "+item+" Verwijderen?"
            message = messagebox.askquestion(title="Weet u het zeker?",
                                             message=msg)
            if message == "yes":
                data = self.datastore.getjson()
                for i in data["Kamers"][self.room]["Scherm"]:
                    if item == i:
                        data["Kamers"][self.room]["Scherm"].pop(item)
                        self.datastore.writejson(data)
                        self.updatelist()
                        break
        else:
            self.sensordata(item)

    def updateroom(self):
        self.room = self.master.getselectedroom()
        aangeven = tk.Label(self.rframe, text=self.room+" : "+self.sensor)
        aangeven.grid(row=0, column=0)

    def sensordata(self, sensor):

        for widget in self.rframe.winfo_children():
            widget.destroy()
        self.rframe.grid(row=0, column=1, padx=5, pady=5, rowspan=10)
        lightframe = tk.LabelFrame(self.rframe, width=200, height=200, padx=5,
                                   pady=5)
        tempframe = tk.LabelFrame(self.rframe, width=200, height=200,  padx=5,
                                  pady=5)
        lightframe.grid(row=1, column=0, padx=40, pady=5)
        tempframe.grid(row=1, column=1, padx=40, pady=5)
        sensorcom = self.get_sensor(sensor)

        backbtn = tk.Button(self.rframe, text="Terug naar kamers", width=70,
                            command=lambda: self.master.showroom('homepage'))
        aangeven = tk.Label(self.rframe, text=self.room+":"+sensor)
        auto = tk.Button(self.rframe, text="Handmatige bediening", width=20,
                         command=lambda: self.buttonstate(auto))

        up = tk.Button(self.rframe, text="Omlaag", width=10,
                       command=lambda: sensorcom.send_byte(b'\x53'))
        down = tk.Button(self.rframe, text="Omhoog", width=10,
                         command=lambda: sensorcom.send_byte(b'\x52'))
        # licht sensor widgets
        graphframe = tk.Frame(lightframe)
        labellight = tk.Label(lightframe, text="Licht sensor")
        grafieken.LightGraph(graphframe, sensorcom)

        # warmte sensor widgets
        graphframe2 = tk.Frame(tempframe)
        labeltemp = tk.Label(tempframe, text="Warmte sensor")
        grafieken.TempGraph(graphframe2, sensorcom)

        # licht sensor grid
        labellight.grid(row=0, column=0, columnspan=1)
        graphframe.grid(row=1, column=0, columnspan=1)
        # canvaslight.grid(row=1, column=0, columnspan=1)

        # warmte sensor widgets
        labeltemp.grid(row=0, column=1, columnspan=1)
        graphframe2.grid(row=1, column=1, columnspan=1)
        # canvastemp.grid(row=1, column=1, columnspan=1)
        # main body grid
        aangeven.grid(row=0, column=0, columnspan=10)
        backbtn.grid(row=12, column=0, columnspan=10)
        auto.grid(row=2, column=0, columnspan=2)
        up.grid(row=3, column=0, sticky="E")
        down.grid(row=3, column=1, sticky="W")

        self.threshold_check(auto, sensorcom)

    def get_sensor(self, sensor):
        if sensor not in self.serialconnections:
            data = self.datastore.getjson()
            comport = data["Kamers"][self.room]["Scherm"][sensor]
            self.serialconnections[sensor] = grafieken.SensorData(comport)
        print(self.serialconnections)
        return self.serialconnections.get(sensor)

    def buttonstate(self, button):
        if button.config('relief')[-1] == 'sunken':
            button.config(relief="raised")
        else:
            button.config(relief="sunken")

    def threshold_check(self, button, arduino):
        light_threshold = 50  # randomly chosen
        open_command = b'\x53'
        close_command = b'\x52'
        # button not pressed, control it automatically.
        # the other relief state is sunken
        if button['relief'] == 'raised':
            # get the light data
            light_value = arduino.return_light()

            # check if its not empty
            if light_value != []:
                # get the latest light data value
                latest_value = light_value[-1][1]

                # check if the value is smaller than the threshold
                # if so, send the close command
                if latest_value < light_threshold:
                    arduino.send_byte(close_command)

                # else, send the open command
                else:
                    arduino.send_byte(open_command)

        # call this function every second
        self.after(1000, lambda: self.threshold_check(button, arduino))


class Addsensor(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        self.data = self.master.getdata()
        self.room = "none"
        self.listport = ["Niks gevonden"]

        # add frame around all the coponents
        frame = tk.LabelFrame(self, padx=5, pady=5)
        frame.grid(row=0, column=0, padx=5, pady=5,)

        # dropdown menu
        self.comport = tk.StringVar()
        self.comport.set(self.listport[0])
        self.dropdown = tk.OptionMenu(frame, self.comport, self.listport)
        # all the modules for the layout
        label = tk.Label(frame, text="Scherm toevoegen")
        labelname = tk.Label(frame, text="Naam:")
        labelcom = tk.Label(frame, text="Scherm:")
        inputbox = tk.Entry(frame)
        add = tk.Button(frame, text="Toevoegen", width=25,
                        command=lambda: self.SaveSensor(inputbox.get(),
                                                        self.comport.get()))
        back = tk.Button(frame, text="Annuleren", width=25,
                         command=lambda: self.master.showroom("roommenu"))
        # added a font and biger size for the label on the top
        label.config(font=("Courier", 30))

        # adding all the modules to the grid
        label.grid(row=0, columnspan=10)
        inputbox.grid(row=1, column=1)
        labelname.grid(row=1, column=0)
        labelcom.grid(row=2, column=0)
        self.dropdown.grid(row=2, column=1)
        add.grid(row=3, column=0)
        back.grid(row=3, column=1)
        # center the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def SaveSensor(self, name, comport):
        datajson = self.data.getjson()
        if name in datajson["Kamers"][self.room]["Scherm"]:
            messagebox.showerror(title="Scherm toevoegen",
                                 message="Deze is al in gebruik")
        else:
            datajson["Kamers"][self.room]["Scherm"][name] = comport
            self.data.writejson(datajson)
            self.master.showroom("roommenu")

    def updatecoms(self):
        self.room = self.master.getselectedroom()
        self.listport = []
        self.comport.set('')
        self.dropdown['menu'].delete(0, 'end')
        comports = serial.tools.list_ports.comports()
        if comports == []:
            self.listport.append("niet gevonden")
            messagebox.showerror(title="Geen schermen gevonden",
                                 message="Er zijn geen schermen aangesloten")
            return True
        else:
            for comport, hwid, devicename in sorted(comports):
                self.listport.append(comport)
                cmd = tk._setit(self.comport, comport)
                self.dropdown['menu'].add_command(label=comport,
                                                  command=cmd)
            return False
        self.comport.set(self.listport[0])


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.rooms = dict()
        self.data = backend.Data("config.json", "Kamers")
        self.datastore = self.data.getjson()
        self.lastroom = ""

        self.rooms['homepage'] = Homepage(self)  # call homepage
        self.rooms['addroom'] = AddRoom(self)    # Add a room page
        self.rooms['roommenu'] = RoomMenu(self)  # call roommenu
        self.rooms['addsensor'] = Addsensor(self)  # add sensor page

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        for i in self.rooms:
            self.rooms[i].place(in_=container, x=0, y=0, relwidth=1,
                                relheight=1)

        self.rooms['homepage'].show()       # show homepage first

    def showroom(self, room):
        if room == "homepage":
            self.rooms[room].updatelist()
        if room == "roommenu":
            self.rooms[room].updateroom()
            self.rooms[room].updatelist()
        if room == "addsensor":
            update = self.rooms[room].updatecoms()
            if update:
                self.rooms["roommenu"].show()
                return
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
