/*
 * defines.h
 *
 * Created: 04/11/2020 22:28:45
 *  Author: Bram
 */ 


#ifndef USART_DEFINITIONS_H_
#define USART_DEFINITIONS_H_

// clock speed arduino == 16.000.000 Hz
// baud rate to be used == 9600
// USART baud rate register (UBRR) == (clockspeed / (16* baudrate)) - 1
// so our UBRR == 103
// can also be found as example value,
// on the atmega328p datasheet page 165
#define MYUBRR 103

#endif /* USART_DEFINITIONS_H_ */