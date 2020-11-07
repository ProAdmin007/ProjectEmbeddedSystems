/*
 * functions.h
 *
 * Created: 04/11/2020 22:28:53
 *  Author: Bram
 */ 

#ifndef USART_FUNCTIONS_H_
#define USART_FUNCTIONS_H_

void USART_init(unsigned int);
void USART_transmit(unsigned char);
unsigned char USART_receive(void);
uint8_t USART_unread_data(void);

#endif /* USART_FUNCTIONS_H_ */