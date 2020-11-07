#include <avr/io.h>
#include "./USART_definitions.h"
#include "./USART_functions.h"

void USART_init(unsigned int ubrr){
	// set baud rate
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	
	// enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	
	// set frame format: 8data, 2 stop bit
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);
}

void USART_transmit(unsigned char data){
	while (!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}

uint8_t USART_unread_data(){
	// check if RXC0 is set, aka
	// is there unread data
	if((UCSR0A >> RXC0)&1){
		return 1;
	}
	return 0;
}

unsigned char USART_receive(){
	// Wait for data to be received
	while (!(UCSR0A & (1<<RXC0)));
	// Get and return received data from buffer
	return UDR0;
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