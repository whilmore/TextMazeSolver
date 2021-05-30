import sys
import math

def printMaze(maze,path,moveCount):
    #loops through the maze, replacing the final path with x's
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if [i,j] in path:
                print("x",end='')
            else:
                print(maze[i][j],end='')
        print()
    print("Solution cost = ", len(path))
    print("Nodes opened = ",moveCount)

def pathFinder(cameFrom,start):
    finalPath = []

    #the last point is the one that met the goal, therefore the starting point
    current = cameFrom[-1]
    finalPath.append(current[1])
    #loop through the camefrom array backwards until the start of the maze
    while current[1] != start:
        for i in cameFrom:
            if i[0] == current[1]:
                current = i
                finalPath.append(i[1])
                break

    finalPath.remove(start)

    return finalPath

def checkSurrounding(maze,current,explored):
    validMoves = []

    # left
    if maze[current[0]][current[1] - 1] != "%" and ([current[0], current[1] - 1] not in explored):
        validMoves.append([current[0], current[1] - 1])

    # right
    if maze[current[0]][current[1] + 1] != "%" and ([current[0], current[1] + 1] not in explored):
        validMoves.append([current[0], current[1] + 1])

    # up
    if maze[current[0] - 1][current[1]] != "%" and ([current[0] - 1, current[1]] not in explored):
        validMoves.append([current[0] - 1, current[1]])

    # down
    if maze[current[0] + 1][current[1]] != "%" and ([current[0] + 1, current[1]] not in explored):
        validMoves.append([current[0] + 1, current[1]])

    return validMoves

def euclidian(point,goal):
    #needed math module for square root/ solves euclidian
    return math.sqrt(pow(point[0]-goal[0],2) + pow(point[1] - goal[1],2))

def heuristic(valid,goal):
    #placeholder
    chosen = valid[0]

    #replace the movement with the one closest to the goal
    for i in valid:
        if euclidian(chosen,goal) > euclidian(i,goal):
            chosen = i

    return chosen

def astar(start,goal,maze):
    current = start
    frontier = []
    explored = []
    path = []
    splits = []
    cameFrom = []
    moveCount = 0

    #add start to frontier
    frontier.append(current)

    while len(frontier) != 0 and (goal not in frontier):

        current = frontier[0]
        valid = checkSurrounding(maze, current, explored)

        if len(valid) > 0:
            moveCount += 1
            #choose the path with least amount of distance to the goal
            chosen = heuristic(valid,goal)
            frontier.append(chosen)
            explored.append(chosen)
            #avoids overriding the start symbol during printing
            if current != start:
                path.append(current)
            #log each split and origin of point
            for i in valid:
                splits.append(i)
                cameFrom.append([i, current])

            frontier.remove(current)

        else:
            #if no more options, return to a split
            if path[-1] in splits:
                frontier[0] = path[-1]
                splits.remove(path[-1])
            #backtrack down the path
            else:
                path.remove(path[-1])

    path = pathFinder(cameFrom,start)

    printMaze(maze, path,moveCount)

def depth(start,goal,maze):
    current = start
    frontier = []
    explored = []
    path = []
    splits = []
    cameFrom = []
    moveCount = 0

    # append the start to the frontier
    frontier.append(current)

    while len(frontier) != 0 and (goal not in frontier):
        moveCount += 1
        current = frontier[0]
        #check all possible moves
        valid = checkSurrounding(maze, current, explored)

        if len(valid) > 0:
            #pick the first possible move
            frontier.append(valid[0])
            explored.append(valid[0])
            if current != start:
                path.append(current)

            for i in valid:
                #log each time the path splits for backtrack uses
                splits.append(i)
                cameFrom.append([i, current])
            frontier.remove(current)

        else:
            #if the current path is at a split, take the other options
            if path[-1] in splits:
                frontier[0] = path[-1]
                splits.remove(path[-1])
            #else backtrack down the current path
            else:
                path.remove(path[-1])

    path = pathFinder(cameFrom,start)
    printMaze(maze,path,moveCount)

def breadth(start,goal,maze):
    current = start
    frontier = []
    explored = []
    cameFrom = []
    moveCount = 0

    #append the start to the frontier
    frontier.append(current)

    while len(frontier) != 0 and (goal not in frontier):
        current = frontier[0]
        #check all valid movements
        valid = checkSurrounding(maze,current,explored)
        #add each move to the frontier
        for i in valid:
            moveCount += 1
            frontier.append(i)
            explored.append(i)
            #log each move with its previous point
            cameFrom.append([i, current])
        frontier.remove(current)


    path = pathFinder(cameFrom,start)

    printMaze(maze,path,moveCount)

####################################################
#main
#input

if len(sys.argv) != 4:
    print("not enough or too many arguments")
    print("Proper usage example: python search.py -method breadth Maze2.txt")
    sys.exit(1)

file = str(sys.argv[3])
method = str(sys.argv[2])

#file open
with open(file) as f:
    maze = f.read().splitlines()

#initialize starting and goal positions
start = [0,0]
goal = [0,0]

#we can exit the loop if we find start and goal
foundStart = False
foundGoal = False

#prints the original maze
for i in range(len(maze)):
    print(maze[i])

#find the position of the start and goal
for i in range(len(maze)):
    for j in range(len(maze[i])):
        if maze[i][j] == 'S':
            start[0] = i
            start[1] = j
            foundStart = True
        elif maze[i][j] == 'G':
            goal[0] = i
            goal[1] = j
            foundGoal = True
        elif foundStart and foundStart:
            break
    if foundStart and foundGoal:
       break

if method == "breadth":
    breadth(start,goal,maze)
elif method == "depth":
    depth(start,goal,maze)
elif method == "astar":
    astar(start,goal,maze)
else:
    print("Not a valid input, type astar,breadth, or depth as algorithm choices")
    print("Proper usage example: python search.py -method breadth Maze2.txt")