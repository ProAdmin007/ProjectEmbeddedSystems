/*
 * GccApplication2.c
 *
 * Created: 13-10-2020 14:35:18
 * Author : Sven
 */ 

#include <avr/io.h>
#include <util/delay.h>

//SERIAL -------------------------------------------------------------------
#define MYUBRR 103 // UBBRN value from atmega328p datasheet pagina 165
//END SERIAL ---------------------------------------------------------------

void ADC_Init(){
	DDRC  = 0x00;	/* set portC group to input*/
	ADCSRA = 0x87;
	ADMUX = 0x40;
}

int ADC_Read(char channel)
{
	ADMUX = 0x40 | (channel & 0x07);   /* set input channel to read */
	ADCSRA |= (1<<ADSC);               /* Start ADC conversion */
	while (!(ADCSRA & (1<<ADIF)));     /* Wait until end of conversion by polling ADC interrupt flag */
	ADCSRA |= (1<<ADIF);               /* Clear interrupt flag */
	_delay_ms(1);                      /* Wait a little bit :) */
	return ADCW;                       /* Return ADC word */
}


int main(void)
{	
	// initialize serial connection
	USART_Init(MYUBRR);
	// initialize Analog digital convector
	ADC_Init();
	float t;
    while (1) 
    {	
		t = "A";
		USART_Transmit((char) t);
    }
}

//------------------------------------------------------------------------------------------------------------------------------
void USART_Init(unsigned int ubrr){
	// set baud rate
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	
	// enable receiver and transmitter
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	
	// set frame format: 8data, 2stop bit
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);
}

void USART_Transmit(unsigned char data){
	while (!(UCSR0A & (1<<UDRE0)));
	UDR0 = data;
}
//------------------------------------------------------------------------------------------------------------------------------