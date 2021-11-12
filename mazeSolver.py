from numpy import true_divide
import pygame
import time

# Maze Class
class Maze:
    # The maze (2D String array):
    maze = [['X','O','X','O','O','O'],
            ['O','O','O','O','X','O'],
            ['O','X','X','O','X','O'],
            ['O','O','X','O','X','O'],
            ['X','O','O','X','X','O'],
            ['X','X','X','O','O','O'],
            ['X','O','O','O','X','O'],
            ['X','O','X','X','O','O']]
    
    # Constructor
    def __init__(self, start, end, width, height, win):
        self.start = start
        self.end = end
        self.rows = len(self.maze)
        self.cols = len(self.maze[0])
        self.spaces = [[Space(self.maze[i][j], i, j, width, height) for j in range(self.cols)] for i in range(self.rows)]
        self.spaces[start[0]][start[1]].isStart = True
        self.spaces[end[0]][end[1]].isEnd = True
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win
        self.wall = 'X'
        self.path = 'O'
        self.solution = []

    # Function for updating the model
    def update_model(self):
        self.model = [[self.spaces[i][j].type for j in range(self.cols)] for i in range(self.rows)]

    # Function for drawing the maze
    def draw(self, win):
        ## horizontalGap = self.width / self.cols
        ## verticalGap = self.width / self.rows
        # Draw Grid Lines
        ## for i in range(self.rows+1):
        ##     thick = 1
        ##     pygame.draw.line(win, (255,0,255), (0, i*verticalGap), (self.width, i*verticalGap), thick)
        ##     pygame.draw.line(win, (255,0,255), (i*horizontalGap, 0), (i*horizontalGap, self.height), thick)

        # Draw Spaces
        for i in range(self.rows):
            for j in range(self.cols):
                self.spaces[i][j].draw(win, self.rows, self.cols)
                
    def drawSolution(self, win):
        horizontalGap = self.width / self.cols
        verticalGap = self.height / self.rows
        
        for i in range(len(self.solution)):
            pygame.draw.rect(win, (0,120,0), (self.solution[i][1],self.solution[i][0],horizontalGap,verticalGap))
            time.sleep(2)
            

    # Function for solving the maze using DFS
    def solve(self):
        # Get start and end spaces
        start = self.spaces[self.start[0]][self.start[1]]
        end = self.spaces[self.end[0]][self.end[1]]

        if not self.dfs(end, start):
            print("Unsolvable Maze")
            return
        
        print("Solved")
        return

    # Depth First Search for solving maze
    def dfs(self, end, cur):
        self.update_model()

        if(cur == end):
            # print("(" + str(cur.col) + "," + str(cur.row) + ")")
            self.solution.append([cur.row, cur.col])
            return True
        
        cur.visited = True
        cur.inPath = True
        cur.draw_change(self.win, self.rows, self.cols)
        self.update_model()
        pygame.display.update()
        print('Delaying time')
        pygame.time.delay(100)

        neighbors = cur.getUnvisitedNeighbors(self.spaces)

        for n in neighbors:
            if self.dfs(end, n):
                # print("(" + str(cur.col) + "," + str(cur.row) + ")")
                self.solution.append([cur.row, cur.col])
                return True
        
        cur.inPath = False
        self.update_model()
        cur.draw_change(self.win, self.rows, self.cols)
        pygame.display.update()
        print('Delaying time 2')
        pygame.time.delay(100)

        return False

# Class for the spaces on the maze
class Space:
    # Constructor
    def __init__(self, type, row, col, width, height):
        self.type = type
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.neighbors = []
        self.visited = False
        self.inPath = False
        self.isStart = False
        self.isEnd = False

    # Function for drawing a space
    def draw(self, win, rows, cols):
        # Get coordinates
        horizontalGap = self.width / cols
        verticalGap = self.height / rows
        x = self.col * horizontalGap
        y = self.row * verticalGap

        # Draw space
        if self.isStart:
            pygame.draw.rect(win, (0,255,0), (x,y,horizontalGap,verticalGap))
        elif self.isEnd:
            pygame.draw.rect(win, (255,0,0), (x,y,horizontalGap,verticalGap))
        elif self.type == 'X': # Wall
            pygame.draw.rect(win, (255,255,255), (x,y,horizontalGap,verticalGap)) # <=== Change last value (width) if needed
        elif self.type == 'O':
            pygame.draw.rect(win, (0,0,180), (x,y,horizontalGap,verticalGap))

    # Function for drawing a change in the space
    def draw_change(self, win, rows, cols):
        horizontalGap = self.width / cols
        verticalGap = self.height / rows
        x = self.col * horizontalGap
        y = self.row * verticalGap

        ## pygame.draw.rect(win, (255,255,255), (x,y,horizontalGap,verticalGap))

        if self.inPath:
            pygame.draw.rect(win, (0,120,0), (x,y,horizontalGap,verticalGap))
        else:
            pygame.draw.rect(win, (120,0,0), (x,y,horizontalGap,verticalGap))

    # Function for getting the unvisited neighbors of a space
    def getUnvisitedNeighbors(self, spaces):
        # print('Getting neighbors of (' + str(self.col) + ',' + str(self.row) + ')')
        neighbors = []

        if self.row > 0:
            if spaces[self.row-1][self.col].type == 'O' and not spaces[self.row-1][self.col].visited: 
                neighbors.append(spaces[self.row-1][self.col]) # Above
        if self.row < len(spaces)-1:
            if spaces[self.row+1][self.col].type == 'O' and not spaces[self.row+1][self.col].visited:
                neighbors.append(spaces[self.row+1][self.col]) # Below
        if self.col > 0:
            if spaces[self.row][self.col-1].type == 'O' and not spaces[self.row][self.col-1].visited:
                neighbors.append(spaces[self.row][self.col-1]) # Left
        if self.col < len(spaces[0])-1:
            if spaces[self.row][self.col+1].type == 'O' and not spaces[self.row][self.col+1].visited:
                neighbors.append(spaces[self.row][self.col+1]) # Right

        return neighbors

def redraw_window(win, maze):
    win.fill((0,0,0))
    
    # Draw grid and maz
    maze.draw(win)

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Maze Runner")
    maze = Maze([0,1],[7,4],540,540,win)
    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    maze.solve()
                    if len(maze.solution) > 0:
                        maze.solution.reverse()
                        # maze.drawSolution(win)
                        print()
                        print('Solution: ')
                        print(maze.solution)
                        print()
                        run = False
                        break
        
        if(not len(maze.solution) > 0):
            redraw_window(win, maze)
            pygame.display.update()            

main()
pygame.time.delay(7500)
pygame.quit()