import serial
ser = serial.Serial('COM3', 9600,timeout=10)
data = ser.read(2)
#data.split("x")
data_dict = {}
print("Datatype is: ",type(data))

dataInt = int.from_bytes(data, byteorder='big')

split_data = data[1:2]

dataInt2 = int.from_bytes(split_data, byteorder='big')

print("dit is data: ")
print(data)
print("dit is dataInt: ")
print(dataInt)
print("dit is split_data: ")
print(split_data)
print("dit is dataInt2: ")
print(dataInt2)
#print(int(data, 0))
