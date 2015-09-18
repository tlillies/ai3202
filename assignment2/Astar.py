#!/usr/bin/python

import sys

ENDING_NODE_X = 9
ENDING_NODE_Y = 7

class Node():
    def __init__(self,x,y,sqr_type):
        self.sqr_type = sqr_type
        self.x = x
        self.y = y
        self.distanceToStart = None
        self.heuristic = None
        self.f = None
        self.parent = None


# Check to make sure argument count is correct
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print('Incorrect number of arguments: ')
    print(len(sys.argv))
    print(sys.argv)
    exit(0)

world = sys.argv[1]
heuristic = sys.argv[2]

print('World: {0}'.format(world))
print('Heuristic: {0}'.format(heuristic))

# Read in matrix
matrix = []
world_file = open(world,'r')
for line in world_file:
    numbers = line.split(" ")
    nodes = []
    for node in numbers:
        nodes.append(int(node))
    matrix.append(nodes)
    #print(nodes)

# create graph
#print len(matrix)
#print len(matrix[0])
world_max_x = len(matrix[0]) # 10
world_max_y = len(matrix) # 8
world_min_x = 0
world_min_y = 0
world = []
#world = [[0 for y in range(world_max_y)] for x in range(world_max_x)]
for i in range(0,world_max_x):
    line = []
    for j in range(0,world_max_y):
        # print('i:{0},j:{1}'.format(i,j))
        line.insert(0,Node(i,world_max_y-j-1,matrix[j][i]))
    world.append(line)

for y in range(world_max_y-1,-1,-1):
    for x in range(0,world_max_x):
        sys.stdout.write(str(world[x][y].sqr_type))
        sys.stdout.write(" ")
    print(" ")
print(" ")

#for y in range(world_max_y-1,-1,-1):
#   for x in range(0,world_max_x):
#       sys.stdout.write(str(world[x][y].x))
#       sys.stdout.write(",")
#       sys.stdout.write(str(world[x][y].y))
#       sys.stdout.write("-")
#       
#       sys.stdout.write(str(x))
#       sys.stdout.write(",")
#       sys.stdout.write(str(y))
#       sys.stdout.write(" ")
#   print(" ")


Open = []
Closed = []

world[0][0].f = 0
world[0][0].distanceToStart = 0
world[0][0].heuristic = 0

Open.append(world[0][0])

nodes_evaluated = 0

while Open:
    #Look for the lowest F cost square on the open list. We refer to this as the current square.
    fs = []
    for x in range(0,len(Open)):
        fs.append(Open[x].f)
    min_value = min(fs)
    index = fs.index(min_value)
    lowest_cost_node = world[Open[index].x][Open[index].y]
    # Switch it to the closed list.
    Closed.append(lowest_cost_node)
    Open.remove(lowest_cost_node)

    x = lowest_cost_node.x
    y = lowest_cost_node.y

    nodes_evaluated += 1

    if x == ENDING_NODE_X and y == ENDING_NODE_Y:
        print('Reached Ending Node!')
        break

    for new_x in range(x-1,x+2):
        for new_y in range(y-1,y+2):
            try:
                # This is really gross
                if new_x < 0:
                    new_x = 10000
                if new_y < 0:
                    new_y = 10000

                node = world[new_x][new_y]

                #print("X: {0}, Y {1}".format(node.x,node.y))
                cost = 10
                if node.sqr_type == 2 or node in Closed: # Mountains
                    pass
                else:
                    if new_x != 0 and new_y != 0:
                        cost += 4
                    if node.sqr_type == 1:
                        cost += 10
                    h = 0
                    if heuristic == 'man':
                        h = (ENDING_NODE_X - node.x) + (ENDING_NODE_Y - node.y)
                    if heuristic == 'tom':
                        h = 5*((ENDING_NODE_X - node.x) + (ENDING_NODE_Y - node.y))
                    distanceToStart = cost + lowest_cost_node.distanceToStart
                    f = h + distanceToStart
                    parent = lowest_cost_node
                    #print("X: {0}, Y {1}".format(node.x,node.y))
                    if node in Open:
                        if node.f > f:
                            node.heuristic = h
                            node.distanceToStart = distanceToStart
                            node.f = f
                            node.parent = parent
                    else:
                        #print("X: {0}, Y {1}".format(node.x,node.y))
                        node.distanceToStart = distanceToStart
                        node.f = f
                        node.heuristic = h
                        node.parent = parent
                        Open.append(node)
            except:
                pass

node = lowest_cost_node
world[node.x][node.y].sqr_type = "-"
while node.x != 0 or node.y != 0:
    node = node.parent
    world[node.x][node.y].sqr_type = "-"
    #print('X:{0},Y:{1}'.format(node.x,node.y))

for y in range(world_max_y-1,-1,-1):
    for x in range(0,world_max_x):
        sys.stdout.write(str(world[x][y].sqr_type))
        sys.stdout.write(" ")
    print(" ")
print(" ")

print("Cost: {0}".format(lowest_cost_node.f))
print("Nodes Evaluated: {0}".format(nodes_evaluated))
