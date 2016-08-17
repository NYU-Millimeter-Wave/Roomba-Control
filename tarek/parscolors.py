import json 
import sys
import Tkinter as tk
import numpy as np
import turtle
import base64 

app = tk.Tk()
cv = turtle.ScrolledCanvas(app)
cv.pack()
screen=turtle.TurtleScreen(cv)
screen.screensize(1500,1500)
lam= turtle.RawTurtle(screen)
Light1Detected="red"
Light2Detected="yellow"
Light3Detected="purple"


def pars(): 
	inputFile = open('data.json')
	data = json.load(inputFile)
	tab_dist =[]
	
	i = int(input ( 'choose the number you want '))
	if i < 0 or i >= len(data["experiments"]):
    		print ("Not a valid choice")
    		sys.exit(1)

	arrayToRead = data["experiments"][i]["readings"]
	lights =[]
	for j in range(3):
		lights.append([0]*len(arrayToRead))	

	for k in range (0, len(arrayToRead)):
    		time = 0
    		if k == 0:
     		   	time = data["experiments"][i]["readings"][k]["timestamp"]
		
    		else:
        		prev = data["experiments"][i]["readings"][k-1]["timestamp"]
        		current = data["experiments"][i]["readings"][k]["timestamp"]
        		time = current - prev
		lights[0][k] = data["experiments"][i]["readings"][k]["Light1Detected"]
		lights[1][k] = data["experiments"][i]["readings"][k]["Light2Detected"]
		lights[2][k] = data["experiments"][i]["readings"][k]["Light3Detected"]

	#print ('timestamp = ' + str(time))
		dist = time*250
	#print ('distance = ' + str(dist))
		tab_dist.append(dist)
	#angle = data["experiments"][i]["readings"][k]["direction"]
	#print 'angle = ',(angle)
	print tab_dist
	print lights
	return tab_dist,lights



def dessin(tab_dist,lights):
        ltab=len(tab_dist)
        '''for i in range (0, ltab-1):
                tab_dist.append(velocity*tab_time[i])
        print tab_dist'''

        for i in range(0,ltab):
                #if tab_time[i]==5:
                lam.forward(tab_dist[i]/5)
                if tab_dist[i]<1250:
                        lam.right(60)
		if ((lights[0][i] > lights[1][i]) and (lights[0][i]>lights[2][i])):
			#lam.color("black",Light1Detected)
			#lam.begin_fill()
			lam.dot(lights[0][i]*35,Light1Detected)
			#lam.end_fill()
			if lights[1][i]>lights[2][i]:
				lam.dot(lights[1][i]*35,Light2Detected)
				lam.dot(lights[2][i]*35,Light3Detected)
			else: 
				lam.dot(lights[2][i]*35,Light3Detected)
				lam.dot(lights[1][i]*35,Light2Detected)
		
	
		elif (lights[1][i] > lights[0][i]) and (lights[1][i]>lights[2][i]):
			lam.dot(lights[1][i]*35,Light2Detected)
			if lights[0][i]>lights[2][i]:
				lam.dot(lights[0][i]*35,Light1Detected)
				lam.dot(lights[2][i]*35,Light3Detected)
			else: 
				lam.dot(lights[2][i]*35,Light3Detected)
				lam.dot(lights[0][i]*35,Light1Detected)


		else:
			lam.dot(lights[2][i]*35,Light3Detected)
			if lights[0][i]>lights[1][i]:
				lam.dot(lights[0][i]*35,Light1Detected)
				lam.dot(lights[1][i]*35,Light2Detected)
			else: 
				lam.dot(lights[1][i]*35,Light2Detected)
				lam.dot(lights[0][i]*35,Light1Detected)



        #turtle.mainloop()
	ts = turtle.getscreen()
	ts.getcanvas().postscript(file="dessin.eps")

func convertEPS(epsFilePath):
    os.system("convert " + str(epsFilePath) + " output.png")
    return base64.b64encode(open("output.png", "rb").read())
    

dist,coul = pars()
dessin(dist,coul)
