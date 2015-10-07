#!/usr/bin/python

import sys
import operator

ENDING_NODE_X = 9
ENDING_NODE_Y = 7

class Node():
    def __init__(self,x,y,sqr_type):
        self.sqr_type = sqr_type
        if sqr_type == 1:
            self.sqr_value = -1.0
        elif sqr_type == 2:
            self.sqr_value = 0
        elif sqr_type == 3:
            self.sqr_value = -2.0
        elif sqr_type == 4:
            self.sqr_value = 1.0
        else:
            self.sqr_value = sqr_type
        self.x = x
        self.y = y
        self.utility = self.sqr_value
        self.last_utility = 0
        self.next_dir = None


# Check to make sure argument count is correct
if len(sys.argv) < 3 or len(sys.argv) > 3:
    print('Incorrect number of arguments: ')
    print(len(sys.argv))
    print(sys.argv)
    exit(0)

world = sys.argv[1]
epsilon = sys.argv[2]

print('World: {0}'.format(world))
print('Epsilon: {0}'.format(epsilon))

# Read in matrix
matrix = []
world_file = open(world,'r')
for line in world_file:
    numbers = line.split(" ")
    nodes = []
    for node in numbers:
        nodes.append(int(node))
    matrix.append(nodes)

# create graph
world_max_x = len(matrix[0]) # 10
world_max_y = len(matrix) # 8
world_min_x = 0
world_min_y = 0
world = []
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

# 0 = Nothing   = 0
# 1 = Mountain  = -1.0
# 2 = Wall      = Can't pass
# 3 = Snake     = -2.0
# 4 = Barn      = 1.0

# 50 = Goal

# Sucsessful .8
# Left       .1
# Right      .1

# y = gama = .9
gama = .9
iteration = 0

exit_value = 100000000000 #Set just for first iteration


### MDP ###

while exit_value > float(epsilon)*(1-gama)/gama:
    exit = []
    for x in range(world_max_x-1,-1,-1):
        for y in range(world_max_y-1,-1,-1):
            if(x != world_max_x-1 or y != world_max_y-1):
                node = world[x][y]
                if node.sqr_type != 2:
                    # Set to none to make sure no node values are changed in trys
                    left = Node(0,0,0)
                    right = Node(0,0,0)
                    up = Node(0,0,0)
                    down = Node(0,0,0)
                    if x-1 > -1:
                        left = world[x-1][y]
                    else:
                        left.utility = 0
                    if x+1 < world_max_x:
                        right = world[x+1][y]
                    else:
                        right.utility = 0
                    if y+1 < world_max_y:
                        up = world[x][y+1]
                    else:
                        up.utility = 0
                    if y-1 > -1:
                        down = world[x][y-1]
                    else:
                        down.utility = 0

                    utilities = {}
                    if right.sqr_type != 2:
                        utilities['right'] = right.utility*.8 + up.utility*.1 + down.utility*.1
                    if left.sqr_type != 2:
                        utilities['left'] = left.utility*.8 + up.utility*.1 + down.utility*.1
                    if up.sqr_type != 2:
                        utilities['up'] = up.utility*.8 + right.utility*.1 + left.utility*.1
                    if down.sqr_type != 2:
                        utilities['down'] = down.utility*.8 + right.utility*.1 + left.utility*.1
                    #maximum = max(utilities, key=lambda i: x[i])
                    maximum = max(utilities.values())
                    #print utilities.values()
                    #print maximum,x,y
                    for nextnode, value in utilities.iteritems():
                        if value == maximum:
                            node.next_dir = nextnode
                    node.utility = maximum*gama + node.sqr_value
                    exit.append(node.utility-node.last_utility)

    gama *= gama
    exit_value = max(exit)


# Flip utility for doing Dijkstra and make sure Dijkstra will not pick walls
for x in range(world_max_x-1,-1,-1):
    for y in range(world_max_y-1,-1,-1):
        node = world[x][y]
        node.utility *= -1
        if node.sqr_type == 2:
            node.utility = 100000000000
            pass


# Dijkstra for fidning shortest path

Open = []
Closed = []

world[0][0].f = 0
world[0][0].distanceToStart = 0
world[0][0].heuristic = 0

Open.append(world[0][0])

nodes_evaluated = 0

# This is old astar code with heuristic removed. Some variables are not needed
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
                if abs(new_x-x) != abs(new_y-y): # Only left right up or down
                    # This is really gross
                    if new_x < 0:
                        new_x = 10000
                    if new_y < 0:
                        new_y = 10000

                    node = world[new_x][new_y]

                    #print("X: {0}, Y {1}".format(node.x,node.y))
                    cost = node.utility
                    if node in Closed: # Mountains
                        pass
                    else:
                        distanceToStart = cost + lowest_cost_node.distanceToStart
                        f = distanceToStart
                        parent = lowest_cost_node
                        #print("X: {0}, Y {1}".format(node.x,node.y))
                        if node in Open:
                            if node.f > f:
                                node.distanceToStart = distanceToStart
                                node.f = f
                                node.parent = parent
                        else:
                            #print("X: {0}, Y {1}".format(node.x,node.y))
                            node.distanceToStart = distanceToStart
                            node.f = f
                            node.parent = parent
                            Open.append(node)
            except:
                pass

# Make take path and output
path_x = []
path_y = []
path_u = []
node = lowest_cost_node
world[node.x][node.y].sqr_type = "-"
while node.x != 0 or node.y != 0:
    node = node.parent
    world[node.x][node.y].sqr_type = "-"
    path_x.append(node.x)
    path_y.append(node.y)
    path_u.append(node.utility*-1)
    #print('X:{0},Y:{1}'.format(node.x,node.y))

for y in range(world_max_y-1,-1,-1):
    for x in range(0,world_max_x):
        sys.stdout.write(str(world[x][y].sqr_type))
        sys.stdout.write(" ")
    print(" ")
print(" ")

for i in range(0,len(path_x)):
    print("X: {0} Y: {1} U: {2}".format(path_x[i],path_y[i],path_u[i]))
