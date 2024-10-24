from env import *
'''
class WalkerClass:
    ## Constructs a walker with pos 0,0.
    #
    def __init__(self, posx, posy):
        self._Xposition = posx
        self._Yposition = posy
        self._type = 'a'

    ## Changes the walkers position
    #  direction is a list containing two integers. The first is the x and the second is the y.
    #
    def move(self, direction, memory):
        for index, stuff in enumerate(memory[self.getPos()[1]][self.getPos()[0]]):
  
          if stuff.getType() == 'a': 
            memory[self.getPos()[1]][self.getPos()[0]].pop(index)
            if stuff.getType() == 'v': pass
            else:
              memory[self.getPos()[1]][self.getPos()[0]].append(RoomClass('v'))
        self._Xposition = self._Xposition + direction[0]
        self._Yposition = self._Yposition + direction[1]
        memory[self._Xposition][self._Yposition].append(WalkerClass(self._Xposition, self._Yposition))
        pass

    def getType(self):
        return self._type

    #def updateWorld(self, blankWorld):
        #probabilityEngine(blankWorld, walker)

    ## Returns the walkers position
    #  Returnes a list containing two integers. The first is the x and the second is the y.
    #
    def getPos(self):
        return (self._Xposition, self._Yposition)
'''

class Agent:
    
    ## Initialized an agent
    # outside is a world object representing the wumpus world
    def __init__(self, outside):
        self.xpos = 0
        self.ypos = 0
        self.outside = outside
        self.notWon = True
        self.type = 'a'
        self.memory = World()
        self.memory.add_env(self.xpos,self.ypos, self)
    

    ## Individual status functions
    def getType(self): return self.type #return agent
    def win(self): return self.notWon #return alive
    def perish(self):
            self.memory = World()
            self.xpos = 0
            self.ypos = 0
            self.memory.add_env(self.xpos,self.ypos, self)
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nYou Died!")

    
    ##returns string of world, with memory
    def stringmemory(self):
        return self.memory.stringworld()
    
    ## moves the agent in a cardinal direction
    def move(self, direction, realWorld=World()):
        if(direction == 'n'):
            # Deleting agent in room
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'a'):
                    self.memory.world[self.ypos][self.xpos].remove(room)
            # Adds to memory current position and checks for overflow
            if(self.ypos+1 <= len(self.memory.world) - 1):
                self.ypos += 1
            self.memory.add_env(self.xpos,self.ypos, self)
            # Adds visited to previous room if there is none
            dontAdd = False
            for room in self.memory.world[self.ypos - 1][self.xpos]:
                if(room.getType() == 'v'):
                    dontAdd = True
            if(dontAdd != True):
               self.memory.add_env(self.xpos,self.ypos - 1, RoomClass('v'))

        elif(direction == 's'):
            # Remove agent from memory
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'a'):
                    self.memory.world[self.ypos][self.xpos].remove(room)
            # Checks for overload
            if(self.ypos-1 >= 0):
                self.ypos -= 1
            # Adds agent back to memory
            self.memory.add_env(self.xpos,self.ypos, self)
            # Adds visited to previous room
            dontAdd = False
            for room in self.memory.world[self.ypos + 1][self.xpos]:
                if(room.getType() == 'v'):
                    dontAdd = True
            # Adding visited 
            if(dontAdd != True):
               self.memory.add_env(self.xpos,self.ypos + 1, RoomClass('v'))

        elif(direction == 'e'):
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'a'):
                    self.memory.world[self.ypos][self.xpos].remove(room)
            if(self.xpos+1 <= len(self.memory.world) - 1):
                self.xpos += 1
            self.memory.add_env(self.xpos,self.ypos, self)
            dontAdd = False
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'v'):
                    dontAdd = True
            if(dontAdd != True):
               self.memory.add_env(self.xpos-1,self.ypos, RoomClass('v'))

        elif(direction == 'w'):
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'a'):
                    self.memory.world[self.ypos][self.xpos].remove(room)
            if(self.xpos-1 >= 0):
                self.xpos -= 1
            self.memory.add_env(self.xpos,self.ypos, self)
            dontAdd = False
            for room in self.memory.world[self.ypos][self.xpos]:
                if(room.getType() == 'v'):
                    dontAdd = True
            if(dontAdd != True):
               self.memory.add_env(self.xpos+1,self.ypos, RoomClass('v'))
        for room in realWorld.getWorld()[self.ypos][self.xpos]:
            if any(isinstance(x, RoomClass) for x in self.memory.getWorld()[self.ypos][self.xpos]):
                self.memory.add_env(self.xpos, self.ypos, room)#
            if(room.getType() == 'w' or room.getType() == 'p'):
                self.perish()
            if(room.getType() == 'g'):
                self.notWon = False