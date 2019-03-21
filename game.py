import random
import math

#particle effects
def particlemaker(xpos, ypos, xmom, ymom):
    # particle settings
    particle_lifespan = 45
    random_factor = 30 # higher number = less random
    max_particles = 6
    max_deviation = 2
    printerlist_add = []
    for i in range(random.randint(max_particles - max_deviation, max_particles)):
        printerlist_add += [xpos, ypos, xmom + ((random.randint(-20, 20))/random_factor), ymom +
                            ((random.randint(-20, 20))/random_factor), 4, "NA", "NA", particle_lifespan]  
    return printerlist_add

#physics handling
def doPhysics(object_list, width, height, max_speed, drag, step_drag):
    for i in range(0, len(object_list), 8):
        #decaying objects
        if object_list[4 + i] in [2, 8, 5, 4]: #stuff in list should have a decrement to their life force
            object_list[7 + i] -= 1
            
        # edges section
        if object_list[i] > width:
            object_list[i] -= width
        if  object_list[i] < 0:
            object_list[i] += width
        if object_list[1 + i] > height:
            object_list[1 + i] -= height
        if object_list[1 + i] < 0:
            object_list[1 + i] += height

        # positioner
        object_list[i] += object_list[2 + i]
        object_list[1 + i] -= object_list[3 + i]

        #drag
        if object_list[4 +i] in drag:
            stepper = abs(object_list[2 +i]) + abs(object_list[3 +i])
            if stepper == 0:
                stepper = 1
            step_drag_x = abs(object_list[2 +i]) / stepper * step_drag
            step_drag_y = abs(object_list[3 +i]) / stepper * step_drag   
            if object_list[2 +i] > 0 and object_list[2 +i] > step_drag_x:
                object_list[2 +i] -= step_drag_x
            elif step_drag_x > object_list[2 +i] > 0:
                object_list[2 +i] = 0
            if object_list[2 +i] < 0 and object_list[2 +i] < step_drag_x:
                object_list[2 +i] += step_drag_x
            elif step_drag_x < object_list[2 +i] < 0:
                object_list[2 +i] = 0     
            if object_list[3 +i] > 0 and object_list[3 +i] > step_drag_y:
                object_list[3 +i] -= step_drag_y
            elif step_drag_y > object_list[3 +i] > 0:
                object_list[3 +i] = 0   
            if object_list[3 +i] < 0 and object_list[3 +i] < step_drag_y:
                object_list[3 +i] += step_drag_y
            elif step_drag_y < object_list[3 +i] < 0:
                object_list[3 +i] = 0

        #speed limit for ship
        if object_list[4+i] == 1 or object_list[4+i] == 5:
            if object_list[2 + i] > max_speed:
                object_list[2 + i] = max_speed
            if object_list[2 + i] < -1 * max_speed:
                object_list[2 + i] =  -1 * max_speed
            if object_list[3 + i] > max_speed:
                object_list[3 + i] = max_speed
            if object_list[3 + i] < -1 * max_speed:
                object_list[3 + i] = -1 * max_speed
        
        #rotation
        if not isinstance(object_list[5+i], str):
            object_list[5+i] += object_list[6+i]/7 #the divided by moderates the speed of rotation
            if object_list[5+i] >= 360:
                object_list[5+i] -= 360
            if object_list[5+i] <= -360:
                object_list[5+i] += 360                

#helps out by setting entities to reasonable speeds
def asteroidspeedmaker(max_asteroid_spd):
    asteroid_speedset = []
    # if else statements institute a minimum horizontal and vertical speed (separately) of half the asteroid high speed
    if random.randint(0,1) == 1:
        asteroid_speedset.append(random.randint(int(max_asteroid_spd/2), max_asteroid_spd)/100)
    else:
        asteroid_speedset.append(random.randint(-1*max_asteroid_spd, int(-1*max_asteroid_spd/2))/100)
    if random.randint(0,1) == 1:
        asteroid_speedset.append(random.randint(int(max_asteroid_spd/2), max_asteroid_spd)/100)
    else:
        asteroid_speedset.append(random.randint(-1*max_asteroid_spd, int(-1*max_asteroid_spd/2))/100)
    return asteroid_speedset

#generates the stars for backgrounds
def generateStars(width, height):
    stars_list = []
    for i in range(20):
        stars_list += [random.randint(0,width), random.randint(0,height), 0, 0, 100, "NA", "NA", 1]
    return stars_list

#leveler
def leveler(object_list, max_asteroids, max_asteroid_spd, width, height, d_sats, d_parts, d_asteroids):
    ASTEROID = 30
    SATS = 50
    PARTS = 20
    object_list = object_list[:8]
    object_list += generateStars(width, height)
    countervar = 0
    while countervar < random.randint(max_asteroids - 2, max_asteroids):
        idChooser = random.randint(0, 100)
        if idChooser < ASTEROID:
            idSelection = d_asteroids
        elif idChooser < ASTEROID + SATS:
            idSelection = d_sats
        else:
            idSelection = d_parts
        asteroid_speedset = asteroidspeedmaker(max_asteroid_spd)                    
        object_list_add = [random.randint(0, width), random.randint(0, height), asteroid_speedset[0],
                           asteroid_speedset[1]]
        object_list_add += [idSelection[random.randint(0, len(idSelection)-1)], random.randint(0,360),
                            random.randint(-10,10), 1] 
        xdiff = object_list[0] - object_list_add[0]
        ydiff = object_list[1] - object_list_add[1]
        distance = ((xdiff ** 2) + (ydiff ** 2)) ** 0.5
        countervar += 1
        object_list += object_list_add
    return object_list

#deaderizer -- perhaps amalgamated into doPhysics in the future, just outside its main for loop
def deaderizer(object_list):
    indexadj = 0
    while indexadj < len(object_list): 
        if object_list[7 + indexadj] <= 0:
            if object_list[4+indexadj] == 5:
                object_list[7+indexadj] = 1
                object_list[4+indexadj] = 1
            else:
                del object_list[indexadj:8+indexadj]
        indexadj += 8
    return object_list

sectorDestData = {1: [2, 5, 3, -1], 2: [-1, 4, 1, -1], 3: [1, -1, -1, -1], 4: [-1, -1, 5, 2], 5: [4, 6, -1, 1],
                  6: [8, -1, 7, 5], 7: [6, 9, -1, -1], 8: [12, 10, 6, -1], 9: [10, 14, -1, 7], 10: [-1, 11, 9, 8],
                  11: [13, 16, 17, 10], 12: [-1, 13, 8, -1], 13: [-1, -1, 11, 12], 14: [-1, 15, -1, 9], 15: [16, -1, -1, 14],
                  16: [-1, 18, 15, 11], 17: [11, -1, -1, -1], 18: [-1, -1, 19, 16], 19: [18, -1, -1, -1]}

def sectorDestinations(sectornum):
    #[left, up, right, down]
    if sectornum in sectorDestData:
        return sectorDestData[sectornum]
    else:
        return [1, 1, 1, 1] #in case you go into a sector that doesn't exist, it will redirect you to the home sector

#returns true if an infinite level that always regenerates
#else returns false to signal a level that doesn't get regenerated
def sectorGeneration(sectornum):
    output = False
    infinite_sectors = [4, 12, 14]
    if sectornum in infinite_sectors:
        output = True
    return output

def solarPanelDrops():
    drops = [0, 0, 0, 0]
    if random.randint(1,100) <= 80:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[0] += 1
        elif 61 <= percentHelper <= 90:
            drops[0] += 2
        else:
            drops[0] += 3
    if random.randint(1,100) <= 20:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[2] += 1
        elif 61 <= percentHelper <= 90:
            drops[2] += 2
        else:
            drops[2] += 3
    if random.randint(1,100) <= 10:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[3] += 2
        elif 61 <= percentHelper <= 90:
            drops[3] += 4
        else:
            drops[3] += 6
    return drops

def satelliteDrops():
    drops = [0, 0, 0, 0]
    if random.randint(1,100) <= 80:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[0] += 1
        elif 61 <= percentHelper <= 90:
            drops[0] += 2
        else:
            drops[0] += 3
    if random.randint(1,100) <= 40:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[1] += 1
        elif 61 <= percentHelper <= 90:
            drops[1] += 2
        else:
            drops[1] += 3
    if random.randint(1,100) <= 20:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[2] += 1
        elif 61 <= percentHelper <= 90:
            drops[2] += 2
        else:
            drops[2] += 3
    if random.randint(1,100) <= 70:
        percentHelper = random.randint(1,100)
        if percentHelper <= 60:
            drops[3] += 5
        elif 61 <= percentHelper <= 90:
            drops[3] += 10
        else:
            drops[3] += 20
    return drops

def makeAsteroidList(scalar2): #generates a list of offsets for all of the separate asteroid designs
    asteroidlist = [[[17, 1], [12, 8], [-2, 17], [-8, 11], [-16, 3], [-14, -7], [-4, -17], [10, -10]],
                    [[16, -3], [12, 10], [-2, 17], [-10, 14], [-19, -2], [-8, -13], [2, -16], [8, -12]],
                    [[16, 3], [7, 13], [-8, 14], [-18, 4], [-11, -11], [-3, -16], [11, -9]],
                    [[18, 0], [10, -10], [0, -17], [-13, -12], [-20, 0], [-11, 11], [0, 13], [14, 12]],
                    "4", "5", "6", "7", "8", "9",
                    [[26, -3], [20, 10], [4, 21], [-8, 9], [-8, 10], [-18, 14], [-26, 10], [-25, -1], [-9, -18], [10, -12], [19, -16]],
                    [[24, 2], [11, 9], [4, 24], [-9, 19], [-22, 5], [-13, -20], [3, -24], [18, -13]],
                    [[23, -1], [16, 19], [-4, 26], [-13, 13], [-26, 3], [-17, -20], [-4, -23], [16, -14]],
                    [[27, 0], [15, -15], [0, -25], [-21, -15], [-22, 0], [-19, 15], [0, 24], [21, 17]],
                    "14", "15", "16", "17", "18", "19",
                    [[33, -4], [27, 23], [-6, 30], [-18, 24], [-32, 5], [-25, -18], [6, -30], [20, -22]],
                    [[20, 0], [24, 24], [-8, 32], [-23, 18], [-33, 5], [-26, -28], [3, -33], [27, -22]],
                    [[30, 0], [26, -22], [3, -33], [-22, -22], [-38, 0], [-27, 22], [3, 34], [30, 23]],
                    [[39, 0], [29, -22], [0, -35], [-28, -20], [-37, 0], [-24, 23], [0, 35], [19, 22]],
                    "24", "25", "26", "27", "28", "29"]
    for i in range(len(asteroidlist)):
        if not isinstance(asteroidlist[i], str):
            for j in range(len(asteroidlist[i])):
                asteroidlist[i][j][0] *= scalar2
                asteroidlist[i][j][1] *= scalar2       
    return asteroidlist

def RotatePoint(xpos, ypos, point, rotation):
    point[1] -= ypos
    point[0] -= xpos
    revisedPoint = []
    if point[0] or point[1]:
        if point[1] > 0 and point[0] == 0:
            currentPosition = 90
        elif point[1] < 0 and point[0] == 0:
            currentPosition = 270
        elif point[0] > 0:
            currentPosition = math.degrees(math.atan(point[1]/point[0]))
        elif point[0] <= 0:
            currentPosition = math.degrees(math.atan(point[1]/point[0])) + 180
        realPosition = currentPosition + rotation
        distance = (abs(point[0])**2 + abs(point[1])**2)**0.5
        xPoint = math.cos(math.radians(realPosition)) * distance + xpos
        yPoint = math.sin(math.radians(realPosition)) * distance + ypos
        revisedPoint.append([xPoint, yPoint])
    else:
        #if the point being rotated around is in the list
        point[1] += ypos
        point[0] += xpos
        revisedPoint.append([point[0], point[1]])
    return revisedPoint

def Rotate(xpos, ypos, points, rotationPosition):
    revisedPoints = []
    for i in range(len(points)):
        revisedPoints += RotatePoint(xpos, ypos, points[i], rotationPosition)
    return revisedPoints

def dock(xpos, ypos, image):
    width = image.get_size()[0]
    height = image.get_size()[1]
    newXpos = xpos+(width/2)+10
    newYpos = ypos+height+10
    rotation = 180
    xmom = 0
    ymom = -0.5
    return (newXpos, newYpos, xmom, ymom, rotation)
      
class Asteroid():
    asteroidlist = "not yet a thing"
    scalar2 = -1
    def __init__ (self, scalar2):
        Asteroid.asteroidlist = makeAsteroidList(scalar2)
        Asteroid.scalar2 = scalar2

    def getPoints(xpos, ypos, objectID):
        offsetList = Asteroid.asteroidlist[objectID-70][:]
        pointList = []
        for i in range(len(offsetList)):
            pointList.append([xpos + offsetList[i][0], ypos + offsetList[i][1]])
        return pointList

    def getHitbox(xpos, ypos, objectID): # in rect format
        if 69 < objectID < 80:
            hitrange = 15
        if 79 < objectID < 90:
            hitrange = 20
        if 89 < objectID < 100:
            hitrange = 25
        return [xpos-hitrange*Asteroid.scalar2, ypos-hitrange*Asteroid.scalar2, hitrange*2*Asteroid.scalar2,
                hitrange*2*Asteroid.scalar2]
        
