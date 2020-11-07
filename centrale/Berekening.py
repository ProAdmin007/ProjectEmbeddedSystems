import serial

# open connectie op poort COM1
ser = serial.Serial('COM3', 9600,timeout=10)

# infenent loop to read data
while True:
    # read the first command
    # leest het eerste bit
    # 0x41 => next byte is distance data
    # 0x4C => next byte is light data
    # 0x54 => next byte is temp data
    command = ser.read().hex()
    if command == '41':
        dist_data = ser.read().hex()
        dist_dec = int(dist_data, 16)
        #print('distance - 0x{}'.format(dist_data))
        print('Distance in decimaal = ',dist_dec)
    if command == '4c':
        light_data = ser.read().hex()
        light_dec = int(light_data, 16)
        #print('light - 0x{}'.format(light_data))
        print('Light in decimaal = ',light_dec)
    if command == '54':
        temp_data = ser.read().hex()
        voltageOut = (int(temp_data, 16) * 5000) / 1024
        temperatureC = round((voltageOut / 10) * 4)
        #print('temp - 0x{}'.format(temp_data))
        print('Temp in C = ',temperatureC)