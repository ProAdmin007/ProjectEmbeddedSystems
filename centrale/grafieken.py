import tkinter as tk
import serial

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


# SensorData object
# An object for getting light and temperature data from an Arduino.
# Takes a comport as argument.
# Creates a dictionary of sensor data. Sensor data is a list of tuples,
#   with each tuple containing the time and sensor value at that time.
# Can return light, temperature or distance data in this format.
class SensorData:
    def __init__(self, comport):
        self.conn = serial.Serial(comport, 9600, timeout=60)
        self.sensor_data = {'light': [], 'temperature': [], 'distance': []}

    # return the light data
    def return_light(self):
        return self.sensor_data['light']

    # return the temperature data
    def return_temp(self):
        return self.sensor_data['temperature']

    # return the distance data
    def return_dist(self):
        return self.sensor_data['distance']

    # reads a byte. if it is a known data identifier byte, it will read
    #   the next byte and write the data to the corresponding list
    def readbyte(self):
        # get the current time
        time = datetime.now().strftime('%H:%M:%S')

        # read a byte
        byte = self.conn.read().hex()

        # dictionary for commands
        commands = {'41': 'distance',
                    '4c': 'light',
                    '54': 'temperature'}

        # check if the read byte is in the command dictionary
        if byte in commands:
            # read the next byte
            data_byte = int(self.conn.read().hex(), 16)
            command = commands[byte]

            # add the sensor data to the dictionary
            self.sensor_data[command].append((time, data_byte))


# Graph Object
# The parent object for the graphs.
# Takes a sensor object (basically a serial connection with an arduino).
# Implements most of the functions needed in the light and temp graph,
#   those only need to override the get_data function.
# Graphs will automatically update every 10 seconds.
class Graph(tk.Frame):
    def __init__(self, master, sensor_obj, *args, **kwargs):
        tk.Frame.__init__(self, master, width=200, height=200, *args, **kwargs)
        self.data = sensor_obj
        self.fig = Figure(figsize=(2, 2), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)

        self.canvas.get_tk_widget().grid(row=1, column=0)
        self.update_plot()

    def update_plot(self):
        # read the next byte and data
        self.data.readbyte()
        data = self.get_data()

        # zip and unzip data from [(time, data), (time, data)....]
        # to [(time, time, time....), (data, data, data...)]
        data_zipped = zip(*data)
        data_unzipped = [*data_zipped]

        # get x-axis and y-axis data
        x_axis = data_unzipped[0]
        y_axis = data_unzipped[1]

        # draw the graph
        # rerun this function automatically after 10 seconds
        self.draw_graph(x_axis, y_axis)
        self.after(10000, self.update_plot)

    # override this function in the child classes with the source of the data
    def get_data(self):
        return [0, 0]

    # draws the graph
    def draw_graph(self, x, y):
        self.fig.add_subplot(111).plot(x, y)
        self.canvas.draw()


# LightGraph object
# Overrides the Graph objects get_data function to use the light data
class LightGraph(Graph):
    def __init__(self, master, sensor_obj):
        self.sensor_obj = sensor_obj
        Graph.__init__(self, master, sensor_obj)

    def get_data(self):
        return self.sensor_obj.return_light()


# TempGraph object
# Overrides the Graph objects get_data function to use the temp data
class TempGraph(Graph):
    def __init__(self, master, sensor_obj):
        self.sensor_obj = sensor_obj
        Graph.__init__(self, master, sensor_obj)

    def get_data(self):
        return self.sensor_obj.return_temp()


if __name__ == '__main__':
    root = tk.Tk()
    sensors_com3 = SensorData('COM3')
    LightGraph(root, sensors_com3).pack()
    TempGraph(root, sensors_com3).pack()
    root.mainloop()
