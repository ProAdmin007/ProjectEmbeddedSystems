import serial
import time

ser = serial.Serial('COM1', 9600,timeout=10) #open connectie op poort COM1
data = ser.read(1) # leest het eerste bit

data_dict = {} # Placeholder dict

dataInt = int.from_bytes(data, byteorder='big') # Bytes naar int omzetten

# Dat naar hex functie
dataString = data.hex()
print("Hex data bit 1: ",dataString)

# Test print statmens
print("dit is Bit1: ")
print(data)
print("dit is Bit2: ")
data2 = ser.read(1)
dataInt2 = int.from_bytes(data2, byteorder='big')
print(dataInt2)
print("dit is Bit3: ")
data3 = ser.read(1)
print(data3)
print("dit is Bit4: ")
data4 = ser.read(1)
print(data4)
print("dit is dataInt: ")
print(dataInt)

i = 100
while i == 100: # Infenet loop
    if data == bytes(b'L'): # If die checkt of het lichtdata is
        print("Data is Lichtdata")
        bit2 = ser.read(2)
        print(bit2)
        lichtData = bit2[1:4]
        print(lichtData)
        print(int.from_bytes(lichtData, byteorder='big'))

    if data3 == bytes(b'T'): # If die checkt of het tempratuurdata is
        print("Data is Tempdata")
        bit4 = ser.read(2)
        print(bit4)
        tempData = bit4[1:3]
        print(tempData)
        print(int.from_bytes(tempData, byteorder='big'))
