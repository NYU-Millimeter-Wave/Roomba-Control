import json 
import sys
 
inputFile = open('data.json')
data = json.load(inputFile)

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

    print ('timestamp = ' + str(time))
    dist = time*500
    print ('distance = ' + str(dist))
    angle = data["experiments"][i]["readings"][k]["direction"]
    print 'angle = ',(angle)
