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
timeout = 5
port = 'COM{}'.format(sys.argv[1])

def read():
	with serial.Serial(port, BAUD, timeout=timeout) as ser:
		while True:
			data = ser.read().hex()
			print('0x{}'.format(data))
