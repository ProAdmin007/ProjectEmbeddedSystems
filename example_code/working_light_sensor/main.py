import serial
import sys

BAUD = 9600
timeout = 5
port = 'COM{}'.format(sys.argv[1])

def read():
	with serial.Serial(port, BAUD, timeout=timeout) as ser:
		while True:
			data = ser.read().hex()
			print('0x{}'.format(data))
