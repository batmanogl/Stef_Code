import turtle
import random

## Pythagorean Theorem
def pythagoras_function(pos1 , pos2):
    x1, y1 =  pos1 
    x2, y2 =  pos2
    distance = float(((x2-x1)**2 + (y2-y1)**2)**0.5)
    return distance

print("Give me the two positions with a form of coordinates (x,y)")

pos1 = (float(input("Enter the x1 coordinate for pos1:")) , float(input ("Enter the y1 coordinate for pos1:")))
pos2 = (float(input("Enter the x2 coordinate for pos2:")) , float(input ("Enter the y2 coordinate for pos2:")))

print ("The lenght of hypotenousa is: ", pythagoras_function(pos1, pos2))

#################################################################################

print('''
''')

## Get 2 random food positions and calculate through Pythagorean Theorem the distance between them.  
def food_position1 ():
    global pos1, x1, y1
    x1 = random.uniform(-497,497)
    y1 = random.uniform(-497,497)
    pos1 = x1,y1
    return pos1

def food_position2 ():
    global pos2, x2, y2
    x2 = random.uniform(-497,497)
    y2 = random.uniform(-497,497)
    pos2 = x2,y2
    return pos2

position1=food_position1()
position2=food_position2()

print("The first food position is: " ,position1)
print("The second food position is: " ,position2)

print('''
''')

def pythagoras_function(pos1,pos2):
    x1, y1 =  pos1 
    x2, y2 =  pos2
    distance = float(((x2-x1)**2 + (y2-y1)**2)**0.5)
    return distance


print ("The distance between the two food positions is: ", pythagoras_function(pos1,pos2), "pixels")
##################################################################################
