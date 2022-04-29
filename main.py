import time

import pygame
from glob import glob

# Initialisation

pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((1920, 1080))  # Attention à bien rentrer un tuple

# Initialisation du titre
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

class Joueur(pygame.sprite.Sprite):

    def __init__(self):
        self.images_droite = [pygame.image.load(f) for f in glob(f"Persos/perso??.png")]
        self.images_gauche = [pygame.image.load(f) for f in glob(f"Persos/perso??_gauche.png")]
        self.orientation = ""
        self.frame = 0
        self.frame_change_time = time.time()

    def change_time(self):
        self.frame_change_time = time.time()

    def idle(self, x, y):
        if self.orientation == "droite":
            screen.blit(self.images_droite[0], (x, y))
        else:
            screen.blit(self.images_gauche[0], (x, y))

    def mvt_droite(self, x, y):
        self.orientation = "droite"
        if self.frame < len(self.images_droite):

            if time.time() > self.frame_change_time + 0.05:
                screen.blit(self.images_droite[self.frame], (x, y))
                self.frame += 1
                self.change_time()
            else:
                screen.blit(self.images_droite[self.frame], (x, y))

        else:
            self.frame = 0
            self.mvt_droite(x, y)

    def mvt_gauche(self, x, y):
        self.orientation = "gauche"
        if self.frame < len(self.images_gauche):

            if time.time() > self.frame_change_time + 0.05:
                screen.blit(self.images_gauche[self.frame], (x, y))
                self.frame += 1
                self.change_time()
            else:
                screen.blit(self.images_gauche[self.frame], (x, y))

        else:
            self.frame = 0
            self.mvt_gauche(x, y)


perso = Joueur()
perso_x = 50
perso_x_deplacement = 0
perso_y = 840

font = pygame.font.Font("freesansbold.ttf", 32)


def tour(x, y):
    screen.blit(tour_image, (x, y))


# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True
movement = False

while running:

    screen.blit(background_image, (background_x, 0))
    # screen.blit(font.render(f"{pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}", True, (255, 0, 0)), (0, 0))  # Affiche la position de la souris

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_d:
                movement = "Droite"
                perso_x_deplacement = 5
            if event.key == pygame.K_q:
                movement = "Gauche"
                perso_x_deplacement = -5
        if event.type == pygame.KEYUP:
            perso_x_deplacement = 0
            movement = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                perso_x_deplacement = 0

    if movement == "Droite":
        perso.mvt_droite(perso_x, perso_y)
    elif movement == "Gauche":
        perso.mvt_gauche(perso_x, perso_y)

    if perso_x_deplacement == 0:
        perso.idle(perso_x, perso_y)

    perso_x += perso_x_deplacement

    pygame.display.update()
