# Maze-Runner

Program that will solve a given maze utilizing Depth First Search.

## Code:

The maze can be set in the mazeSolver.py file.
    - 'X's are walls and 'O's are paths
    - start and end inputs are given as a pair representing their [col,row]
    - Maze can be of any size (the window is limitted to 540x540)

## Maze Spaces:

    - Start space is displayed as a green rectangle
    - Path spaces ('O') are displayed as blue rectangles
    - Wall spaces ('X') are displayed as white rectangles
    - End space is displayed as a red rectangle

## Solving:

The program uses a Depth First Search approach to solve the given maze. As the maze is solved, the process is animated with:
    - green rectangles (spaces) = visited and on the current/correct path
    - red rectangles (spaces) = visited but not on the current/correct path
