def calc_OCR1A():
	Fcpu = 16000000
	prescaler = int(input("Prescaler value= "))
	desired_freq = int(input("How many pulses a second? "))
	return (Fcpu // prescaler) // desired_freq

OCR1A = calc_OCR1A()
print("OCR1A needs to be {} = {}".format(OCR1A, hex(OCR1A)))