#include <asf.h>
#include "./inc_def.h"

bool light_ready = false;
bool temp_ready = false;
bool distance_ready = false;

uint16_t light_avg_total;
uint16_t light_avg_count;
uint16_t temp_avg_total;
uint16_t temp_avg_count;
uint16_t dist_avg_total;
uint16_t dist_avg_count;

char screen_state;

int main (void){
	init();
	screen_state = SCREEN_OPEN;
	lights_open();
	scheduler_tasks();
	
	while(1){
		SCH_Dispatch_Tasks();
		if(light_ready){
			send_light();
		}
		if(temp_ready){
			send_temp();
		}
		if(distance_ready){
			send_distance();
		}
		check_command();
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
	
	// lights initialization
	lights_init();		
}

void scheduler_tasks(){
	SCH_Add_Task(avg_light, 0, 1);				// average light measured in second increments
	SCH_Add_Task(avg_temp, 0, 1);				// average temp measured in second increments
	SCH_Add_Task(avg_dist, 0, 1);				// average distance measured in second increments
	
	SCH_Add_Task(set_light_bool, 5, 10);		// average light sent every 30 seconds
	SCH_Add_Task(set_temp_bool, 5, 15);			// average temp sent every 40 seconds
	SCH_Add_Task(set_distance_bool, 5, 30);		// average distance sent every 60 seconds
}

void send_light(){
	char light_data;
	light_data = light_avg_total / light_avg_count;		// calculate average light value
	
	light_avg_count = 0;								// reset total of all values
	light_avg_total = 0;								// reset total count

	USART_transmit(LIGHT_CODE);							// send byte signaling the data source
	USART_transmit(light_data);							// send data
	light_ready = 0;
}

void send_temp(){
	char temp_data;
	temp_data = temp_avg_total / temp_avg_count;		// calculate average temp value
	
	temp_avg_count = 0;									// reset total of all values
	temp_avg_total = 0;									// reset total counts
	
	USART_transmit(TEMP_CODE);							// send byte signaling the data source
	USART_transmit(temp_data);							// send data
	temp_ready = 0;
}

void send_distance(){
	if(dist_avg_count != 0){
		char distance_data;
		distance_data = dist_avg_total / dist_avg_count;	// calculate average distance
	
		dist_avg_count = 0;									// reset total of all values
		dist_avg_total = 0;									// reset total counts	
	
		USART_transmit(DISTANCE_CODE);						// send byte signaling data source
		USART_transmit(distance_data);						// send distance data
		distance_data = 0x00;
		distance_ready = 0;
	}
}

/*-----------------------------------
Since the scheduler uses an interrupt
to handle the scheduled tasks, we
can't directly call the send_[x]
functions in the scheduler tasks.

This is because the distance sensor
also uses interrupts in it's
implementation.

To fix this, we use a couple of
booleans to 
-----------------------------------*/

void set_light_bool(){
	light_ready = true;
}

void set_distance_bool(){
	distance_ready = true;
}

void set_temp_bool(){
	temp_ready = true;
}


/*----------------------------------
These functions (simulate) open(ing)
the screen. If the screen is already
in the state it should be in, than
the function does nothing.
----------------------------------*/

void screen_open(){
	while(HCSR04_get_distance() > 0x12){
		lights_busy();
	}
	lights_open();
}

void screen_close(){
	while(HCSR04_get_distance() < 0x4A){
		lights_busy();
	}
	lights_closed();
}

/*--------------------------------------
This function checks if the computer
sent us a command to do something. 

It works by checking whether there is
unread data in the RX0 buffer. The
function does nothing if there is no
data ready in the buffer, so it can be
called repeatetly without getting
stuck.

If a command is found, it executes it
immediately. If a command is not known,
the function does nothing.
--------------------------------------*/

void check_command(){
	if(USART_unread_data() == 1){
		char command = USART_receive();

		if((command == SCREEN_OPEN)&(screen_state == SCREEN_CLOSED)){
			screen_open();
			screen_state = SCREEN_OPEN;
		}
		if((command == SCREEN_CLOSED)&(screen_state == SCREEN_OPEN)){
			screen_close();
			screen_state = SCREEN_CLOSED;
		}
	}
}

/*-----------------------------------------------------
These functions and variables are used to calculate the
average values of the temperature and light sensor. 

Averages are calculated by measuring the data from
the sensor every second between sending the data, and
dividing it by the seconds that have passed.

These are called every second by the scheduler. Right
before the data is sent, the average is calculated and
send as the light or temperature data.
-----------------------------------------------------*/
void avg_light(){
	light_avg_total += get_light();
	light_avg_count += 1;
}

void avg_temp(){
	temp_avg_total += get_temp();
	temp_avg_count += 1;
}

void avg_dist(){
	dist_avg_total += HCSR04_get_distance();
	dist_avg_count += 1;
}