import json 
import sys
import Tkinter as tk
import numpy as np
import turtle

app = tk.Tk()
cv = turtle.ScrolledCanvas(app)
cv.pack()
screen=turtle.TurtleScreen(cv)
screen.screensize(1500,1500)
lam= turtle.RawTurtle(screen)


def pars(): 
	inputFile = open('data.json')
	data = json.load(inputFile)
	tab_dist =[]

	i = int(input ( 'choose the number you want '))
	if i < 0 or i >= len(data["experiments"]):
    		print ("Not a valid choice")
    		sys.exit(1)

	arrayToRead = data["experiments"][i]["readings"]

	for k in range (0, len(arrayToRead)):
    		time = 0
    		if k == 0:
     		   	time = data["experiments"][i]["readings"][k]["timestamp"]
    		else:
        		prev = data["experiments"][i]["readings"][k-1]["timestamp"]
        		current = data["experiments"][i]["readings"][k]["timestamp"]
        		time = current - prev

	#print ('timestamp = ' + str(time))
		dist = time*250
	#print ('distance = ' + str(dist))
		tab_dist.append(dist)
	#angle = data["experiments"][i]["readings"][k]["direction"]
	#print 'angle = ',(angle)
	print tab_dist
	return tab_dist



def dessin(tab_dist):
        ltab=len(tab_dist)
        '''for i in range (0, ltab-1):
                tab_dist.append(velocity*tab_time[i])
        print tab_dist'''

        for i in range(0,ltab):
                #if tab_time[i]==5:
                lam.forward(tab_dist[i]/10)
                if tab_dist[i]<1250:
                        lam.right(60)

        turtle.mainloop()


tab = pars()
dessin(tab)
