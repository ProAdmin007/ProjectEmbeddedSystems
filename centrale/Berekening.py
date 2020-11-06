import serial
import time

ser = serial.Serial('COM1', 9600,timeout=10)
data = ser.read(1)
#data.split("x")
data_dict = {}
#print("Datatype is: ",type(data))
#print(ser.read(24))
#split_data = data[1:2]

dataInt = int.from_bytes(data, byteorder='big')
dataString = data.hex()
print("Hex data bit 1: ",dataString)

""" teller=1
while teller<=1:
    data_dict.update({data[0:1]:data[1:2]})
    #data.update({'c':3,'d':4})  # Updates 'c' and adds 'd'
    time.sleep(5)
    print(teller)
    teller+=1
 """
#dataInt2 = int.from_bytes(split_data, byteorder='big')

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
#print("dit is split_data: ")
#print(split_data)
#print("dit is dataInt2: ")
#print(dataInt2)
print("dit is data_dict: ")
for item in data_dict.items():
    print(item)

i = 100
while i == 100:
    #concept ifje
    if data == bytes(b'L'):
        print("Data is Lichtdata")
        bit2 = ser.read(2)
        print(bit2)
        lichtData = bit2[1:4]
        print(lichtData)
        print(int.from_bytes(lichtData, byteorder='big'))

    if data3 == bytes(b'T'):
        print("Data is Tempdata")
        bit4 = ser.read(4)
        print(bit4)
        tempData = bit4[1:3]
        print(tempData)
        print(int.from_bytes(tempData, byteorder='big'))
