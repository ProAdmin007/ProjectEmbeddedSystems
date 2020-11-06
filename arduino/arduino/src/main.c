#include <asf.h>
#include "./inc_def.h"

bool light_bool = 0;
bool temp_bool = 0;
bool distance_bool = 0;

void testlight(void){
	DDRD |= (1<<PIND4) | (1<<PIND5) | (1<<PIND6);
	PORTD |= (1<<PIND4) | (1<<PIND5) | (1<<PIND6);
}

int main (void){
	init();
	
	scheduler_tasks();
	
	while(1){
		SCH_Dispatch_Tasks();
		if(light_bool){
			send_light();
		}
		if(temp_bool){
			send_temp();
		}
		if(distance_bool){
			send_distance();
		}
		_delay_ms(50);
	}
}



void init(){
	// enable global interrupts
	sei();
	
	// USART initialization
	USART_init(MYUBRR);	
				
	// analog to digital initialization
	// needed for the light and temp sensor
	ADC_init();					
	
	// distance sensor initializations
	HCSR04_init_pins();	
	HCSR04_counter_init();
	HCSR04_interrupts_init();
	
	// scheduler initializations
	// scheduler is set to work with 1 second time slots
	SCH_Init_T1();				
}

void scheduler_tasks(){
	SCH_Add_Task(set_light_bool, 0, 15);
	SCH_Add_Task(set_temp_bool, 5, 15);
	SCH_Add_Task(set_distance_bool, 10, 15);
}

void send_light(){
	char light_data;
	light_data = get_light();		// get light data
	USART_transmit(LIGHT_CODE);		// send byte signaling the data src
	USART_transmit(light_data);		// send data
	light_bool = 0;
}

void send_temp(){
	char temp_data;
	temp_data = get_temp();			// get temperature data
	USART_transmit(TEMP_CODE);		// send byte signaling the data source
	USART_transmit(temp_data);		// send data
	temp_bool = 0;
}

void send_distance(){
	char distance_data;
	distance_data = HCSR04_get_distance();	// get distance data
	USART_transmit(DISTANCE_CODE);			// send byte signaling data source
	USART_transmit(distance_data);			// send distance data
	distance_bool = 0;
}

void set_light_bool(){
	light_bool = 1;
}

void set_distance_bool(){
	distance_bool = 1;
}

void set_temp_bool(){
	temp_bool = 1;
}

