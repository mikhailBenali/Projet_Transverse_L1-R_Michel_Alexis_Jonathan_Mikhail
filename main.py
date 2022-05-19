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
    def __init__(self, arrow_x, arrow_y, image, angle, power):
        self.x = arrow_x
        self.y = arrow_y
        self.image = image
        self.rect = image.get_rect()
        self.trainee = []
        self.angle = angle
        self.power = power

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
    for arrow in arrows_list:
        if grounded_arrows:
            for img in grounded_arrows:
                screen.blit(img[0], (img[1], img[2]))
        if arrow.trainee:
            size = 1
            for trainee in arrow.trainee:
                screen.fill(trainee[0], (trainee[1], (size, size)))
                size += 0.5



    # Creation de la cible pour la compétence "Arrow rain"


    if drawline:
        angle = find_angle(initial_pos, pos)
        pygame.draw.line(screen, (64, 64, 64), line[0], line[1])
        bowImg = rot_center(pygame.transform.rotate(bow_image, 180), angle - 45)
    else:
        angle = find_angle([bow_x, bow_y], pos)
        bowImg = rot_center(pygame.transform.rotate(bow_image, 180), angle - 225)

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
    screen.blit(aptitude_bar_images, (5, 5))
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
bow_images = [pygame.image.load(f).convert_alpha() for f in glob("Images/Arc/arc-?.png")]
bow_image = bow_images[0]
aptitude_bar_images = pygame.image.load("Images/aptitude_bar/parchemin_9.png")
    # [pygame.image.load(f).convert_alpha() for f in glob("Images/aptitude_bar/parchemin_?.png")]
arrows_list = [Arrow(bow_x, bow_y, pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), 0, 0)]
power = 0
old_angle = 0
arrow_angle = {}
new_arrow_angle = 0
fallen_arrow = 0
shoot = False
outline_size = 10
grounded_arrows = []
competence = 0
arrow_split_ability = 1
arrow_rain = 0
arrow_rain_active = 0
arrow_rain_init = 0
ground_target = False

# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True
movement = False

while running:
    pos = pygame.mouse.get_pos()
    if drawline:
        line = [initial_pos, pos]
        distance = sqrt((initial_pos[0] - pos[0]) ** 2 + (initial_pos[1] - pos[1]) ** 2)

        # Gère le bandage de l'arc
        if 0 <= distance < 250:
            bow_image = bow_images[0]
        if 250 <= distance < 500:
            bow_image = bow_images[1]
        if 500 <= distance < 750:
            bow_image = bow_images[2]
        if 750 <= distance:
            bow_image = bow_images[3]
    redraw()



    if arrow_rain_init:
        competence = 1
        arrow_rain_number = random.randint(40, 50)
        falling_arrows = []
        for i in range(arrow_rain_number):
            falling_arrows.append(Arrow(ground_x - 2*random.randint(50, 400), -random.randint(80, 1000), rot_center(pygame.image.load("Images/Arc/phlaitche-1.png"), 250).convert_alpha(), 0, 100))
        arrow_rain_active = True
        arrow_rain_init = 0
        arrow_speed = []
    if arrow_rain_active:
        for arrow in falling_arrows:
            screen.blit(arrow.image, (arrow.x, arrow.y))
            arrow.x += 10
            arrow.y += 30
            if arrow.y > 925:
                grounded_arrows.append([arrow.image, arrow.x, arrow.y])
                falling_arrows.remove(arrow)
        if not falling_arrows:
            arrow_rain_active = False
            competence = 0
    if len(grounded_arrows) > 50:
        grounded_arrows.pop(0)
    # screen.blit(font.render(f"{pygame.mouse.get_pos()[0]},{pygame.mouse.get_pos()[1]}", True, (255, 0, 0)), (0, 0))  # Affiche la position de la souris

    if shoot:
        time += 0.25
        for arrow in arrows_list:
            arrow_number = arrows_list.index(arrow)
            if arrow.y < 925 and -64 < arrow.x < 1952:
                position = arrow.arrow_path(initial_bow_x, initial_bow_y, arrow.power, arrow.angle, time)
                arrow_angle[f"arrow_angle_{arrow_number}"] = find_angle((arrow.x, arrow.y), (position[0], position[1]))
                if f"old_angle_{arrow_number}" in arrow_angle:
                    new_arrow_angle = (arrow_angle[f"arrow_angle_{arrow_number}"] + arrow_angle[f"old_angle_{arrow_number}"]) / 2
                arrow.x = position[0]
                arrow.y = position[1]
                arrow_angle[f"old_angle_{arrow_number}"] = arrow_angle[f"arrow_angle_{arrow_number}"]
                # Gère la rotation de la flèche
                arrow_angle[f"rotated_arrow_{arrow_number}"] = rot_center(arrow.image, new_arrow_angle - 45).convert_alpha()
                screen.blit(arrow_angle[f"rotated_arrow_{arrow_number}"], (arrow.x, arrow.y))

                # Gère la trainée de la flèche
                arrow.trainee.append([(235, 138, 126), (arrow.x + 32, arrow.y + 32)])
                if len(arrow.trainee) > 15:
                    arrow.trainee.pop(0)
            elif arrow.x >= 1952 or arrow.x <= -64:
                arrow.x = bow_x
                arrow.y = bow_y
                arrow.trainee = []
                shoot = False
            else:
                if not arrow_split_ability:
                    grounded_arrows.append([arrow_angle[f"rotated_arrow_{arrow_number}"], arrow.x, arrow.y])
                    shoot = False

                # SI la compétence "splitting arrows" est active, séparer les flèches en deux à l'impact
                if arrow_split_ability == 1:
                    arrows_list.append(Arrow(arrow.x, 925 - 10, pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), new_arrow_angle, arrow.power / 1.6))
                    arrow.y = 925 - 10
                    arrow.power /= 1.5
                    time = 0
                    initial_bow_x = arrow.x
                    initial_bow_y = arrow.y
                    angle = 360 - new_arrow_angle
                    arrow_split_ability += 1
                elif arrow_split_ability == 2:  # Une fois qu'une des flèches split touche le sol
                    fallen_arrow += 1
                    grounded_arrows.append([arrow_angle[f"rotated_arrow_{arrow_number}"], arrow.x, arrow.y])
                    arrows_list.remove(arrow)
                    arrow_split_ability = 0

                # Si la compétence "Arrow_rain" est active, dessiner une cible au sol et faire pleuvoir des flèches depuis le haut de l'écran
                if arrow_rain:
                    arrow_rain_init = True
                    ground_target = True
                    ground_x = arrow.x
                    ground_y = arrow.y + 32
                    width = 100
                    height = 50

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
            if not shoot and not competence:
                drawline = True
                initial_pos = pygame.mouse.get_pos()
                bow_pos_calc = True
                old_angle = 0

        if event.type == pygame.MOUSEBUTTONUP:
            if not shoot and drawline:
                drawline = False
                bow_image = bow_images[0]
                initial_bow_x = bow_x
                initial_bow_y = bow_y
                arrows_list[0].angle = find_angle(initial_pos, pos)
                shoot = True
                time = 0
                arrows_list[0].power = sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 6

    pygame.display.update()
