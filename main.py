import pygame

# Initialisation
pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((800, 600))  # Attention à bien rentrer un tuple

# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
