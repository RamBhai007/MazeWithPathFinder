from collections import deque
import heapq
import os
import sys
import pygame

cell = 20
clock = pygame.time.Clock()

program_directory = os.path.dirname(sys.argv[0])
circle = pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "circle.png")),(15,15))
pacman =pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "pacman.jpg")),(20,20))
pacman_food =pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "pacman_food.png")),(20,20))
pacman_track=pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "pacman_track.png")),(15,15))
wall =pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "wall.png")),(20,20))
empty=pygame.transform.scale(pygame.image.load(os.path.join(program_directory, "empty.jpg")),(20,20))

def markAsVisited(currNode, Screen):
    Screen.blit(circle, (currNode[1] * cell, currNode[0] * cell))
    pygame.display.flip()
    clock.tick(60)

def closeFood(matrix, start):
    queue = deque([(start, 0)])
    visited = set()
    FoodPositions = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == '.':
                FoodPositions.append((i, j))
    while queue:
        currPos, distance = queue.popleft()
        if currPos in FoodPositions:
            return currPos
        visited.add(currPos)
        neighbourNodes = []
        for dr, dc in [(1, 0), (-1, 0),(0, 1), (0, -1)]:
            nr, nc = currPos[0] + dr, currPos[1] + dc
            if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]) and matrix[nr][nc] != '%' and (nr, nc) not in visited:
                neighbourNodes.append((nr, nc))
        for neighbor in neighbourNodes:
            queue.append((neighbor, distance + 1))
    return None

def neighbourNodes(MazeMatrix, currNode):
    nodesList = []
    dirs = [(1, 0), (-1, 0),(0, 1), (0, -1)]
    for x, y in dirs:
        xNode = currNode[0]+x
        yNode = currNode[1]+y
        if 0 <= xNode < len(MazeMatrix) and 0 <= yNode < len(MazeMatrix[0]) and MazeMatrix[xNode][yNode] != '%':
            nodesList.append((xNode, yNode))
    return nodesList

def StartandEndPositions(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 'P':
                StartPoint = (i, j)
            elif mat[i][j] == '.':
                EndingPoint = (i, j)
    return StartPoint, EndingPoint

def assignmentMazeSolvingPart1(MazeMatrix,Screen,algo):
    if algo==1:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        StartPoint, EndingPoint = StartandEndPositions(MazeMatrix)
        stack = [(StartPoint, [StartPoint])]
        visited = set()
        while stack:
            currNode, Route = stack.pop()
            nodesExpanded += 1
            MaxDepth = max(MaxDepth, len(Route))
            MaxFringe = max(MaxFringe, len(stack))
            

            if currNode == EndingPoint:
                return Route, len(Route)-1, nodesExpanded, MaxDepth, MaxFringe

            if currNode not in visited:
                markAsVisited(currNode, Screen)
                visited.add(currNode)
                for _ in neighbourNodes(MazeMatrix, currNode):
                    if _ not in visited:
                        stack.append((_, Route+[_]))

        return None, None, None, None, None
    elif algo==2:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        StartPoint, EndingPoint = StartandEndPositions(MazeMatrix)
        queue = deque([(StartPoint, [StartPoint])])
        VisitedSet = set()
        while queue:
            currNode, Route = queue.popleft()
            nodesExpanded += 1
            MaxDepth = max(MaxDepth, len(Route))
            MaxFringe = max(MaxFringe, len(queue))
            if currNode == EndingPoint:
                return Route, len(Route)-1, nodesExpanded, MaxDepth, MaxFringe
            if currNode not in VisitedSet:
                markAsVisited(currNode, Screen)
                VisitedSet.add(currNode)
                for _ in neighbourNodes(MazeMatrix, currNode):
                    if _ not in VisitedSet:
                        queue.append((_, Route+[_]))
        return None, None, None, None, None
    elif algo==3:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        StartPoint, EndingPoint = StartandEndPositions(MazeMatrix)
        heap = [(0, StartPoint, [StartPoint])]
        VisitedSet = set()
        while heap:
            k, currNode, Route = heapq.heappop(heap)
            nodesExpanded += 1
            MaxDepth = max(MaxDepth, len(Route))
            MaxFringe = max(MaxFringe, len(heap))
            if currNode == EndingPoint:
                return Route, len(Route)-1, nodesExpanded, MaxDepth, MaxFringe
            if currNode not in VisitedSet:
                markAsVisited(currNode, Screen)
                VisitedSet.add(currNode)
                for _ in neighbourNodes(MazeMatrix, currNode):
                    if _ not in VisitedSet:
                        Cost = abs(_[0]-EndingPoint[0]) +abs(_[1]-EndingPoint[1])
                        heapq.heappush(heap, (Cost, _, Route+[_]))
        return None, None, None, None, None

def assignmentMazeSolvingPart2(MazeMatrix,algo):
    
    direction = [(1, 0), (-1, 0),(0, 1), (0, -1)]
    if algo==1:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        matrix = MazeMatrix

        FoodPositions = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'P':
                    start = (i, j)
                elif matrix[i][j] == '.':
                    FoodPositions.append((i, j))

        Route = []
        while FoodPositions:
            closestFood = closeFood(matrix, start)
            visitedSet = set()
            stack = [(start, 0, [])]

            while stack:
                pos, currdist, path = stack.pop(0)
                nodesExpanded += 1
                MaxDepth = max(MaxDepth, len(path))
                MaxFringe = max(MaxFringe, len(stack))

                if pos == closestFood:
                    Route.append(path + [pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start = pos
                    FoodPositions.remove(pos)
                    break

                if pos not in visitedSet:
                    visitedSet.add(pos)
                    for i, j in direction:
                        nextRow = pos[0] + i
                        nextCol = pos[1] + j
                        if (
                            0 <= nextRow < len(matrix)
                            and 0 <= nextCol < len(matrix[0])
                            and matrix[nextRow][nextCol] != '%'
                            and (nextRow, nextCol) not in visitedSet
                        ):
                            stack.append(
                                ((nextRow, nextCol), currdist + 1, path + [pos]))

        return Route, len(Route) - 1, nodesExpanded, MaxDepth, MaxFringe
    elif algo==2:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        matrix = MazeMatrix
        FoodPositions = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'P':
                    start = (i, j)
                elif matrix[i][j] == '.':
                    FoodPositions.append((i, j))

        Route = []
        while FoodPositions:
            closetFood = closeFood(matrix, start)
            vistedSet = set()
            queue = deque([(start, 0, [])])
            while queue:
                pos, currdist, path = queue.popleft()
                nodesExpanded += 1
                MaxDepth = max(MaxDepth, len(path))
                MaxFringe = max(MaxFringe, len(queue))

                if (pos == closetFood):
                    Route.append(path+[pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start = pos
                    FoodPositions.remove(pos)
                    break
                if pos not in vistedSet:
                    vistedSet.add(pos)
                    for i, j in direction:
                        nextRow = pos[0]+i
                        nextCol = pos[1]+j
                        if 0 <= nextRow < len(matrix) and 0 <= nextCol < len(matrix[0]) and matrix[nextRow][nextCol] != '%' and (nextRow, nextCol) not in vistedSet:
                            queue.append(
                                ((nextRow, nextCol), currdist+1, path+[pos]))

        return Route,len(Route)-1, nodesExpanded, MaxDepth, MaxFringe
    elif algo==3:
        nodesExpanded = 0
        MaxDepth = 0
        MaxFringe = 0
        matrix = MazeMatrix

        FoodPositions = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 'P':
                    start = (i, j)
                elif matrix[i][j] == '.':
                    FoodPositions.append((i, j))
        
        Route=[]
        while FoodPositions:

            closetFood = closeFood(matrix, start)
            vistedSet = set()
            heap = [(start, 0, [])]
            while heap:
                pos, currdist, path = heapq.heappop(heap)
                nodesExpanded += 1
                MaxDepth = max(MaxDepth, len(path))
                MaxFringe = max(MaxFringe, len(heap))

                if (pos == closetFood):
                    Route.append(path+[pos])
                    matrix[pos[0]] = list(matrix[pos[0]])
                    matrix[pos[0]][pos[1]] = 'P'
                    matrix[pos[0]] = ''.join(matrix[pos[0]])
                    start = pos
                    FoodPositions.remove(pos)
                    break
                if pos not in vistedSet:
                    vistedSet.add(pos)
                    for i, j in direction:
                        nextRow = pos[0]+i
                        nextCol = pos[1]+j
                        if 0 <= nextRow < len(matrix) and 0 <= nextCol < len(matrix[0]) and matrix[nextRow][nextCol] != '%' and (nextRow, nextCol) not in vistedSet:
                            heapq.heappush(heap, (((nextRow, nextCol), currdist+1+abs(nextRow-closetFood[0])+abs(nextCol-closetFood[1]), path+[pos])))

        return Route,len(Route)-1, nodesExpanded, MaxDepth, MaxFringe

def main():
    MazeListPart1 = ['bigMaze.lay', 'mediumMaze.lay', 'smallMaze.lay','openMaze.lay']
    MazeListPart2 =['trickySearch.lay', 'tinySearch.lay', 'smallSearch.lay']
    print("Choose an Assignment to Run:\n1 for MazeSolution \n2 for SearchMazeSolution ")
    
    nameList=["","DFS","BFS","ASTAR"]
    
    def LayToMatrix(layPath):
        with open(layPath, 'r') as f:
            MazeMatrix = [list(line.strip()) for line in f.readlines()]
        return MazeMatrix
    
    def drawMazePart1(MazeMatrix):
        for i in range(len(MazeMatrix)):
            for j in range(len(MazeMatrix[0])):
                if MazeMatrix[i][j] == '%':
                    Screen.blit(wall,(j*cell,i*cell))
                elif MazeMatrix[i][j] == 'P':
                    Screen.blit(pacman,(j*cell,i*cell))
                elif MazeMatrix[i][j] == '.':
                    Screen.blit(pacman_food,(j*cell,i*cell))
                else:
                    Screen.blit(empty,(j*cell,i*cell))
            pygame.display.flip()
                               
    def drawMazePart2(MazeMatrix):
        for i in range(len(MazeMatrix)):
            for j in range(len(MazeMatrix[0])):
                if MazeMatrix[i][j] == '%':
                    Screen.blit(wall,(j*cell,i*cell))
                elif MazeMatrix[i][j] == 'P':
                    Screen.blit(pacman,(j*cell,i*cell))
                elif MazeMatrix[i][j] == '.':
                    Screen.blit(pacman_food,(j*cell,i*cell))
                else:
                    Screen.blit(empty,(j*cell,i*cell))

    def drawFinalPath(Route, Screen, Cost, MaxDepth, NoofNodesExpanded, MaxFringe):
        for currNode in Route:
            Screen.blit(pacman_track,(currNode[1]*cell,currNode[0]*cell))
            display_infoPart1(Screen, Cost, MaxDepth,NoofNodesExpanded, MaxFringe)
            pygame.display.flip()
            clock.tick(120)

    def display_infoPart1(Screen, Cost, MaxDepth, nodesExpanded, MaxFringe):
        font = pygame.font.SysFont('Helvetica', 25,bold=False, italic=True)
        text1 = font.render("Route Cost: {}".format(Cost), True, (255, 255, 255))
        text2 = font.render("Maximum Depth: {}".format(MaxDepth), True, (255, 255, 255))
        text3 = font.render("No.of Nodes Expanded: {}".format(nodesExpanded), True, (255, 255, 255))
        text4 = font.render("Maximum Fringe: {}".format(MaxFringe), True, (255, 255, 255))
        Screen.blit(text1, (LENGTH-290, 30))
        Screen.blit(text2, (LENGTH-290, 60))
        Screen.blit(text3, (LENGTH-290, 90))
        Screen.blit(text4, (LENGTH-290, 120))

    def display_infoPart2(Screen, cost, maxDepth, nodesExpanded, maxFringe):
        font = pygame.font.SysFont('Helveticas', 20, bold=False, italic=True)
        text1 = font.render("Path Cost: {}".format(cost), True, (255, 255, 255))
        text2 = font.render("Max Depth: {}".format(maxDepth), True, (255, 255, 255))
        text3 = font.render("Nodes Expanded: {}".format(nodesExpanded), True, (255, 255, 255))
        text4 = font.render("Max Fringe: {}".format(maxFringe), True, (255, 255, 255))
        
        Screen.blit(text1, (LENGTH-290, 0))
        Screen.blit(text2, (LENGTH-290, 30))
        Screen.blit(text3, (LENGTH-290, 60))
        Screen.blit(text4, (LENGTH-290, 90))

    ChoiceOfAssignment = int(input())
    if ChoiceOfAssignment == 1:

        print("Choose LayOut File : \n 0 for bigMaze \n 1 for mediunMaze \n 2 for smallMaze \n 3 for openMaze")

        ChoiceOfLayout = int(input())

        MazeMatrix = LayToMatrix(MazeListPart1[ChoiceOfLayout])

        print("Enter Input of Algorithum Choice:\n 0 for original matrix \n 1 for DepthFirstSearch Algo Route \n 2 for BreathFirstSearch Algo Route \n 3 for A* Algo Route")

        ChoiceOfAlgo = int(input())


        cell = 20
        clock = pygame.time.Clock()
        pygame.init()
        BREATH = (len(MazeMatrix)*cell)
        LENGTH = (len(MazeMatrix[0])*cell)+300
        Screen = pygame.display.set_mode((LENGTH, BREATH), pygame.RESIZABLE)

        flag = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if flag:
                drawMazePart1(MazeMatrix)

            if ChoiceOfAlgo == 0:
                pygame.display.set_caption("Maze Route")
                pygame.display.flip()

            if ChoiceOfAlgo in [1,2,3]:
                
                pygame.display.set_caption("Maze Route"+nameList[ChoiceOfAlgo])
                pygame.display.flip()
                Route, Cost, NoofNodesExpanded, MaxDepth, MaxFringe = assignmentMazeSolvingPart1(MazeMatrix, Screen, ChoiceOfAlgo)
                print(nameList[ChoiceOfAlgo]+" Route:", Route)
                drawFinalPath(Route, Screen, Cost,MaxDepth, NoofNodesExpanded, MaxFringe)
                pygame.time.wait(10)
                pygame.display.flip()
                ChoiceOfAlgo = 0
                flag = False
            
    elif ChoiceOfAssignment == 2:
        print("Choose a Layout File : \n0 for trickySearch\n1 for tinySearch\n2 for smallSearch")
    
        ChoiceOfLayout = int(input())

        print("Choose an algo to run : \n0 for original matrix\n1 for dfs Algo path\n2 for bfs Algo path\n3 for A* Algo path")

        ChoiceOfAlgo = int(input())

        MazeMatrix = LayToMatrix(MazeListPart2[ChoiceOfLayout])

        pygame.init()
        cell = 20
        BREATH = (len(MazeMatrix)*cell)
        LENGTH = len(MazeMatrix[0])*cell+300

        Screen = pygame.display.set_mode((LENGTH, BREATH), pygame.RESIZABLE)
        pygame.display.set_caption("Maze Route with Multiple Targets")
        clock = pygame.time.Clock()
        flag = 0
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if flag == 0:
                drawMazePart2(MazeMatrix)

            if ChoiceOfAlgo == 0:
                pygame.display.set_caption("Maze Route ")
                pygame.display.flip()

            if ChoiceOfAlgo in [1,2,3]:
                path, cost, node_expanded, max_depth, max_fringe = assignmentMazeSolvingPart2(
                    MazeMatrix,ChoiceOfAlgo)
                result_list = [tup for sublist in path for tup in sublist]
                prev = path[0][0]
                for node in result_list:
                    pygame.display.set_caption("Maze Route part2 "+nameList[ChoiceOfAlgo])
                    Screen.blit(empty,(prev[1]*cell,prev[0]*cell))
                    clock.tick(10)
                    Screen.blit(pacman,(node[1]*cell,node[0]*cell))
                    prev = node
                    pygame.display.flip()
                display_infoPart2(Screen, cost, max_depth,node_expanded, max_fringe)
                print(nameList[ChoiceOfAlgo]+" Route :", path)

                ChoiceOfAlgo = 0
            pygame.display.flip()
            flag = flag+1

if __name__ == "__main__":    
    main()
