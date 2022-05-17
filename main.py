import pygame
import time as tm
from glob import glob
from math import *
import random

# Initialisation


pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((1920, 1080))  # Attention à bien rentrer un tuple

# Initialisaiton du titre
pygame.display.set_caption("Pana pua")

chateau_image = pygame.image.load("Images/Chateau.png").convert_alpha()
chateau_image = pygame.transform.scale(chateau_image, (512, 600))
tour_x = 50
largeur_tour = 201

taille_tour = 256
tour_y = 355

background_image = pygame.image.load("Images/background.jpg").convert()
background_x = 0
background_x_change = 0

clock = pygame.time.Clock()

bow_pos_calc = False
drawline = False


# Personnage
class Joueur(pygame.sprite.Sprite):

    def __init__(self):
        self.images_droite = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??.png")]
        self.images_gauche = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??_gauche.png")]
        self.mouvement = True
        self.orientation = "droite"
        self.frame = 0


    def idle(self, x, y):
        if self.orientation == "droite" and self.mouvement:
            screen.blit(self.images_droite[0], (x, y))
        elif self.orientation == "gauche" and self.mouvement:
            screen.blit(self.images_gauche[0], (x, y))

    def mvt_droite(self, x, y):
        self.orientation = "droite"
        if self.frame < len(self.images_droite):
            screen.blit(self.images_droite[self.frame], (x, y))
            self.frame += 1

        else:
            self.frame = 0
            self.mvt_droite(x, y)

    def mvt_gauche(self, x, y):
        self.orientation = "gauche"
        if self.frame < len(self.images_gauche):
            screen.blit(self.images_gauche[self.frame], (x, y))
            self.frame += 1

        else:
            self.frame = 0
            self.mvt_gauche(x, y)


perso = Joueur()
perso_x = 50
perso_x_deplacement = 0
perso_y = 840


class Sprite:
    def __init__(self, dossier):
        self.images = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/{dossier}/*.png")]
        self.frame = 0
        self.temps_derniere_frame = 0

    def afficher(self, x, y):
        self.temps_derniere_frame = tm.time()
        screen.blit(self.images[self.frame], (x, y))

    def changer_frame(self):
        if tm.time() > self.temps_derniere_frame + 500:
            self.frame += 1


slimes = [Sprite("slime") for i in range(5)]
slimes_x_pos = [random.randint(1920, 2600) for slime in slimes]
slimes_y = 800
slimes_x_deplacement = [random.randint(1, 8) for slime in slimes]


class Arrow(object):
    def __init__(self, arrow_x, arrow_y, image, bow_image):
        self.x = arrow_x
        self.y = arrow_y
        self.image = image
        self.rect = image.get_rect()
        self.bow_image = bow_image
        self.trainee = []

    @staticmethod
    def arrow_path(startx, starty, arrow_power, angle, arrow_time):
        velx = cos(radians(angle)) * -arrow_power  # velocity
        vely = sin(radians(angle)) * -arrow_power

        distx = velx * time  # distance
        disty = (vely * time) + ((-4.9 * arrow_time ** 2) / 2)  # 4.9 = gravité

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


def find_angle(initial_position, position):
    new_angle = atan2((initial_position[1] - position[1]), (initial_position[0] - position[0]))
    new_angle = degrees(new_angle)
    new_angle = abs(new_angle - 180)
    return new_angle


def redraw():
    global perso_x
    global bow_x
    screen.blit(background_image, (background_x, 0))
    # Affichage de la tour
    tour(tour_x, tour_y)
    if grounded_arrows:
        for img in grounded_arrows:
            screen.blit(img[0], (img[1], img[2]))
    if arrow.trainee:
        size = 1
        for trainee in arrow.trainee:
            screen.fill(trainee[0], (trainee[1], (size, size)))
            size += 0.5

    if drawline and initial_pos[0] - pos[0] != 0:
        angle = find_angle(initial_pos, pos)
        pygame.draw.line(screen, (64, 64, 64), line[0], line[1])
        bowImg = rot_center(pygame.transform.rotate(arrow.bow_image, 180), angle - 45)
    else:
        angle = find_angle([bow_x, bow_y], pos)
        bowImg = rot_center(pygame.transform.rotate(arrow.bow_image, 180), angle - 225)

    # Affichage personnage
    if movement == "Droite":
        perso.mvt_droite(perso_x, perso_y)
    elif movement == "Gauche":
        perso.mvt_gauche(perso_x, perso_y)
    if perso_x_deplacement == 0:
        perso.idle(perso_x, perso_y)

    if perso_x < 0:
        perso.mouvement = False
        perso_x = 0
    if perso_x >= 1920 - 128:
        perso.mouvement = False
        perso_x = 1920 - 128


    # Affichage arc
    screen.blit(bowImg, (bow_x, bow_y))

    perso_x += perso_x_deplacement
    bow_x = perso_x + 40
    clock.tick(60)

    """i = 0
    for slime in slimes:
        i += 1
        slime.afficher(slimes_x_pos[i], slimes_y)"""


font = pygame.font.Font("freesansbold.ttf", 32)


def tour(x, y):
    screen.blit(chateau_image, (x, y))


bow_x = perso_x + 40
bow_y = perso_y + 50
bow_images = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Arc/arc-?.png")]
arrow = Arrow(bow_x, bow_y, pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), bow_images[0])
power = 0
angle = 0
rotation_angle = 0
shoot = False
grounded_arrows = []

# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True
movement = False

while running:
    pos = pygame.mouse.get_pos()
    if drawline:
        line = [initial_pos, pos]
        arrow.bow_image = bow_images[0]
        distance = sqrt((initial_pos[0] - pos[0])**2 + (initial_pos[1] - pos[1])**2)
        if 0 <= distance < 250:
            arrow.bow_image = bow_images[0]
        if 250 <= distance < 500:
            arrow.bow_image = bow_images[1]
        if 500 <= distance < 750:
            arrow.bow_image = bow_images[2]
        if 750 <= distance:
            arrow.bow_image = bow_images[3]
    redraw()
    # screen.blit(font.render(f"{pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}", True, (255, 0, 0)), (0, 0))  # Affiche la position de la souris

    if shoot:
        if arrow.y < 925 and -32 < arrow.x < 1952:
            time += 0.25
            position = arrow.arrow_path(initial_bow_x, initial_bow_y, power, angle, time)
            screen.set_at((position[0], position[1]), (100, 100, 100))
            arrow.x = position[0]
            arrow.y = position[1]
            rotation_angle -= rotation_value
            rotated_arrow = rot_center(arrow.image, rotation_angle).convert_alpha()
            arrow.trainee.append([(235, 138, 126), (arrow.x+32, arrow.y+32)])
            if len(arrow.trainee) > 15:
                arrow.trainee.pop(0)
            screen.blit(rotated_arrow, (arrow.x, arrow.y))
        else:
            grounded_arrows.append([rotated_arrow, arrow.x, arrow.y])
            if len(grounded_arrows) > 20:
                grounded_arrows.pop(0)
            shoot = False
            arrow.x = bow_x
            arrow.y = bow_y
            arrow.trainee = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_d:
                perso.mouvement = True
                movement = "Droite"
                perso_x_deplacement = 10
            if event.key == pygame.K_q:
                perso.mouvement = True
                movement = "Gauche"
                perso_x_deplacement = -10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and movement == "Droite":
                movement = ""
                perso_x_deplacement = 0
            if event.key == pygame.K_q and movement == "Gauche":
                movement = ""
                perso_x_deplacement = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                drawline = True
                initial_pos = pygame.mouse.get_pos()
                bow_pos_calc = True

        if event.type == pygame.MOUSEBUTTONUP:
            if not shoot and drawline:
                drawline = False
                arrow.bow_image = bow_images[0]
                initial_bow_x = bow_x
                initial_bow_y = bow_y
                angle = find_angle(initial_pos, pos)
                arrow.image = rot_center(pygame.transform.rotate(pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), 180), angle - 45)
                rotation_angle = 0
                shoot = True
                time = 0
                power = sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 6
                rotation_value = 1
                if power > 25:
                    if pos[0] > initial_pos[0] + 32:
                        rotation_value = -85/power
                    else:
                        rotation_value = 85/power

    pygame.display.update()
