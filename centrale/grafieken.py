import tkinter as tk
import serial

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime


class SensorData:
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


class Graph(tk.Frame):
    def __init__(self, sensor_obj, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.data = sensor_obj
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas.get_tk_widget().pack()
        self.update_plot()

    def update_plot(self):
        self.data.readbyte()
        data = self.get_data()

        # zip and unzip data from [(time, data), (time, data)....]
        # to [(time, time, time....), (data, data, data...)]
        data_zipped = zip(*data)
        data_unzipped = [*data_zipped]

        x_axis = data_unzipped[0]
        y_axis = data_unzipped[1]

        # self.add_point(self.velocity_line, x_axis)
        self.draw_graph(x_axis, y_axis)
        self.after(10000, self.update_plot)

    def get_data(self):
        pass

    def draw_graph(self, x, y):
        self.fig.add_subplot(111).plot(x, y)
        self.canvas.draw()


class LightGraph(Graph):
    def __init__(self, master, sensor_obj):
        self.sensor_obj = sensor_obj
        Graph.__init__(self, sensor_obj)

    def get_data(self):
        return self.sensor_obj.return_light()


class TempGraph(Graph):
    def __init__(self, master, sensor_obj):
        self.sensor_obj = sensor_obj
        Graph.__init__(self, sensor_obj)

    def get_data(self):
        return self.sensor_obj.return_temp()


if __name__ == '__main__':
    root = tk.Tk()
    sensors_com3 = SensorData(3)
    LightGraph(root, sensors_com3).pack()
    TempGraph(root, sensors_com3).pack()
    root.mainloop()
