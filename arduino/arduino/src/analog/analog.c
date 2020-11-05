#include <avr/io.h>
#include "./analog_definitions.h"
#include "./analog_functions.h"

// initialize the Analog to Digital Converter
void ADC_init(void){
	// disable the power reduction ADC bit
	PRR = (0<<PRADC);
	
	// set the ADMUX register
	// set REFS1 high and REFS0 low -> use AVcc as reference voltage
	// set ADLAR high -> ADC Left Adjust to use only 8 bits resolution
	ADMUX = (0 << REFS1) | (1 << REFS0) | (1 << ADLAR);
	
	// IMPORTANT
	// set the ADC pre-scaler register
	// the ADC requires a clock speed between 50KHz and 200Khz
	// all three bits high is a pre-scaler of 128
	// which gives us a ADC clock speed of 16Mhz / 128 = 125KHz
	// not setting these bits gives garbage data (0xFF), since the default clock speed is 16MHz
	ADCSRA |= (0b0111);
	
	// set the Enable ADC bit
	ADCSRA |= (1 << ADEN);
}

int get_temp(void){
	// retrieve analog value from the temp sensor
	int temp_value = get_analog(TEMP_PIN);
	return temp_value;
}

int get_light(void){
	// retrieve analog value from the light sensor
	int light_value = get_analog(LIGHT_PIN);
	return light_value;
}

int get_analog(int pin){
	// failsafe
	// if the pin > 3, you could override some of the important settings bits.
	// so if pin > 3, return 0xEE
	// if you only receive 0xEE, something went wrong with the pin definition
	if(pin > 3){
		return 0xEE;
	}
	
	// clear everything in ADMUX except low 4 high bits
	// done so we can define a new port to read based on the given argument
	ADMUX &= 0xF0;
	
	// set the desired input pin
	// the to be used pin correspond to the binary representation of that pin
	// so  pin 0 = 0b0000 -> decimal 0
	//     pin 1 = 0b0001 -> decimal 1
	//     pin 2 = 0b0010 -> decimal 2
	//	   pin 3 = 0b0011 -> decimal 3
	// where these 4 bits are the 4 low bits in ADMUX
	// see atmega328p data sheet page 218 for more
	ADMUX |= pin;
	
	// start a conversion by setting the start conversion bit in ADCSRA
	ADCSRA |= (1<<ADSC);
	
	// check if a conversion has been completed, AKA if ADIF is high in ADCSRA
	while(!(ADCSRA & (1<<ADIF)));
	
	// return the value of the conversion
	// since we use a left adjust we only have to read ADCH
	// TODO: maybe change function to return both ADCL and ADCH for better resolution
	//		 don't forget to change ADLAR in ADMUX to 0 when doing the above
	return ADCH;
}