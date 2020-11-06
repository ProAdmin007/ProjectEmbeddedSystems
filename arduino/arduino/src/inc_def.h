/*
 * definitions.h
 *
 * Created: 04/11/2020 22:22:49
 *  Author: Bram
 */ 


#ifndef INC_DEF_H_
#define INC_DEF_H_

/* DEFINES */

// protocol
#define DISTANCE_CODE 0x41
#define LIGHT_CODE 0x4C
#define SCREEN_OPEN 0x53
#define SCREEN_CLOSED 0x52
#define TEMP_CODE 0x54

// 

/* INCLUDES */

// USART files
#include "./USART/USART_definitions.h"
#include "./USART/USART_functions.h"

// temperature and light sensor files
#include "./analog/analog_definitions.h"
#include "./analog/analog_functions.h"

// distance sensor files
#include "./HCSR04/HCSR04_definitions.h"
#include "./HCSR04/HCSR04_functions.h"

// scheduler files
#include "./scheduler/AVR_TTC_scheduler.h"

#define F_CPU 16E6
#include <util/delay.h>

/* FUNCTIONS */

void init(void);

void scheduler_tasks(void);

void send_light(void);
void send_temp(void);
void send_distance(void);

void set_light_bool(void);
void set_temp_bool(void);
void set_distance_bool(void);

#endif /* INC_DEF_H_ */