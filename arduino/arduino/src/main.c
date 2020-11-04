#include <asf.h>
#include "./inc_def.h"

int main (void){
	init();
}

void init(){
	USART_init(MYUBRR);
	ADC_init();
}
