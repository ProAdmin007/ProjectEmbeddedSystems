/*
 * functions.h
 *
 * Created: 13/10/2020 21:47:40
 *  Author: Bram
 */ 


#ifndef ANALOG_FUNCTIONS_H_
#define ANALOG_FUNCTIONS_H_

void ADC_init(void);

int get_analog(int);
int get_temp(void);
int get_light(void);

#endif /* ANALOG_FUNCTIONS_H_ */