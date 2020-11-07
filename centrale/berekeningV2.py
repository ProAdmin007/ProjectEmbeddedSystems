import serial

ser = serial.Serial('COM3', 9600,timeout=10) #open connectie op poort COM1


while True:
    # read the first command
    # leest het eerste bit
    # 0x41 => next byte is distance data
    # 0x4C => next byte is light data
    # 0x54 => next byte is temp data
    command = ser.read().hex()
    if command == '41':
        dist_data = ser.read().hex()
        print('distance - 0x{}'.format(dist_data))
    if command == '4c':
        light_data = ser.read().hex()
        print('light - 0x{}'.format(light_data))
    if command == '54':
        temp_data = ser.read().hex()
        print('temp - 0x{}'.format(temp_data))