/*
 * functions.h
 *
 * Created: 13/10/2020 21:47:40
 *  Author: Bram
 */ 


#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void USART_init(unsigned int ubrr);
void USART_transmit(unsigned char data);
void init_ports(void);
void init_ADC(void);

int get_analog(int);
int get_light(void);

#endif /* FUNCTIONS_H_ */