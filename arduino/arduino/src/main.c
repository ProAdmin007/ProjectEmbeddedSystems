#include <asf.h>
#include "./inc_def.h"

int main (void){
	init();
	while(1){
		_delay_ms(500);
		int light = get_light();
		int temp = get_temp();
		USART_transmit(light);
		USART_transmit(temp);
	}
}

void init(){
	USART_init(MYUBRR);
	ADC_init();
}
