import create
import time


robot=create.Create()
robot.start()
robot.clean()
time.sleep(1)
print ('getting data')
#print (robot.sensorDataIsOK())
#robot.getDist()
#robot.getAngle()
for i in range(1,50):
	robot.getDist()
	robot.getAngle()
	#robot.getCharg()
	time.sleep(2)
robot.safe()
