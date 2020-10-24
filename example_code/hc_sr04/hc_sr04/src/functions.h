/*
 * functions.h
 *
 * Created: 19/10/2020 14:04:15
 *  Author: Bram
 */ 


#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void HCSR04_init_pins(void);
void HCSR04_counter_init(void);
void HCSR04_start_counter(void);
void HCSR04_send_pulse(void);
void HCSR04_time_distance(void);
void HCSR04_get_distance(void);

void interrupts_init(void);

void USART_Init(unsigned int);
void USART_Transmit(unsigned char);

#endif /* FUNCTIONS_H_ */