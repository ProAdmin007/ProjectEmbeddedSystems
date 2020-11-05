#include <asf.h>
#include "./inc_def.h"

int main (void){
	init();
	
}

void init(){
	USART_init(MYUBRR);			// USART initialization
	
	ADC_init();					// analog to digital initialization
								// needed for the light and temp sensor
	
	HCSR04_init_pins();			// distance sensor initializations
	HCSR04_counter_init();
	HCSR04_interrupts_init();
	
	SCH_Init_T1();				// scheduler initializations
								// scheduler is set to 1 second time slots
}
