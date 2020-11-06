/*********************************************************************************

This script send a 2 byte value correlated to the distance the HCSR04 is measuring
Using: 
				    Fcpu = 16 MHz
		      Pre-scaler =  8	
Counter after pre-scaler =  2 MHz

We can calculate that:
time_sec = counter_value / 2.000.000
time_ms  = counter_value / 2.000
distance_cm = (time_ms / 58) * 1000

*********************************************************************************/

#define F_CPU				16E6

#include <asf.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "./HCSR04_functions.h"
#include "./HCSR04_definitions.h"

volatile char counter;
volatile int echorecv = 0;

unsigned int distance_time;
void adsf(void){
	DDRD |= (1<<PIND4) | (1<<PIND5) | (1<<PIND6);
	PORTD |= (1<<PIND4) | (1<<PIND5) | (1<<PIND6);
}
char HCSR04_get_distance(){
	HCSR04_send_pulse();			// send a pulse
	while(echorecv != 1);			// wait for the echo to be sent back

	return counter;
// 	HCSR04_send_pulse();				// send a pulse
// 	while(echorecv != 1);				// wait for the echo to be sent back
// 	
// 	unsigned int distance = 0x00;		// clear distance int
// 
// 	distance |= (counter_h<<8);			// set higher byte of distance int
// 	distance |= (counter_l);			// set lower byte
// 	
// 	return distance_time;
}

void HCSR04_interrupts_init(){
	EICRA = (0<<ISC11)|(1<<ISC10);	// set the external interrupt to trigger any logical change
	EIMSK = (1<<INT1);				// enable external interrupt on INT1
}

// pulls the trigger high for 15 ms, making the HCSR04 send a pulse
void HCSR04_send_pulse(){
	PORTB = (1<<TRIGGER_PIN);		// set trigger high
	_delay_ms(15);					// wait 15 ms (trigger has to be at least 10ms)
	PORTB = (0<<TRIGGER_PIN);		// set trigger low
}

// initialize the HCSR04 pins
void HCSR04_init_pins(){
	// laag = input
	// hoog = output
	DDRD |= (0<<ECHO_PIN);		// PIND3 -> INT1
	DDRB |= (1<<TRIGGER_PIN);	// PINB0
}

// initialize the clock for the HC-SR04
// uses TCCR1A
void HCSR04_counter_init(){
	TCCR0A = 0x00;				// clear all timer settings just to be sure
	TCCR0B = 0x00;				// no need to enable any additional options, standard is fine
}

// triggers on a logical change on INT1
ISR (INT1_vect){
	if (TCCR0B == 0x00){		// check if timer is disabled
	
		echorecv = 0;			// set echo received flag low

		TCNT0 = 0x00;			// clear timer
		
		counter = 0x00;			// clear counter
		
		TCCR0B = (1<<CS02);		// enable timer, with a pre-scaler of 8. 
								// the pre-scaler prevents the timer from overflowing 
								// if there is nothing in front of the sensor
		return;					// exit the ISR
	}
	if (TCCR0B == (1<<CS02)){	// check if the timer is enabled
		TCCR0B = 0x00;			// disable the timer
	
		counter = TCNT0;		// copy timer into counter var

		TCNT0 = 0x00;			// clear timer
		
		echorecv = 1;			// set echo received flag high
		return;					// exit the ISR
	}
}