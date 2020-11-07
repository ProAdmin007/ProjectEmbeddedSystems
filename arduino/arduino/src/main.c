#include <asf.h>
#include "./inc_def.h"

bool light_ready = false;
bool temp_ready = false;
bool distance_ready = false;

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
		_delay_ms(50);
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
	SCH_Add_Task(set_light_bool, 0, 3);
	SCH_Add_Task(set_temp_bool, 1, 3);
	SCH_Add_Task(set_distance_bool, 2, 3);
}

void send_light(){
	char light_data;
	light_data = get_light();		// get light data
	USART_transmit(LIGHT_CODE);		// send byte signaling the data src
	USART_transmit(light_data);		// send data
	light_ready = 0;
}

void send_temp(){
	char temp_data;
	temp_data = get_temp();			// get temperature data
	USART_transmit(TEMP_CODE);		// send byte signaling the data source
	USART_transmit(temp_data);		// send data
	temp_ready = 0;
}

void send_distance(){
	char distance_data;
	distance_data = HCSR04_get_distance();	// get distance data
	USART_transmit(DISTANCE_CODE);			// send byte signaling data source
	USART_transmit(distance_data);			// send distance data
	distance_ready = 0;
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
	if(screen_state != SCREEN_OPEN){
		while(HCSR04_get_distance() > 0x12){
			lights_busy();
		}
		lights_open();
	}
}

void screen_close(){
	if(screen_state != SCREEN_CLOSED){
		while(HCSR04_get_distance() < 0x4A){
			lights_busy();
		}
		lights_closed();
	}
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