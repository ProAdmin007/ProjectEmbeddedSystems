/*
 * definitions.h
 *
 * Created: 04/11/2020 22:22:49
 *  Author: Bram
 */ 


#ifndef INC_DEF_H_
#define INC_DEF_H_

/* INCLUDES */

// USART files
#include "./USART/USART_definitions.h"
#include "./USART/USART_functions.h"

// temperature and light sensor files
#include "./analog/analog_definitions.h"
#include "./analog/analog_functions.h"

#define F_CPU 16E6
#include <util/delay.h>

/* FUNCTIONS */

void init(void);

#endif /* INC_DEF_H_ */