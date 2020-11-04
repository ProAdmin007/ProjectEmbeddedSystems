#include <avr/io.h>
#include "./definitions.h"
#include "./functions.h"

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


// example code for initializing a connection and sending data
/*int main(void){
	// initialize serial connection
	USART_Init(MYUBRR);
	while(1){
		USART_Transmit(0x69);
		// send data over serial connection
	}
}*/