# Used for linking rooms to potential rooms
class RandID:
    def __init__(self, randNumber=0):
        self.randID = randNumber

class RoomClass:
    ## Constructs a Room with a room_type.
    #
    def __init__(self, room_type, probability=1.0, randID = RandID(0)):
        self._room_type = room_type
        self._probability = probability
        self.id = randID

    ## Gets the room's type
    #  Returns the room type as a string.
    #
    def getType(self):
        return self._room_type

    ## Changes the room's probability
    #  newProb is a float
    #
    def setProbability(self, newProb):
        self._probability = newProb

    ## Gets the room's probability
    #  Returns the probability as a float.
    #
    def getProbability(self):
        return self._probability


class World:
    ## Constructs a World, optional with filetype
    def __init__(self, file=None):
        # Initialize a 4x4 grid of empty arrays
        self.world = [[[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []],
                      [[], [], [], []]]

        # If a file is provided, populate the world based on file contents
        if file is not None:
            with open(file, "r") as file1:
                for line in file1:
                    line = line.split()
                    y = int(line[2]) - 1  # row, adjust for indexing
                    x = int(line[1]) - 1  # column

                    if line[0] == 'wumpus':
                        self.world[y][x].append(RoomClass('w'))
                    elif line[0] == 'pit':
                        self.world[y][x].append(RoomClass('p'))
                    elif line[0] == 'gold':
                        self.world[y][x].append(RoomClass('g'))

            # Add smells and breezes based on wumpus or pit presence
            self.update_environment()
    
    #Helper class of init
    def update_environment(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                if len(self.world[i][j]) == 0:
                    continue
                else:
                    if self.world[i][j][0].getType() == 'w':
                        self.add_neighbor(i, j, RoomClass('s'))
                    elif self.world[i][j][0].getType() == 'p':
                        self.add_neighbor(i, j, RoomClass('b'))

    #Adds new objects to world
    def add_env(self, x, y, object):
        self.world[y][x].append(object)

    # Adds objects around a point
    def add_neighbor(self, i, j, room_class):
        # Check boundaries to avoid IndexError
        if i > 0:
            self.world[i-1][j].append(room_class)  # Up
        if i < len(self.world) - 1:
            self.world[i+1][j].append(room_class)  # Down
        if j > 0:
            self.world[i][j-1].append(room_class)  # Left
        if j < len(self.world[i]) - 1:
            self.world[i][j+1].append(room_class)  # Right

    # Checks objects around a point
    def wumpus_pit_validity_check(self, i, j, room_class):
        validPlace = True
        # Check boundaries to avoid IndexError
        if i > 0:
            if len(self.world[i-1][j]) == 0:
                validPlace += 1
            for room in self.world[i-1][j]:  # Down
                if(room.getType() == 'v' or room.getType() == 'a'):
                    for room2 in self.world[i-1][j]:
                        if(room2.getType() == room_class):
                            validPlace = True
        
        if i < len(self.world) - 1:
            if len(self.world[i+1][j]) == 0:
                validPlace += 1
            for room in self.world[i+1][j]:  # Up
                if(room.getType() == 'v' or room.getType() == 'a'):
                    for room2 in self.world[i+1][j]:
                        if(room2.getType() == room_class):
                            validPlace += 1

        if j > 0:
            if len(self.world[i][j-1]) == 0:
                validPlace += 1
            for room in self.world[i][j-1]:  # Left
                if(room.getType() == 'v' or room.getType() == 'a'):
                    for room2 in self.world[i][j-1]:
                        if(room2.getType() == room_class):
                            validPlace += 1

        if j < len(self.world[i]) - 1:
            if len(self.world[i][j+1]) == 0:
                validPlace += 1
            for room in self.world[i][j+1]:  # Right
                if(room.getType() == 'v' or room.getType() == 'a'):
                    for room2 in self.world[i][j+1]:
                        if(room2.getType() == room_class):
                            validPlace += 1
        
        return validPlace >= 4

    
    ## Return world array
    def getWorld(self):return self.world

    # Returns a string of the world to print 
    def stringworld(self):
        line = ''
        line += ' ____________________________'
        line += '\n'
        for row in reversed(self.world): #Orients the array up
            for cell in row:
                block = ' | '
                remainingBlockSize = 4
                for k in cell:
                    remainingBlockSize -= 1
                    block+=k.getType()
                for x in range(remainingBlockSize):
                    block += ' '
                line += block
            line+='|\n'
        line += ' ----------------------------'
        return line