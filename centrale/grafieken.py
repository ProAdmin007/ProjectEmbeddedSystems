import tkinter as tk
import serial

from pprint import pprint
from datetime import datetime
import matplotlib.pyplot as plt

#plt.plot(*zip(*sensor_data['light']))

""""
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

fig = Figure(figsize=(5,4), dpi=100)
fig.add_subplot(111).plot(*zip(*sensor_data['light']))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
"""

class sensordata():
    def __init__(self, comport):
        self.conn = serial.Serial('COM{}'.format(comport), 9600, timeout=60)
        self.sensor_data = {'light': [], 'temperature': [], 'distance': []}

    def return_light(self):
        return self.sensor_data['light']

    def return_temp(self):
        return self.sensor_data['temperature']

    def return_dist(self):
        return self.sensor_data['distance']

    def readbyte(self):
        time = datetime.now().strftime('%H:%M:%S')
        byte = self.conn.read().hex()

        # dictionary for commands
        commands = {'41': 'distance',
                    '4c': 'light',
                    '54': 'temperature'}

        # check if the byte is in the command dictionary
        if byte in commands:
            # read the next byte
            data_byte = int(self.conn.read().hex(), 16)
            command = commands[byte]
            print('{} - {} - {}'.format(time, command, data_byte))

            # add the sensor data to the dictionary
            self.sensor_data[command].append((time, data_byte))

class lightgraph(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.data = sensordata(3)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.light_line = self.canvas.create_line(0,0,0,0, fill="red")
        self.update_plot()

    def update_plot(self):
        self.data.readbyte()
        data = self.data.return_light()

        if data == []:
            return

        # zip and unzip data from [(time, data), (time, data)....]
        # to [(time, time, time....), (data, data, data...)]
        data_zipped = zip(*data)
        data_unzipped = [*data_zipped]

        x_axis = data_unzipped[0]
        y_axis = data_unzipped[1]

        #self.add_point(self.velocity_line, x_axis)
        self.add_point(self.light_line, y_axis)
        self.canvas.xview_moveto(1.0)
        self.after(100, self.update_plot)

    def add_point(self, line, y):
        coords = self.canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)

        coords = coords[-200:]
        self.canvas.coords(line, *coords)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == '__main__':
    root = tk.Tk()
    lightgraph(root).pack()
    root.mainloop()