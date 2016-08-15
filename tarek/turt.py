from __future__ import division

import Tkinter as tk
import numpy as np
import turtle

#wn= turtle.Screen()
#lam= turtle.Turtle()
app = tk.Tk()
cv = turtle.ScrolledCanvas(app)
cv.pack()
screen=turtle.TurtleScreen(cv)
screen.screensize(1500,1500)
lam= turtle.RawTurtle(screen)

tabdist = [-4, -156, 2, 0, -8, -211, 0, -5, -9, -10, -16, -21, 0, -8, -40]
tabangle = [0, 0, 14, 18, 10, -1, 16, -2, -8, -7, -1, 1, 17, 12, -1]
#tabdist = [100,50,50,100]
#tabangle = [0,30,0,-45]


#dessin(tabdist,tabangle)

def dessin(tabdist,tabangle):
        ltab=len(tabdist)
        for i in range (0,ltab):
		#lam.forward(tabdist[i])
                if tabangle[i] >0:
                	temp = (180-tabangle[i])
           		lam.left(temp)
			#lam.left(tabangle[i])
			#lam.left(180-tabangle[i])
		#elif (tabangle[i]=0): 
			
		elif tabangle[i]<0:	
			tempp = (180+tabangle[i])
                        lam.right(tempp)
			#tempp=-1*tabangle[i]
			#lam.right(tempp)

		lam.forward(tabdist[i])

        #turtle.getscreen()._root.mainloop()
	turtle.mainloop()
#tabdist=[32,78,125,94,17,25,0,34]
#tabangle=[41,25,90,-13,65,-8,-42,18]
dessin(tabdist,tabangle)
