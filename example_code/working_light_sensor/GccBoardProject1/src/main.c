#define F_CPU  16000000
#define myUBRR 103

#include <avr/io.h>
#include <functions.h>
#include <asf.h>
#include <util/delay.h>

int main (void){
	// initialize USART
	USART_init(myUBRR);

	// initialize ADC
	init_ADC();
		
	while(1){
		int light = get_light();
		USART_transmit(light);
		_delay_ms(500);
	}
}

void USART_init(unsigned int ubrr){
	// set baud rate
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	
	// enable receiver and transmitter
	UCSR0B = (1<<RXEN0) | (1<<TXEN0);
	
	// set frame format; 8 data, 2 stop bits
	UCSR0C = (1<<USBS0) | (3<<UCSZ00);
}

void USART_transmit(unsigned char data){
	// check if the UDRE register is high in UCSR0A
	// if it's high than the transmit buffer is ready to receive new data
	// which means the data can be sent
	while (!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

// initialize the Analog to Digital Converter
void init_ADC(void){
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

int get_light(void){
	// retrieve and analog value from port A2
	int light_value = get_analog(2);
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