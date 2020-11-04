#include <asf.h>
#include "./inc_def.h"

int main (void){
	init();
	
	while(1){
		unsigned int distance;		// get the distance from the HCSR04
		distance = HCSR04_get_distance();
		char upper = (distance >> 8);
		char lower = (distance & 0xFF);
		USART_transmit(upper);
		USART_transmit(lower);
		_delay_ms(500);
	}
}

void init(){
	USART_init(MYUBRR);			// USART initialization
	
	ADC_init();					// analog to digital initialization
								// needed for the light and temp sensor
	
	HCSR04_init_pins();			// distance sensor initializations
	HCSR04_counter_init();
	HCSR04_interrupts_init();			
}
