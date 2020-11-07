#include "lights_definitions.h"
#include "lights_functions.h"
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/io.h>

void lights_init(){
	// set led pins as output
	DDRD |= (1<<LED_RED)|(1<<LED_YELLOW)|(1<<LED_GREEN);
}

// turns on the green LED
void lights_open(){
	PORTD &= ~((1<<LED_YELLOW)|(1<<LED_RED));	// turn of all leds except green
												// prevents potential flashing if screen already open
	PORTD |= (1<<LED_GREEN);					// turn on green LED
}

// turns on the red LED
void lights_closed(){
	PORTD &= ~((1<<LED_YELLOW)|(1<<LED_GREEN));	// turn of all leds except red
												// prevents potential flashing if screen already closed
	PORTD |= (1<<LED_RED);						// turn on red LED	
}

// turns on the yellow led, and after 750 ms, turns it off
// too blink while rolling out, keep calling this function
// as long as the screen is rolling out
void lights_busy(){
	PORTD |= (1<<LED_YELLOW);	// turn on yellow led
	_delay_ms(750);
	PORTD &= ~(1<<LED_YELLOW);	// turn of yellow led
	_delay_ms(750);
}
