/*
 * functions.h
 *
 * Created: 19/10/2020 14:04:15
 *  Author: Bram
 */ 


#ifndef HCSR04_FUNCTIONS_H_
#define HCSR04_FUNCTIONS_H_

void HCSR04_init_pins(void);
void HCSR04_counter_init(void);
void HCSR04_send_pulse(void);
char HCSR04_get_distance(void);

void HCSR04_interrupts_init(void);

#endif /* HCSR04_FUNCTIONS_H_ */