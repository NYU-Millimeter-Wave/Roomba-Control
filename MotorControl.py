#!/usr/bin/env python 
#
# MotorControl.py
# 
# Roomba-Control 
# New York University (c) 2016
# 

import RPi.GPIO as GPIO, time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(16, 500)

def SpinMotor(direction, num_steps):
	GPIO.output(18, direction)
	while num_steps > 0:
		p.start(1)
		time.sleep(0.01)
		num-steps -=1
	p.stop()
	GPIO.cleanup()
	return True

direction_input = raw_input('Please enter C or O for Close or Open:')
num_steps = input('Please enter the number of steps:')
if direction_input == 'C':
	SpinMotor(False, num_steps)
else:
	SpinMotor(True, num_steps)

