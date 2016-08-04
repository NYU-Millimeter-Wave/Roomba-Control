import datetime
import serial
import time
import sys
import testclass
import turtle
import numpy as np
import Tkinter as tk

# main

ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
ser.flushInput()
robot = testclass.Roomba()
robot._start()
robot._safe()
time.sleep(1)

start=datetime.datetime.now()
tab_dist=[]

debut=datetime.datetime.now()
end=datetime.datetime.now()

velocity=250
'''robot._drive(300,0)
time.sleep(2)
t=robot._sensorstasis()'''

while ((end-debut).seconds<30):
	ser.flushInput()
	robot._drive(250,0)
	time.sleep(0.25)
	t=1
	#t=robot._sensorstasis()
	#print(t)
	while ((end-start).seconds<5) & (t!=0):
		#robot._drive(300,0)	
		time.sleep(0.25)
		t=robot._sensorstasis()
		end=datetime.datetime.now()
		print t
	if (t==0):
		end=datetime.datetime.now()
		times=float((end-start).total_seconds())
		distance=velocity*times
		tab_dist.append(distance)
		robot._stop()
		robot._drive(-100,0)
		time.sleep(0.5)
		robot._stop()
		time.sleep(2)
		robot._turn(90)
		time.sleep(0.346)
		start=datetime.datetime.now()
		end=datetime.datetime.now()
		t=1
		#robot._drive(15,0)
	else:
		times=float((end-start).total_seconds())
		distance=times*velocity
		tab_dist.append(distance)
		robot._stop()
		time.sleep(4)
		start=datetime.datetime.now()
		end=datetime.datetime.now()
		t=1
		#robot._drive(15,0)

print ('tab_dist = ' + str(tab_time))
robot._stop()
robot._safe()

app=tk.Tk()
cv = turtle.ScrolledCanvas(app)
cv.pack()
screen=turtle.TurtleScreen(cv)
screen.screensize(1500,1500)
lam= turtle.RawTurtle(screen)


def dessin(tab_dist):
	ltab=len(tab_dist)
	for i in range(0,ltab-1):
		lam.forward(tab_dist[i])
		if tab_time[i]<1250:
			lam.right(60)
	turtle.mainloop()

dessin(tab_time)


