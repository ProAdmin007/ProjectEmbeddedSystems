/*
 * functions.h
 *
 * Created: 09/10/2020 15:16:21
 *  Author: Bram
 */ 


#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void init_ports(void);
void USART_Init(unsigned int ubrr);
void USART_Transmit(unsigned char data);

#endif /* FUNCTIONS_H_ */