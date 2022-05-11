import time
import pygame
import numpy as np

"""
Instructions for how to write this code are based on a video from NeuralNine.
https://www.youtube.com/watch?v=cRWg2SWuXtM
"""

#sets constants for the game colors
color_background = (10,10,10)
color_grid = (40,40,40)
color_die_next = (170, 170, 170)
color_alive_next = (0, 255, 0)

def update(screen, cells, size, with_progress=False):
    """
    applies the game rules and updates the screen
    :param screen: interactive screen using pygame
    :param cells: cells that are alive or dead
    :param size: size of the screen the game is played on
    :param with_progress: determines whether game is paused
    :return: updated cells
    """
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        #calculate the alive  neighbor cells and determine the color
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = color_background if cells[row, col] == 0 else color_alive_next

        #Apply the rules of the game
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = color_die_next

            elif 2 <= alive <=3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = color_alive_next

        #Draw the rectangle and grid for the game
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size -1))

    return updated_cells

def main():
    #Creating the display window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Collins Project Two')
    Icon = pygame.image.load('Collins.ico')
    pygame.display.set_icon(Icon)

    window = pygame.display.set_mode((800, 600), 0, 24)
    black = (0, 0, 0)
    end_it = False
    while (end_it == False):#Creating a Title Screen for the Game
        window.fill(black)
        myfont = pygame.font.SysFont("Arial", 40)
        nlabel = myfont.render("Conway's Game of Live", 1, (0, 255, 0))
        ntext = myfont.render("Click Mouse to begin", 1, (255, 0, 0))
        ntext2 = myfont.render("Spacebar Starts and Stops Game", 1, (0, 0, 255))
        ntext3 = myfont.render("Use Mouse to turn cells alive", 1, (0, 0, 255))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_it = True
        window.blit(nlabel, (100, 100))
        window.blit(ntext, (100, 200))
        window.blit(ntext2, (100, 300))
        window.blit(ntext3, (100, 400))
        pygame.display.flip()

    cells = np.zeros((60, 80))
    screen.fill(color_grid)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            #Making the game close if the exit button is selected
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                #Creating the pause if spacebar is pressed
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] //10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(color_grid)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == '__main__':
    main()

