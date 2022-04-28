import pygame
from glob import glob
from math import *

# Initialisation
from pygame.time import delay

pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((1920, 1080))  # Attention à bien rentrer un tuple

# Initialisaiton du titre
pygame.display.set_caption("Pana pua")

tour_image = pygame.image.load("Images/tour.png").convert_alpha()
tour_x = 50
largeur_tour = 201

taille_tour = 256
tour_y = 1080 - taille_tour

background_image = pygame.image.load("Images/background.jpg").convert()
background_x = 0
background_x_change = 0


# Personnage

class Joueur(pygame.sprite.Sprite):

    def __init__(self):
        self.images_droite = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??.png")]
        self.images_gauche = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??_gauche.png")]
        self.orientation = ""
        self.frame = 0

    def idle(self, x, y):
        if self.orientation == "droite":
            screen.blit(self.images_droite[0], (x, y))
        else:
            screen.blit(self.images_gauche[0], (x, y))

    def mvt_droite(self, x, y):
        self.orientation = "droite"
        if self.frame < len(self.images_droite):
            screen.blit(self.images_droite[self.frame], (x, y))
            self.frame += 1
            delay(50)   #TODO:Mettre le timer pour les frame en global, c'est ce qui fait actuellement lag le jeu
        else:
            self.frame = 0
            self.mvt_droite(x, y)

    def mvt_gauche(self, x, y):

        self.orientation = "gauche"
        if self.frame < len(self.images_gauche):
            screen.blit(self.images_gauche[self.frame], (x, y))
            self.frame += 1
            delay(50)
        else:
            self.frame = 0
            self.mvt_gauche(x, y)


class Arrow(object):
    def __init__(self, arrow_x, arrow_y, image):
        self.x = arrow_x
        self.y = arrow_y
        self.image = image
        self.rect = image.get_rect()

    @staticmethod
    def arrow_path(startx, starty, arrow_power, angle, arrow_time):
        velx = cos(radians(angle)) * arrow_power  # velocity
        vely = sin(radians(angle)) * arrow_power

        distx = velx * time  # distance
        disty = (vely * time) + ((-4.9 * arrow_time**2)/2)  # 4.9 = gravité

        newx = round(distx + startx)
        newy = round(starty - disty)

        return newx, newy


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def find_angle(position):
    pos_x = bow_x + 32
    pos_y = bow_y + 32
    new_angle = atan2((pos_y - position[1]), (pos_x - position[0]))
    new_angle = degrees(new_angle)
    new_angle = abs(new_angle - 180)
    return new_angle


perso = Joueur()
perso_x = 50
perso_x_deplacement = 0
perso_y = 840
bow_x = perso_x + 40
bow_y = perso_y + 50
arrow = Arrow(bow_x, bow_y, pygame.image.load("Images/Arc/arrow.png").convert_alpha())
bow_image = pygame.image.load("Images/Arc/archer.png").convert_alpha()
power = 0
angle = 0
rotation_angle = 0
shoot = False


def redraw():
    screen.blit(background_image, (background_x, 0))
    pygame.draw.line(screen, (64, 64, 64), line[0], line[1])

    # Affichage de la tour
    tour(tour_x, tour_y)

    # Affichage personnage
    if movement == "Droite":
        perso.mvt_droite(perso_x, perso_y)
    elif movement == "Gauche":
        perso.mvt_gauche(perso_x, perso_y)
    if perso_x_deplacement == 0:
        perso.idle(perso_x, perso_y)

    # Affichage arc
    angle = find_angle(pos)
    bowImg = rot_center(pygame.transform.rotate(bow_image, 180), angle-45)
    screen.blit(bowImg, (bow_x, bow_y))



font = pygame.font.Font("freesansbold.ttf", 32)


def tour(x, y):
    screen.blit(tour_image, (x, y))


# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True
movement = False

while running:
    pos = pygame.mouse.get_pos()
    line = [(bow_x + 32, bow_y + 32), pos]
    redraw()
    # screen.blit(font.render(f"{pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}", True, (255, 0, 0)), (0, 0))  # Affiche la position de la souris

    if shoot:
        if arrow.y < 1112 and -32 < arrow.x < 1952:
            time += 0.03
            position = arrow.arrow_path(initial_bow_x, initial_bow_y, power, angle, time)
            arrow.x = position[0]
            arrow.y = position[1]
            rotation_angle -= rotation_value
            screen.blit(pygame.transform.rotate(arrow.image, rotation_angle), (arrow.x, arrow.y))
        else:
            shoot = False
            arrow.x = bow_x
            arrow.y = bow_y

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_d:
                movement = "Droite"
                perso_x_deplacement = 10
            if event.key == pygame.K_q:
                movement = "Gauche"
                perso_x_deplacement = -10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and movement == "Droite":
                movement = False
                perso_x_deplacement = 0
            if event.key == pygame.K_q and movement == "Gauche":
                movement = False
                perso_x_deplacement = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                initial_bow_x = bow_x
                initial_bow_y = bow_y
                angle = find_angle(pos)
                print(f"angle fleche = {angle}")
                arrow.image = rot_center(pygame.transform.rotate(pygame.image.load("Images/Arc/arrow.png").convert_alpha(), 180), angle - 45)
                if pos[0] > bow_x + 32:
                    rotation_value = -0.10
                else:
                    rotation_value = 0.10
                rotation_angle = 0
                shoot = True
                time = 0
                power = -sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2)/6
                angle = find_angle(pos)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                perso_x_deplacement = 0

    perso_x += perso_x_deplacement
    bow_x = perso_x + 40

    pygame.display.update()
