#include <asf.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <functions.h>

// amount of interrupts per second generated by counter 1
#define COUNTER1_INT_PS 1
#define F_CPU 16000000

int main(void){
	// enable interrupts
	sei();
	
	// set PIND as output
	DDRD = 0xFF;
	
	// initialize and start timers
	HCSR04_counter_init();
	HCSR04_start_counter();
	
	// loop forever while waiting on interrupts
	while(1);
}

void HCSR04_init(){
	
}

void HCSR04_start_counter(){
	// enable the counter, using the internal clock with a 1024 prescaler
	TCCR1B |= (1<<CS12);
}

// initialize the clock for the HC-SR04
// uses TCCR1A
void HCSR04_counter_init(){
	// set bit 6 and 7
	// OC1A will be set on an output compare match
	TCCR1A |= (1<<COM1A1) | (1<<COM1A0);
	
	// set the waveform generation mode
	// set bit WGM13
	// CTC mode = clear timer on compare
	TCCR1B |= (1<<WGM12);
	
	// disable the clock for now
	// clock will be enabled by setting CS02 and CS00 when the timer is needed
	// aka when a pulse needs to be send
	// with CS11 high the clock will use the internal clock with a pre-scaler of 8
	TCCR1B |= (0<<CS12);
	
	// enable the timer interrupt compare match A
	TIMSK1 |= (1<<OCIE1A);
	
	// set OCR1A
	// Fcpu = 16 MHz
	// prescaler = 256
	// pulses / sec = 1
	// OCR1A = (Fcpu / prescaler) / desired_freq
	
	OCR1A = (F_CPU / 256) / COUNTER1_INT_PS;
}
	
	
void interrupt_handler(){
	PORTD = ~PORTD;
}
// create an interrupt service routine for when the Output Compare flag on Timer0 (10ms pulse clock) is set
ISR (TIMER1_COMPA_vect){
	interrupt_handler();
}

