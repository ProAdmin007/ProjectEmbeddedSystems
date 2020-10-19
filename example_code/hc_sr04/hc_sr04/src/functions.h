/*
 * functions.h
 *
 * Created: 19/10/2020 14:04:15
 *  Author: Bram
 */ 


#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

void HCSR04_init(void);
void HCSR04_counter_init(void);
void HCSR04_start_counter(void);
void interrupt_handler(void);

#endif /* FUNCTIONS_H_ */