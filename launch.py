import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from const import WIDTH, HEIGHT
from game import Game

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(win)

run = True
while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            game.reset_allowed()
            if not game.clicked:
                pass
            else:
                pass


pygame.quit()
