import serial
ser = serial.Serial('COM3', 9600,timeout=10)
ser.read(2)