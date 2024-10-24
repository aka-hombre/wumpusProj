from agent import Agent
from env import *
import datetime
import random

# Function to log message with timestamp to a file
def log_out(message, file_name='log.txt'):
    with open(file_name, 'a') as file:
        # Get current date and time
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Write message with timestamp
        file.write(f'[{current_time}] {message}\n')


'''
#function will make new txt each time agent moves
def log_out(message):
    # Get current date and time
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # Use the current time in the file name to ensure uniqueness
    file_name = f'log_{current_time}.txt'
    
    # Write message to a new file
    with open(file_name, 'w') as file:
        file.write(f'[{current_time}] {message}\n')
'''
## goes through a world and adds pits to breezes and wumpi to stenches unless it is impossible due to a visisted square confirming a room
def calculateProbability(world=World()):
    for rowNumber, row in enumerate(world.getWorld()):
        for collumNumber, collum in enumerate(row):
            for cellNumber, cell in enumerate(collum):
                if(cell.getType() == 's'):
                    #count valid positions
                    validPositionCount = 0
                    if rowNumber > 0:
                        validPositionCount += 1
                    if rowNumber < len(world.getWorld()) - 1:
                        validPositionCount += 1
                    if collumNumber > 0:
                        validPositionCount += 1
                    if collumNumber < len(world.getWorld()[rowNumber]) - 1:
                        validPositionCount += 1
                    computedProbability = 1 / validPositionCount
                    # Check boundaries to avoid IndexError
                    if rowNumber > 0:
                        notVisited = True
                        for room in world.getWorld()[rowNumber-1][collumNumber]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber-1][collumNumber].append(RoomClass('w', computedProbability))  # Up
                    if rowNumber < len(world.getWorld()) - 1:
                        notVisited = True
                        for room in world.getWorld()[rowNumber+1][collumNumber]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber+1][collumNumber].append(RoomClass('w', computedProbability))  # Down
                    if collumNumber > 0:
                        notVisited = True
                        for room in world.getWorld()[rowNumber][collumNumber-1]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber][collumNumber-1].append(RoomClass('w', computedProbability))  # Left
                    if collumNumber < len(world.getWorld()[rowNumber]) - 1:
                        notVisited = True
                        for room in world.getWorld()[rowNumber][collumNumber+1]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber][collumNumber+1].append(RoomClass('w', computedProbability))  # Right
                if(cell.getType() == 'b'):
                    #count valid positions
                    validPositionCount = 0
                    if rowNumber > 0:
                        validPositionCount += 1
                    if rowNumber < len(world.getWorld()) - 1:
                        validPositionCount += 1
                    if collumNumber > 0:
                        validPositionCount += 1
                    if collumNumber < len(world.getWorld()[rowNumber]) - 1:
                        validPositionCount += 1
                    computedProbability = 1 / validPositionCount
                    # Check boundaries to avoid IndexError
                    if rowNumber > 0:
                        notVisited = True
                        for room in world.getWorld()[rowNumber-1][collumNumber]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber-1][collumNumber].append(RoomClass('p', computedProbability))  # Up
                    
                    if rowNumber < len(world.getWorld()) - 1:
                        notVisited = True
                        for room in world.getWorld()[rowNumber+1][collumNumber]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber+1][collumNumber].append(RoomClass('p', computedProbability))  # Down
                    
                    if collumNumber > 0:
                        notVisited = True
                        for room in world.getWorld()[rowNumber][collumNumber-1]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber][collumNumber-1].append(RoomClass('p', computedProbability))  # Left
                    
                    if collumNumber < len(world.getWorld()[rowNumber]) - 1:
                        notVisited = True
                        for room in world.getWorld()[rowNumber][collumNumber+1]:
                            if(room.getType() == 'v'):
                                notVisited = False
                        if(notVisited):
                            world.getWorld()[rowNumber][collumNumber+1].append(RoomClass('p', computedProbability))  # Right
    # Clean up
    print(world.stringworld())
    for rowNumber, row in enumerate(world.getWorld()):
        for collumNumber, collum in enumerate(row):
            objectsToRemove = []
            for cellNumber, cell in enumerate(collum):
                if(cell.getType() == 'w'):
                    if(world.wumpus_pit_validity_check(rowNumber, collumNumber,'s') != True):
                        objectsToRemove.append(cell)
                elif(cell.getType() == 'p'):
                    print(world.stringworld())
                    if(world.wumpus_pit_validity_check(rowNumber, collumNumber,'b') != True):
                        objectsToRemove.append(cell)
            for objectToRemove in objectsToRemove:
                world.getWorld()[rowNumber][collumNumber].remove(objectToRemove)



def moveAndCalcProb(theAgent, theRealWorld, direction='n', randomNumber=0):
    theAgent.move(direction, theRealWorld)
    calculateProbability(theAgent.memory)
    print(theAgent.stringmemory())
    ostr = ''
    for i in theAgent.memory.world[theAgent.ypos][theAgent.xpos]: ostr+=i.getType()+", "
    print("Agent encountered the following: "+ostr)
    return theAgent.stringmemory()+"\nAgent encountered the following: "+ostr

#file naming for logs:
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
fname = f'log_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt'

#world and moves
realworld = World('testworld.txt')
agent = Agent(realworld)
moveSet = ['n','s','e','w']

randID = RandID(0)
print(realworld.stringworld())


print(agent.stringmemory())

while(agent.win()):
    #log_out(moveAndCalcProb(agent, realworld, input("Enter in n,s,e, or w: ")), fname)
    log_out(moveAndCalcProb(agent, realworld, moveSet[random.randint(0, 3)]), fname)
