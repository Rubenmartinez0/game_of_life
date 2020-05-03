import pygame
import numpy as np
import time

pygame.init()

# Assign width and height pixels.
width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

# Creating every cell of the game.
nxC, nyC = 50, 50
# Width and height of every cell depends of the screen width and height
dimCW = width / nxC
dimCH = height / nyC

# Storage for every state of every cell.
# Values: alive = 1; death = 0;
gameState = np.zeros((nxC, nyC))


# Variable to pause the execution of the game.
pauseExecution = False

# Execution loop
while True:
	
	#Copy the last state of the game.
	newGameState = np.copy(gameState)

	screen.fill(bg)
	time.sleep(0.25)

	# Event listener for keyboard and mouse

	ev = pygame.event.get()

	for event in ev:
		if event.type == pygame.KEYDOWN:
			pauseExecution = not pauseExecution

		mouseClick = pygame.mouse.get_pressed()

		if sum(mouseClick) > 0:
			posX, posY = pygame.mouse.get_pos()
			celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
			newGameState[celX, celY] = not mouseClick[2]

	# We go through all the cells.
	for y in range(0, nxC):
		for x in range(0, nyC):

			if not pauseExecution:

				# Calculate the number of neighbours.
				n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
						  gameState[(x)     % nxC, (y - 1) % nyC] + \
						  gameState[(x + 1) % nxC, (y - 1) % nyC] + \
						  gameState[(x - 1) % nxC,     (y) % nyC] + \
						  gameState[(x + 1) % nxC,     (y) % nyC] + \
						  gameState[(x - 1) % nxC, (y + 1) % nyC] + \
						  gameState[(x)     % nxC, (y + 1) % nyC] + \
						  gameState[(x + 1) % nxC, (y + 1) % nyC]


				# 1: If a death cell is death and has exactly 3 alive neighbours, revives.
				if gameState[x, y] == 0 and n_neigh == 3:
					newGameState[x, y] = 1
				# 2: If an alive cell has less than 2 alive neighbours or more than 3 alive neighbours, dies.
				elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
					newGameState[x, y] = 0


			# Define every corner of each cell.
			poly = [((x) * dimCW, y * dimCH),
					((x+1) * dimCW, y * dimCH),
					((x+1) * dimCW, (y+1) * dimCH),
					((x) * dimCW, (y+1) * dimCH)]


			# Draw every cell

			if newGameState[x, y] == 0:		
				# Draw death cell
				pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
			else:
				# Draw alive cell
				pygame.draw.polygon(screen, (255, 255, 255), poly, 0)


	# Update content to show
	gameState = np.copy(newGameState)


	pygame.display.flip()

pass