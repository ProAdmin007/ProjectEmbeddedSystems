'''
PYTHON SERIAL DEBUGGING CODE
HOW TO USE:
1. run script in terminal with the -i flag and with a comport number as argument (python -i main.py)
   e.g. 'python -i main.py 3'
2. to continuously print recieved data, type read()
3. python will now print all received data to the console
4. to stop reading, use a keyboard interrupt (CTRL+C)
5. the connection to the arduino will close automatically
6. flash a new version of your C code and start again at step 2, no need to stop python
7. ???
8. profit
'''

import serial
import sys

if len(sys.argv) == 1:
	raise Exception('\n\nNo arguments given for comport. Read main.py for more information.')

BAUD = 9600
timeout = 2
port = 'COM{}'.format(sys.argv[1])

def read(bytes_nr=1):
	with serial.Serial(port, BAUD, timeout=timeout) as ser:
		while True:
			data_hex = ser.read(bytes_nr).hex()
			data_nr = str(data_hex)
			if data_nr == '':
				data_nr = '0'
			data_nr = int(data_nr, 16)
			print('0x{} - {}'.format(data_hex, data_nr))
