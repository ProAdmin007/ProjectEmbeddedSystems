import serial
import time
import re 
import csv 
import numpy as np 

sample_time = 0.1

#list met tmp data
tmpList = []

#verander de com port naar de goeie poort!
ser = serial.Serial('COM3', 9600,timeout=10)
ser.read(2)

#berekeing
temperatureC = (5 - 0.5) * 100

# Collecting the data from the serial port 
while True: 
    line = ser.readline()
    line_data = re.findall('\d*\.\d*',str(line))
    line_data = filter(None,line_data)
    line_data = [float(x) for x in line_data]
    if len(line_data) > 0:
        print(line_data[0])
