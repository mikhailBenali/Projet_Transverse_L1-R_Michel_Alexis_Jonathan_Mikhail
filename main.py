import pygame
from glob import glob

# Initialisation
from pygame.time import delay

pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((1920, 1080))  # Attention à bien rentrer un tuple

# Initialisaiton du titre
pygame.display.set_caption("Pana pua")

tour_image = pygame.image.load("tour.png")
tour_x = 50
largeur_tour = 201

taille_tour = 256
tour_y = 1080 - taille_tour

background_image = pygame.image.load("background.jpg")
background_x = 0
background_x_change = 0


# Personnage

class Sprite(pygame.sprite.Sprite):

    def __init__(self):
        self.images = [pygame.image.load(f) for f in glob(f"Persos/*.png")]
        self.frame = 0

    def afficher(self, x, y):
        if self.frame < len(self.images):
            screen.blit(self.images[self.frame], (x, y))
            self.frame += 1
            delay(50)
        else:
            self.frame = 0


test = Sprite("New Piskel")

perso_image = pygame.image.load("Perso.png")
perso_x = 50
perso_y = 840

font = pygame.font.Font("freesansbold.ttf", 32)


def tour(x, y):
    screen.blit(tour_image, (x, y))


# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.blit(background_image, (background_x, 0))
    screen.blit(font.render(f"{pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}", True, (255, 0, 0)), (0, 0))  # Affiche la position de la souris

    screen.blit(perso_image, (perso_x, perso_y))

    test.afficher(200, 200)

    pygame.display.update()
