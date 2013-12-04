# P3.py
# Author: Paul Talaga
# 
# This file demonstrates how to implement various kinds of Roomba robot agents
# and run them in GUI or non-gui mode using the roomba_sim library.
#

from roomba_sim import *
from roomba_concurrent import *

import random
import math
try:
  import Queue
except ImportError:
  import queue as Queue

# Each robot below should be a subclass of ContinuousRobot, RealisticRobot, or DiscreteRobot.
# All robots need to implement the runRobot(self) member function, as this is where
# you will define that specific robot's characteristics.

# All robots perceive their environment through self.percepts (a class variable) and 
# act on it through self.action.  The specific percepts received and actions allowed
# are specific to the superclass.  See roomba_sim for details.

# TunedRobot - Robot that acceps a chromosome parameter and can store limited state
#               (a single number).  Continuous and dynamic environment.
      
class simBot(RealisticRobot):
  """ The ReflexRobotState robot is similar to the ReflexRobot, but some
    state is allowed in the form of a number.
  """
  
  def __init__(self, room, speed, start_location = -1, chromosome = None):
    super(simBot, self).__init__(room,speed, start_location)
    # Set initial state here you may only store a single number.
    self.state = 0
    # Save chromosome value
    self.degrees = chromosome
      
    
  def runRobot(self):
    (bstate, dirt) = self.percepts
    if(bstate == 'Bump'):
      self.action = ('TurnRight', self.degrees)
    elif(dirt == 'Dirty'):
      self.action = ('Suck', None)
    else:
      self.action = ('Forward', None)


class TunedRobot(RealisticRobot):
  """ The ReflexRobotState robot is similar to the ReflexRobot, but some
    state is allowed in the form of a number.
  """
  
  def __init__(self, room, speed, start_location = -1, chromosome = None):
    super(TunedRobot, self).__init__(room, speed, start_location)
    # Set initial state here you may only store a single number.
    self.state = 0
    # Save chromosome value
    thing = getChromosome(room, start_location, .95)
    self.degrees = thing
      
    
  def runRobot(self):
    (bstate, dirt) = self.percepts
    if(bstate == 'Bump'):
      self.action = ('TurnRight', self.degrees)
    elif(dirt == 'Dirty'):
      self.action = ('Suck', None)
    else:
      self.action = ('Forward', None)

def getChromosome(rooms, start_location, min_clean):
    population = range(50, 350, 10)
    metric = {}
    use = 0
    while len(population) > 1:
        population = runTests(population, start_location, min_clean)

    print("Using: %d" % population[0])
    return population[0]

def runTests(population, start_location, min_clean):
    least = 999999
    fitnessQueue = Queue.PriorityQueue()
    print("Fitness testing")
    print(population)
    for x in population:
        print("Testing angle: %d" % x)
        temp = concurrent_test(robot = simBot,
                               rooms = allRooms[0:2],
                               num_trials = 1,
                               start_location = start_location,
                               min_clean = .6,
                               chromosome = x,
                               timeout = 15)
        #temp is the performance, x is the angle must group the two so that cullPop can cull the worst
        #performing angles.
        fitnessQueue.put((temp,x))
        #if temp < least:
        #    least = temp
        #    use = x
    print("Queue size: %d" % fitnessQueue.qsize())
    #return cullPop(population), use
    return cullPop(fitnessQueue)
        
def cullPop(fitnessQueue):
    #size = len(fitnessQueue)
    size = fitnessQueue.qsize()
    end = int(math.ceil(0.30 * size))#euthenasia
    top = int(math.ceil(0.10 * size))#proletariat
    print("Size: %f and end: %f" % (size, end))
    newPop = []
    toBreed = []
    for x in range(0, size - end):
        if x < top:
            newPop.append(fitnessQueue.get()[1])
        else:
            toBreed.append(fitnessQueue.get()[1])
    newPop.extend(breed(toBreed))
    return newPop

def breed(pop):
    print("Breeding")
    print(pop)
    newPop = []
    x = 0
    while x < len(pop):
        if x + 1 < len(pop):
            newPop.append((pop[x] + pop[x + 1]) / 2)
        else:
            newPop.append(pop[x])
        x += 2
    return newPop

def mutate(val):
    return val
############################################
## A few room configurations

allRooms = []

smallEmptyRoom = RectangularRoom(10,10)
allRooms.append(smallEmptyRoom)  # [0]

largeEmptyRoom = RectangularRoom(10,10)
allRooms.append(largeEmptyRoom) # [1]

mediumWalls1Room = RectangularRoom(30,30)
mediumWalls1Room.setWall((5,5), (25,25))
allRooms.append(mediumWalls1Room) # [2]

mediumWalls2Room = RectangularRoom(30,30)
mediumWalls2Room.setWall((5,25), (25,25))
mediumWalls2Room.setWall((5,5), (25,5))
allRooms.append(mediumWalls2Room) # [3]

mediumWalls3Room = RectangularRoom(30,30)
mediumWalls3Room.setWall((5,5), (25,25))
mediumWalls3Room.setWall((5,15), (15,25))
mediumWalls3Room.setWall((15,5), (25,15))
allRooms.append(mediumWalls3Room) # [4]

mediumWalls4Room = RectangularRoom(30,30)
mediumWalls4Room.setWall((7,5), (26,5))
mediumWalls4Room.setWall((26,5), (26,25))
mediumWalls4Room.setWall((26,25), (7,25))
allRooms.append(mediumWalls4Room) # [5]

mediumWalls5Room = RectangularRoom(30,30)
mediumWalls5Room.setWall((7,5), (26,5))
mediumWalls5Room.setWall((26,5), (26,25))
mediumWalls5Room.setWall((26,25), (7,25))
mediumWalls5Room.setWall((7,5), (7,22))
allRooms.append(mediumWalls5Room) # [6]

#############################################    
def TunedTest(num):
  print("Robot Results:")
  print(runSimulation(num_robots = 1,
                      min_clean = 0.95,
                      num_trials = 1,
                      room = allRooms[num],
                      robot_type = TunedRobot,
                      chromosome = 0))
                    
def runDefault(num):
    print("Default robot result:")
    print(runSimulation(num_robots = 1,
                        min_clean = 0.95,
                        num_trials = 1,
                        room = allRooms[num],
                        robot_type = simBot,
                        chromosome = 135))

if __name__ == "__main__":
  # This code will be run if this file is called on its own
  random.seed(None)
  num = random.randrange(0, 6, 1)
  TunedTest(num)
  runDefault(num)
  print("Testing: %d" % num)
  
  # This is an example of how we will test your program.  Our rooms will not be those listed above, but similar.
  #rooms = [allRooms[1], allRooms[5]]
  #startLoc = (5,5)
  #minClean = 0.2
  #chromosome = getChromosome(rooms, startLoc, minClean)
  
  # Concurrent test execution.
  #print(concurrent_test(TunedRobot, rooms, num_trials = 20, min_clean = minClean, chromosome = chromosome))


