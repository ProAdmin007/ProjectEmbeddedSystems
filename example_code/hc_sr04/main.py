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
from datetime import datetime

if len(sys.argv) == 1:
	raise Exception('\n\nNo arguments given for comport. Read main.py for more information.')

BAUD = 9600
timeout = 2
port = 'COM{}'.format(sys.argv[1])

def read(bytes_nr=1):
	with serial.Serial(port, BAUD, timeout=15) as ser:
		while True:
			data_hex = ser.read(bytes_nr).hex()
			timestr = datetime.now().strftime('%H:%M:%S')

			print('{} - 0x{}'.format(timestr, data_hex))


def cm_distance(counter_value):
	ms_elapsed = (int(counter_value, 16)*1000) / 2000
	cm_distance = round(ms_elapsed / 58, 2)
	return cm_distance