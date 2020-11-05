#include <asf.h>
#include "./inc_def.h"

int main (void){
	init();
	scheduler_tasks();
	
	while(1){
		SCH_Dispatch_Tasks();
	}
}

void init(){
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
	SCH_Add_Task(send_light, 0, 10);
	SCH_Add_Task(send_temp, 5, 10);
	//SCH_Add_Task(send_distance, 0, 1);
}

void send_light(){
	char light_data;
	light_data = get_light();		// get light data
	USART_transmit(LIGHT_CODE);		// send byte signaling the data src
	USART_transmit(light_data);		// send data
}

void send_temp(){
	char temp_data;
	temp_data = get_temp();			// get temperature data
	USART_transmit(TEMP_CODE);		// send byte signaling the data source
	USART_transmit(temp_data);		// send data
}

void send_distance(){
	unsigned int distance;
	char distancel;						// lower distance byte var
	char distanceh;						// upper distance byte var
	
	distance = HCSR04_get_distance();	// get distance data
	
	distanceh = (distance>>8);			// split 16 bit distance data 
	distancel = (distance & 0xFF);		//		into 2 single bytes
	
	USART_transmit(DISTANCE_CODE);		// send byte signaling data source
	USART_transmit(distanceh);			// send higher distance byte
	USART_transmit(distancel);			// send lower distance byte
}
