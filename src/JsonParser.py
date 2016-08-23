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
	i=sys.argv[1]
	inputFile = open('data.json')
	data = json.load(inputFile)
	tab_dist =[]

	arrayToRead = data["experiments"][i]["readings"]
	lights =[]
	bumps=[]
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
			dist = time*250
			tab_dist.append(dist)
			lights[0][k] = data["experiments"][i]["readings"][k]["Light1Detected"]
			lights[1][k] = data["experiments"][i]["readings"][k]["Light2Detected"]
			lights[2][k] = data["experiments"][i]["readings"][k]["Light3Detected"]
			bumps.append(data["experiments"][i]["readings"][k]["bump"])
				
	print tab_dist
	print lights
	print bumps
	return tab_dist,lights,bumps



def dessin(tab_dist,lights,bumps):
        ltab=len(tab_dist)
        '''for i in range (0, ltab-1):
                tab_dist.append(velocity*tab_time[i])
        print tab_dist'''

        for i in range(0,ltab):
                lam.forward(tab_dist[i]/5)
                if (bumps[i]==1):
					lam.right(45)
				elif (bumps[i]==2):
					lam.left(45)
					
		if ((lights[0][i] > lights[1][i]) and (lights[0][i]>lights[2][i])):
			lam.dot(lights[0][i]*35,Light1Detected)
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
    

dist,coul,bumps = pars()
dessin(dist,coul,bumps)
