import pygame, sys
import numpy as np
import matplotlib.pyplot as plt
import time
import math

pygame.init()

# Height and width of the screen
width, height = 900, 900

# Number of cells
nxC = 400
nyC = 400
# Dimensions of each cell
dimCW = (width-1) / nxC
dimCH = (height-1) / nyC

# Background color
bg = 25, 25, 25

# Creation of the screen
screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)

# Paint the screen with the background color
screen.fill(bg)

# Initialize the board with the shape we want
gameState = np.zeros((nxC, nyC))

# Triangular Automata
gameState[int(nxC / 2), 0] = 1

# Execution control of the player
pauseExec = True


# COOL NUMBERS RULES:
rules = list(np.binary_repr(30, width=8))
#rules = list(np.binary_repr(110, width=8))
#rules = list(np.binary_repr(90, width=8))
#rules = list(np.binary_repr(22, width=8))
#rules = list(np.binary_repr(99, width=8))

"""
# RANDOM NUMBER RULE:
RULE = np.random.randint(256)
print("Rule: " + str(RULE))
rules = list(np.binary_repr(RULE, width=8))
"""


rules.reverse()


for y in range(0, nyC):
        for x in range(0, nxC):
            
            # Calculate the position of each cell
            poly = [((x)*dimCW, (y)*dimCH),
                    ((x+1)*dimCW, (y)*dimCH),
                    ((x+1)*dimCW, (y+1)*dimCH),
                    ((x)*dimCW, (y+1)*dimCH)]

            pygame.draw.polygon(screen, (128,128,128), poly, 1)
            

y = 0

while y < nyC:

    new_gameState = np.copy(gameState)

    # proceed events
    ev = pygame.event.get()

    for event in ev:
        # Detect if any key is pressed
        if event.type == pygame.KEYDOWN:
            pauseExec = not pauseExec

        # Detect if the mouse is pressed
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()

            if posX > 0 and posX < width-1 and posY > 0 and posY < height-1:
                new_gameState[math.floor(posX / dimCW),
                              math.floor(posY / dimCH)] = mouseClick[0] and not mouseClick[2]
         

    for x in range(0, nxC):
        # If the execution is not paused
        if not pauseExec:
                            
            ruleIdx = 4 * gameState[(x-1) % nxC, y] + 2 * gameState[x, y] + 1 * gameState[(x+1) % nxC, y]

            new_gameState[x, (y+1) % nyC] = rules[int(ruleIdx)]

        # Calculate the position of each cell
        poly = [((x)*dimCW, (y)*dimCH),
                ((x+1)*dimCW, (y)*dimCH),
                ((x+1)*dimCW, (y+1)*dimCH),
                ((x)*dimCW, (y+1)*dimCH)]

        # Draw the state computed in the cell
        if new_gameState[x,y] == 1:
            pygame.draw.polygon(screen, (255,255,255), poly, 0)

    time.sleep(0.01)
    
    if not pauseExec:
        y = (y + 1)
        

    gameState = np.copy(new_gameState)
    pygame.display.flip()


time.sleep(5)