import tkinter as tk
from pprint import pprint
from serial import Serial
from datetime import datetime
import matplotlib.pyplot as plt

s = Serial('COM3', 9600, timeout=60)
sensor_data = {'light':[], 'temperature':[], 'distance':[]}

def readbyte():
    time = datetime.now().strftime('%H:%M:%S')
    byte = s.read().hex()
    commands = {'41': 'distance', '4c': 'light', '54':'temperature'}
    if byte in commands:
        data_byte = int(s.read().hex(),16)
        command = commands[byte]
        print('{} - {} - {}'.format(time, command, data_byte))
        sensor_data[command].append((time, data_byte))

for i in range(5):
    readbyte()

plt.plot(*zip(*sensor_data['light']))
plt.show()
