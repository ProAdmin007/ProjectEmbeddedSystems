#include <avr/io.h>
#include <functions.h>

// clock speed arduino == 16.000.000 Hz
// baud rate to be used == 9600
// USART baud rate register (UBRR) == (clockspeed / (16* baudrate)) - 1
// so our UBRR == 103
// can also be found as example value,
// on the atmega328p datasheet page 165
#define MYUBRR 103


int main(void){
	// initialize serial connection
	USART_Init(MYUBRR);
	while(1){
		USART_Transmit(0x69);
		// send data over serial connection
	}
}

void USART_Init(unsigned int ubrr){
	// set baud rate
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	
	// enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	
	// set frame format: 8data, 2 stop bit
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);
}

void USART_Transmit(unsigned char data){
	while (!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

void init_ports(void){
	// pin high == output
	// pin low == input
	// pinA0 == input button 1
	// pinA1 == input button 2
	// pinA2 == input light sensor
	// pinA3 == input temp sensor
	
	// pinD2 == output led
	// pinD3 == output led
	// pinD4 == output led
	
	// pinB0 == sonar echo
	// pinB1 == sonar trigger
}