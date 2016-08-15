from datetime import datetime
import serial
import time
import sys
import testclass

def getSignedNumber(number, bitLength):
                mask = pow(2,bitLength) - 1
                if number & (1 << (bitLength - 1)):
                        return number | ~mask
                else:
                        return number & mask

def bytes2val(highbyte, lowbyte):
                number = (highbyte<<8)+lowbyte
                return getSignedNumber(number,16)

def hex(value):
        """ returns two bytes (ints) in high, low order
        whose bits form the input value when interpreted in
        two's complement
        """
        # if positive or zero, it's OK
        if value >= 0:
            eqBitVal = value
            # if it's negative, I think it is this
        else:
            eqBitVal = (1<<16) + value
	
	high = ((eqBitVal >> 8) & 0xFF)
	low = (eqBitVal & 0xFF)    
        #return (((eqBitVal >> 8) & 0xFF),(eqBitVal & 0xFF)) 
	return high,low
# main
ser = serial.Serial("/dev/ttyAMA0",baudrate = 115200,timeout = 0.1)
ser.flushInput()
robot = testclass.Roomba()
robot._start()
robot._safe()
#robot.drive(500,0)
#robot.stop()
#time.sleep(3)
robot.turn(90)
time.sleep(0.26)
#robot.drive(400,0)
#time.sleep(3)
robot.stop()
time.sleep(2)
robot._safe()
'''debut=datetime.now()
fin=datetime.now()'''


'''for i in range(1,100):
		time.sleep(0.1)
		t=robot._sensorstasis()
		if (t==0):
			#time.sleep(0.5)
			#robot._dataCalc()
			print 'sensor OK' '''
'''tab_dist=[]
tab_ang=[]
dis
t,ang=robot._sensors()
tab_dist.append(dist)
tab_ang.append(ang)

while ((fin-debut).seconds<10):
	for i in range(1,20):
		time.sleep(0.4)
		t=robot._sensorstasis()
		if (t==0):
			#time.sleep(0.7)
			dist,ang=robot._sensors()
                        tab_dist.append(dist)
                        tab_ang.append(ang)
		fin=datetime.now()

if ((fin-debut).seconds>10):
	time.sleep(1)
	dist,ang=robot._sensors()
        tab_dist.append(dist)
        tab_ang.append(ang)
        robot._safe()
print ('tabdist = ' + str(tab_dist))
print ('tabangle = ' +str(tab_ang))

		
time.sleep(1)
robot._safe()'''
