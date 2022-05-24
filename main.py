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

background_image = pygame.image.load("Images/background.jpg").convert()
background_x = 0
background_x_change = 0

clock = pygame.time.Clock()

drawline = False

barre_de_vie_image = pygame.image.load("Images/barre_de_vie.png").convert_alpha()
barre_de_vie_image = pygame.transform.scale(barre_de_vie_image, (508, 48))

# Création du château

chateau_x = 50
chateau_y = 355
largeur_chateau = 512
taille_chateau = 600


# Boutons

class Bouton:
    def __init__(self, nom_bouton, coordonnees, taille_resize):
        self.images = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Boutons/{nom_bouton}*png")]
        self.x = coordonnees[0]
        self.y = coordonnees[1]
        self.largeur = taille_resize[0]
        self.hauteur = taille_resize[1]
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.scale(self.images[i], (self.largeur, self.hauteur))
        self.rect = [image.get_rect(topleft=(self.x, self.y)) for image in self.images]
        self.pointe = False

    def afficher(self):
        if self.rect[0].x < pygame.mouse.get_pos()[0] < self.rect[0].x + self.largeur and self.rect[0].y < pygame.mouse.get_pos()[1] < self.rect[0].y + self.hauteur:  # Si le bouton est pointé
            screen.blit(self.images[0], (self.rect[0].x, self.rect[0].y))
            self.pointe = True
        else:
            screen.blit(self.images[1], (self.rect[0].x, self.rect[0].y))
            self.pointe = False


boutons_play = Bouton("Bouton_play", (842, 512), (236, 56))  # 118x28 (118x24) sans les pixels transparents
boutons_pause = Bouton("Bouton_rond_pause", (1864, 0), (56, 56))  # 28x28
boutons_resume = Bouton("Bouton_resume", (842, 300), (236, 56))  # 118x28
boutons_quit = Bouton("Bouton_quit", (1684, 1024), (236, 56))  # 118x28
boutons_play_again = Bouton("Bouton_play_again", (842, 512), (236, 56))  # 118x28
boutons_competence_1 = Bouton("Bouton_comp_1", (525, 500), (256, 256))
boutons_competence_2 = Bouton("Bouton_comp_2", (825, 500), (256, 256))
boutons_competence_3 = Bouton("Bouton_comp_3", (1125, 500), (256, 256))


class Chateau:
    def __init__(self):
        self.vie_max = 1000
        self.vie = self.vie_max

        # Images

        self.images_full_hp = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Chateau/schato_drapeau*.png")]  # Chargement des images
        for i in range(len(self.images_full_hp)):
            self.images_full_hp[i] = pygame.transform.scale(self.images_full_hp[i], (512, 600))  # Agrandissement

        self.images_75_hp = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Chateau/schato_destr_25*.png")]
        for i in range(len(self.images_75_hp)):
            self.images_75_hp[i] = pygame.transform.scale(self.images_75_hp[i], (512, 600))

        self.images_50_hp = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Chateau/schato_destr_50*.png")]
        for i in range(len(self.images_50_hp)):
            self.images_50_hp[i] = pygame.transform.scale(self.images_50_hp[i], (512, 600))

        self.images_25_hp = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Chateau/schato_destr_75*.png")]
        for i in range(len(self.images_25_hp)):
            self.images_25_hp[i] = pygame.transform.scale(self.images_25_hp[i], (512, 600))

        self.images_destruction = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Fumee/*.png")]
        for i in range(len(self.images_destruction)):
            self.images_destruction[i] = pygame.transform.scale(self.images_destruction[i], (512, 600))

        self.detruit = False

        self.frame = 0
        self.rect = pygame.Rect(chateau_x, chateau_y, largeur_chateau, taille_chateau)
        self.temps_derniere_frame = 0

    def afficher(self):
        if self.vie > 75 / 100 * self.vie_max:
            if tm.time() > self.temps_derniere_frame + 1:
                if self.frame + 1 < len(self.images_full_hp):
                    screen.blit(self.images_full_hp[self.frame], (chateau_x, chateau_y))
                    self.temps_derniere_frame = tm.time()
                    self.frame += 1
                else:
                    screen.blit(self.images_full_hp[self.frame], (chateau_x, chateau_y))
                    self.frame = 0
            else:
                screen.blit(self.images_full_hp[self.frame], (chateau_x, chateau_y))
        elif self.vie > 50 / 100 * self.vie_max:
            if tm.time() > self.temps_derniere_frame + 1:
                if self.frame + 1 < len(self.images_75_hp):
                    screen.blit(self.images_75_hp[self.frame], (chateau_x, chateau_y))
                    self.temps_derniere_frame = tm.time()
                    self.frame += 1
                else:
                    screen.blit(self.images_75_hp[self.frame], (chateau_x, chateau_y))
                    self.frame = 0
            else:
                screen.blit(self.images_75_hp[self.frame], (chateau_x, chateau_y))
        elif self.vie > 25 / 100 * self.vie_max:
            if tm.time() > self.temps_derniere_frame + 1:
                if self.frame + 1 < len(self.images_50_hp):
                    screen.blit(self.images_50_hp[self.frame], (chateau_x, chateau_y))
                    self.temps_derniere_frame = tm.time()
                    self.frame += 1
                else:
                    screen.blit(self.images_50_hp[self.frame], (chateau_x, chateau_y))
                    self.frame = 0
            else:
                screen.blit(self.images_50_hp[self.frame], (chateau_x, chateau_y))
        elif self.vie > 0:
            if tm.time() > self.temps_derniere_frame + 1:
                if self.frame + 1 < len(self.images_25_hp):
                    screen.blit(self.images_25_hp[self.frame], (chateau_x, chateau_y))
                    self.temps_derniere_frame = tm.time()
                    self.frame += 1
                else:
                    screen.blit(self.images_25_hp[self.frame], (chateau_x, chateau_y))
                    self.frame = 0
            else:
                screen.blit(self.images_25_hp[self.frame], (chateau_x, chateau_y))

        else:
            self.destruction()

    def destruction(self):
        i = 0
        while i < len(self.images_destruction):
            if tm.time() > self.temps_derniere_frame + 0.2:
                self.temps_derniere_frame = tm.time()
                screen.blit(self.images_destruction[i], (chateau_x, chateau_y))
                pygame.display.update()
                i += 1
            else:
                screen.blit(self.images_destruction[i], (chateau_x, chateau_y))
        self.detruit = True

    def reset(self):
        self.vie = self.vie_max
        self.detruit = False


chateau = Chateau()


# Personnage
class Joueur:

    def __init__(self):
        self.images_droite = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??.png")]
        self.images_gauche = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/Persos/perso??_gauche.png")]
        self.orientation = "droite"  # Sert pour la direction de l'idle
        self.frame = 0
        self.temps_derniere_frame = 0
        self.rect = [self.images_droite[i].get_rect() for i in range(len(self.images_droite))] + [self.images_gauche[i].get_rect() for i in range(len(self.images_gauche))]  # Chaque image a son rectangle de collision

    def idle(self, x, y):
        if self.orientation == "droite":
            screen.blit(self.images_droite[0], (x, y))
        elif self.orientation == "gauche":
            screen.blit(self.images_gauche[0], (x, y))

    def mvt_droite(self, x, y):
        self.orientation = "droite"
        if tm.time() > self.temps_derniere_frame + 0.2:
            if self.frame + 1 >= len(self.images_droite):
                self.frame = 0
                self.mvt_droite(x, y)
            else:
                self.frame += 1
            screen.blit(self.images_droite[self.frame], (x, y))
            self.nouvelle_frame()

        else:
            screen.blit(self.images_droite[self.frame], (x, y))

    def mvt_gauche(self, x, y):
        self.orientation = "gauche"
        if tm.time() > self.temps_derniere_frame + 0.2:
            if self.frame + 1 >= len(self.images_gauche):
                self.frame = 0
                self.mvt_gauche(x, y)
            else:
                self.frame += 1
            screen.blit(self.images_gauche[self.frame], (x, y))
            self.nouvelle_frame()

        else:
            screen.blit(self.images_gauche[self.frame], (x, y))

    def nouvelle_frame(self):
        self.temps_derniere_frame = tm.time()

    def maj_rect(self, x, y):
        self.rect = [self.images_droite[i].get_rect(topleft=(x, y)) for i in range(len(self.images_droite))] + [self.images_gauche[i].get_rect(topleft=(x, y)) for i in range(len(self.images_gauche))]


perso = Joueur()
perso_x = chateau_x + 50
perso_x_deplacement = 0
perso_y = chateau_y + 225  # 825


class Sprite:
    def __init__(self, dossier):
        self.images = [pygame.image.load(f).convert_alpha() for f in glob(f"Images/{dossier}/*.png")]
        self.frame = 0
        self.temps_derniere_frame = 0
        self.rect = [self.images[i].get_rect() for i in range(len(self.images))]  # Chaque image a son rectangle de collision

    def afficher(self, x, y):
        if tm.time() > self.temps_derniere_frame + 0.05:
            if self.frame + 1 < len(self.images):  # S'il est possible de passer à la frame suivante
                screen.blit(self.images[self.frame], (x, y))
                self.frame += 1
                self.changer_frame()
            else:
                self.frame = 0
                self.afficher(x, y)
        else:
            screen.blit(self.images[self.frame], (x, y))

    def changer_frame(self):
        self.temps_derniere_frame = tm.time()

    def maj_rect(self, x, y):
        self.rect = [self.images[i].get_rect(topleft=(x + 50, y + 50), width=78, height=78) for i in range(len(self.images))]  # On réduit la taille du rect


slimes = [Sprite("slime") for i in range(5)]
random.seed(tm.time())
slimes_x_pos = [random.randint(1700, 2500) for slime in slimes]  # 1920, 2600
slimes_y = 825
for i in range(len(slimes)):  # Mettre à jour les rect des slimes une première fois
    slimes[i].maj_rect(slimes_x_pos[i], slimes_y)
slimes_x_deplacement = [random.choice([x / 10 for x in range(-40, -10)]) for slime in slimes]  # Pour avoir des vitesses entre -4.0 et -1.0

oiseaux = [Sprite("bird") for i in range(5)]
oiseaux_x_pos = [random.randint(1700, 2500) for oiseau in oiseaux]
oiseaux_y = [random.randint(600, 675) for oiseau in oiseaux]
for i in range(len(slimes)):
    oiseaux[i].maj_rect(oiseaux_x_pos[i], oiseaux_y[i])
oiseaux_x_deplacement = [random.choice([x / 10 for x in range(-60, -30)]) for oiseau in oiseaux]

experience = 0
experience_max = 100


class Arrow(object):
    def __init__(self, arrow_x, arrow_y, image, angle, power):
        self.x = arrow_x
        self.y = arrow_y
        self.image = image
        self.rect = image.get_rect()
        self.trainee = []
        self.angle = angle
        self.power = power
        self.rect = self.image.get_rect()

    def arrow_path(self, startx, starty, arrow_power, angle, arrow_time):
        velx = cos(radians(angle)) * -arrow_power  # velocity
        vely = sin(radians(angle)) * -arrow_power

        distx = velx * time  # distance
        disty = (vely * time) + ((-4.9 * arrow_time ** 2) / 2)  # 4.9 = gravité

        newx = round(distx + startx)
        newy = round(starty - disty)

        return newx, newy

    def maj_rect(self, x, y):
        self.rect = self.image.get_rect(topleft=(x, y))


class Particle:
    def __init__(self, radius):
        self.radius = random.randint(radius - 10, radius)
        self.max_radius = radius
        self.angle = random.randint(0, 360)
        self.size = random.randint(10, 13)
        self.x = bow_x + 26 + radius * cos(self.angle)
        self.y = bow_y + 26 + radius * sin(self.angle)

    def generate_x_y(self, radius, angle):
        self.x = bow_x + 26 + radius * cos(angle)
        self.y = bow_y + 26 + radius * sin(angle)


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
    for arrow in arrows_list:
        if grounded_arrows:
            for img in grounded_arrows:
                screen.blit(img[0], (img[1], img[2]))
        if arrow.trainee:
            if charge_complete:
                size = 10
                for trainee in arrow.trainee:
                    screen.fill(trainee[0], (trainee[1], (size, size)))
            else:
                size = 1
                for trainee in arrow.trainee:
                    screen.fill(trainee[0], (trainee[1], (size, size)))
                    size += 0.5

    font = pygame.font.Font("freesansbold.ttf", 40)
    screen.blit(font.render(f"xp:", True, (0, 0, 0)), (780, 5))
    if competence_point:
        font = pygame.font.Font("freesansbold.ttf", 30)
        screen.blit(font.render(f"+ {competence_point} pt de compétence à dépenser", True, (200, 0, 0)), (780, 50))

    # Creation de la cible pour la compétence "Arrow rain"

    if drawline:
        angle = find_angle(initial_pos, pos)
        pygame.draw.line(screen, (64, 64, 64), line[0], line[1])
        bowImg = rot_center(pygame.transform.rotate(bow_image, 180), angle - 45)
    else:
        angle = find_angle([bow_x, bow_y], pos)
        bowImg = rot_center(pygame.transform.rotate(bow_image, 180), angle - 225)

    pygame.draw.line(screen, (0, 150, 0), (chateau_x, 1000), (chateau_x + chateau.vie / 2, 1000), 25)

    # Affichage de la tour
    chateau.afficher()

    # animation d'ouverture du parchemin de competences
    screen.blit(debut_barre_competence, (5, 5))
    fin_barre = 5
    i = -1
    for i in range(len(active_competences)):
        for j in range(len(barre_competence)):
            screen.blit(barre_competence[i], (33 + 84 * i, 5))
        screen.blit(competences_images[active_competences[i]], (37 + 84 * i, 41))
    screen.blit(fin_barre_competence, (21 + 84 * (i + 1), 5))

    for i in range(len(slimes)):
        slimes[i].afficher(slimes_x_pos[i], slimes_y)

    for i in range(len(oiseaux)):
        oiseaux[i].afficher(oiseaux_x_pos[i], oiseaux_y[i])

    # Affichage personnage
    if movement == "Droite" and perso_x_deplacement != 0:
        perso.mvt_droite(perso_x, perso_y)
    elif movement == "Gauche" and perso_x_deplacement != 0:
        perso.mvt_gauche(perso_x, perso_y)
    if perso_x_deplacement == 0:
        perso.idle(perso_x, perso_y)

    # Affichage arc
    screen.blit(bowImg, (bow_x, bow_y))
    perso_x += perso_x_deplacement
    bow_x = perso_x + 40
    clock.tick(60)

    screen.blit(barre_de_vie_image, (chateau_x, 975))


bow_x = perso_x + 40
bow_y = perso_y + 50
bow_images = [pygame.image.load(f).convert_alpha() for f in glob("Images/Arc/arc-?.png")]
bow_image = bow_images[0]
# [pygame.image.load(f).convert_alpha() for f in glob("Images/aptitude_bar/parchemin_?.png")]
arrows_list = [Arrow(bow_x, bow_y, pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), 0, 0)]
competences_images = [pygame.image.load(f).convert_alpha() for f in glob("Images/aptitude_bar/competence_?.png")]
debut_barre_competence = pygame.image.load("Images/aptitude_bar/debut_parchemin.png").convert_alpha()
barre_competence = [pygame.image.load(f).convert_alpha() for f in glob("Images/aptitude_bar/parchemin_infini_?.png")]
fin_barre_competence = pygame.image.load("Images/aptitude_bar/fin_parchemin.png").convert_alpha()
Titre_image = pygame.transform.scale(pygame.image.load("Images/Titre.png").convert_alpha(), (800, 200))
power = 0
competence_point = 0
arrow_angle = {}
new_arrow_angle = 0
fallen_arrow = 0
shoot = False
debut = True
level_up = 0
outline_size = 10
grounded_arrows = []
competence_active = 0
active_competences = []
arrow_split_ability = 0
arrow_rain = 0
arrow_rain_level = 0
laser_arrow = 0
arrow_rain_active = 0
arrow_rain_init = 0
laser_arrow_init = 0
ground_target = False
charge_complete = False
arrow_trainee_rects = []
particle_dispertion = 0
hit = False
laser = False
max_xp = 10
level_up = 1
MAXED = []

# Variable de conditionnement : pour arrêter le programme on passera cette variable à false
running = True

movement = False

jeu_lance = False
jeu_pause = False

while running:
    if jeu_lance and not jeu_pause:  # Si le jeu est en cours
        if not chateau.detruit:
            pos = pygame.mouse.get_pos()
            if drawline:
                line = [initial_pos, pos]
                distance = sqrt((initial_pos[0] - pos[0]) ** 2 + (initial_pos[1] - pos[1]) ** 2)

                # Gère le bandage de l'arc
                if 0 <= distance < 250:
                    bow_image = bow_images[0]
                elif 250 <= distance < 500:
                    bow_image = bow_images[1]
                elif 500 <= distance < 750:
                    bow_image = bow_images[2]
                elif 750 <= distance:
                    bow_image = bow_images[3]
            redraw()

            # Barre d'xp
            if experience >= max_xp:
                experience = 0
                max_xp += 5
                competence_point += 1
            pygame.draw.line(screen, (0, 100, 0), (850, 25), (850 + experience * (200/max_xp), 25), 20)
            pygame.draw.rect(screen, (0, 0, 0), ((850, 12), (200, 27)), 5)

            if laser_arrow_init:
                for particle in charging_particles:
                    screen.fill((255, 0, 0), ((particle.x, particle.y), (particle.size, particle.size)))
                    particle.radius -= 3
                    particle.size -= 0.5
                    particle.generate_x_y(particle.radius, particle.angle)
                    if particle.size == 0 or particle.radius < 0:
                        if particle.max_radius > 13:
                            particle.max_radius -= 3
                        else:
                            charge_complete = True
                        charging_particles[charging_particles.index(particle)] = Particle(particle.max_radius)
            if particle_dispertion:
                for particle in charging_particles:
                    screen.fill((255, 0, 0), ((particle.x, particle.y), (particle.size, particle.size)))
                    particle.radius += 3
                    particle.size -= 0.3
                    particle.generate_x_y(particle.radius, particle.angle)

            if arrow_rain_init:
                competence_active = 1
                arrow_rain_number = random.randint(arrow_rain_level, arrow_rain_level+5)
                falling_arrows = []
                for i in range(arrow_rain_number):
                    falling_arrows.append(Arrow(ground_x - 2 * random.randint(50, 400), -random.randint(80, 1000), rot_center(pygame.image.load("Images/Arc/phlaitche-1.png"), 250).convert_alpha(), 0, 100))
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

                    for falling_arrow in falling_arrows:
                        falling_arrow.maj_rect(falling_arrow.x, falling_arrow.y)

                    slimes_a_supprimer = -1
                    oiseaux_a_supprimer = -1

                    for i in range(len(slimes)):
                        for falling_arrow in falling_arrows:
                            if pygame.Rect.colliderect(falling_arrow.rect, slimes[i].rect[slimes[i].frame]):
                                slimes_a_supprimer = i
                    for i in range(len(oiseaux)):
                        for falling_arrow in falling_arrows:
                            if pygame.Rect.colliderect(falling_arrow.rect, oiseaux[i].rect[oiseaux[i].frame]):
                                oiseaux_a_supprimer = i

                    if slimes_a_supprimer != -1:  # S'il y a au moins un slime à supprimer
                        del slimes[slimes_a_supprimer]  # On supprime le slime correspondant
                        del slimes_x_pos[slimes_a_supprimer]  # Ainsi que sa position (sinon tous les slimes se décalent)
                        slimes_a_supprimer = -1
                        slimes.append(Sprite("slime"))
                        slimes_x_pos.append(random.randint(1700, 2500))
                        slimes[len(slimes) - 1].maj_rect(slimes_x_pos[i], slimes_y)
                        slimes_x_deplacement[len(slimes_x_deplacement) - 1] = random.choice([x / 10 for x in range(-60, -30)])

                        experience += 1
                        slimes_a_supprimer = -1

                    if oiseaux_a_supprimer != -1:  # S'il y a au moins un slime à supprimer
                        del oiseaux[oiseaux_a_supprimer]  # On supprime le slime correspondant
                        del oiseaux_x_pos[oiseaux_a_supprimer]  # Ainsi que sa position (sinon tous les slimes se décalent)
                        oiseaux_a_supprimer = -1
                        oiseaux.append(Sprite("bird"))
                        oiseaux_x_pos.append(random.randint(1700, 2500))
                        oiseaux[len(slimes) - 1].maj_rect(oiseaux_x_pos[i], oiseaux_y[i])
                        oiseaux_x_deplacement[len(oiseaux_x_deplacement) - 1] = random.choice([x / 10 for x in range(-60, -30)])

                        experience += 1
                        oiseaux_a_supprimer = -1

                if not falling_arrows:
                    arrow_rain_active = False
                    arrow_rain = 0
                    competence_active = 0

            if len(grounded_arrows) > 50:
                grounded_arrows.pop(0)

            if shoot:
                time += 0.25
                hit = False
                for arrow in arrows_list:
                    arrow_number = arrows_list.index(arrow)
                    # Collisions avec les slimes

                    slimes_a_supprimer = -1

                    # Suppression des slimes

                    for i in range(len(slimes)):
                        if pygame.Rect.colliderect(arrow.rect, slimes[i].rect[slimes[i].frame]):
                            slimes_a_supprimer = i  # On garde l'indice du slime à supprimer
                        elif arrow_trainee_rects:
                            for particle in arrow_trainee_rects:
                                if pygame.Rect.colliderect(particle, slimes[i].rect[slimes[i].frame]):
                                    slimes_a_supprimer = i
                                    arrow_trainee_rects.remove(particle)

                    if slimes_a_supprimer != -1:  # S'il y a au moins un slime à supprimer
                        hit = True  # On arrête les calculs de tir (trajectoires etc...)
                        shoot = False
                        del slimes[slimes_a_supprimer]  # On supprime le slime correspondant
                        del slimes_x_pos[slimes_a_supprimer]  # Ainsi que sa position (sinon tous les slimes se décalent)
                        # On rajoute un slime à la fin
                        slimes.append(Sprite("slime"))
                        slimes_x_pos.append(random.randint(1700, 2500))
                        slimes[len(slimes) - 1].maj_rect(slimes_x_pos[i], slimes_y)
                        slimes_x_deplacement[len(slimes_x_deplacement) - 1] = random.choice([x / 10 for x in range(-60, -30)])

                        experience += 1
                        slimes_a_supprimer = -1

                    oiseaux_a_supprimer = -1

                    # Suppression des oiseaux

                    for i in range(len(oiseaux)):
                        if pygame.Rect.colliderect(arrow.rect, oiseaux[i].rect[oiseaux[i].frame]):
                            oiseaux_a_supprimer = i
                        elif arrow_trainee_rects:
                            for particle in arrow_trainee_rects:
                                if pygame.Rect.colliderect(particle, oiseaux[i].rect[oiseaux[i].frame]):
                                    oiseaux_a_supprimer = i
                                    arrow_trainee_rects.remove(particle)

                    if oiseaux_a_supprimer != -1:
                        hit = True
                        shoot = False
                        del oiseaux[oiseaux_a_supprimer]
                        del oiseaux_x_pos[oiseaux_a_supprimer]
                        # On rajoute un oiseau à la fin
                        oiseaux.append(Sprite("bird"))
                        oiseaux_x_pos.append(random.randint(1700, 2500))
                        oiseaux[len(slimes) - 1].maj_rect(oiseaux_x_pos[i], oiseaux_y[i])
                        oiseaux_x_deplacement[len(oiseaux_x_deplacement) - 1] = random.choice([x / 10 for x in range(-60, -30)])

                        experience += 1
                        oiseaux_a_supprimer = -1

                    if -500 < arrow.y < 925 and -64 < arrow.x < 1952 and not hit:
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
                        if charge_complete:
                            separation_x = (arrow.x - old_arrow[0]) / 100
                            separation_y = (arrow.y - old_arrow[1]) / 100
                            for i in range(1, 100):
                                arrow.trainee.append([(200, 0, 0), (arrow.x + 32 + separation_x * i, arrow.y + 32 + separation_y * i)])
                                arrow_trainee_rects.append(pygame.Rect((arrow.x + 32 + separation_x * i, arrow.y + 32 + separation_y * i), (arrow.x + 42 + separation_x * i, arrow.y + 42 + separation_y * i)))
                                if len(arrow.trainee) > 200:
                                    arrow.trainee.pop(0)
                            old_arrow = [arrow.x, arrow.y]
                        else:
                            arrow.trainee.append([(235, 138, 126), (arrow.x + 32, arrow.y + 32)])
                            if len(arrow.trainee) > 15:
                                arrow.trainee.pop(0)
                    elif arrow.x >= 1952 or arrow.x <= -64 or arrow.y < -500 or arrow.y > 940:
                        if not arrow_split_ability == 2:
                            arrow_trainee_rects = []
                            charge_complete = False
                            laser = False
                            arrow.x = bow_x
                            arrow.y = bow_y
                            arrow.trainee = []
                            shoot = False
                    else:
                        if not arrow_split_ability and not hit:
                            grounded_arrows.append([arrow_angle[f"rotated_arrow_{arrow_number}"], arrow.x, arrow.y])
                            shoot = False

                        # SI la compétence "splitting arrows" est active, séparer les flèches en deux à l'impact
                        if arrow_split_ability == 1:
                            shoot = True
                            hit = False
                            arrows_list.append(Arrow(arrow.x, 925 - 10, pygame.image.load("Images/Arc/phlaitche-1.png").convert_alpha(), new_arrow_angle, arrow.power / 1.6))
                            arrow.y = arrow.y - 20
                            arrow.power /= 1.5
                            time = 0
                            initial_bow_x = arrow.x
                            initial_bow_y = arrow.y
                            angle = 360 - new_arrow_angle
                            arrow_split_ability += 1
                        elif arrow_split_ability == 2:  # Une fois qu'une des flèches split touche le sol
                            shoot = True
                            fallen_arrow += 1
                            if not hit:
                                grounded_arrows.append([arrow_angle[f"rotated_arrow_{arrow_number}"], arrow.x, arrow.y])
                            arrows_list.remove(arrow)
                            arrow_split_ability = 0

                        # Si la compétence "Arrow rain" est active, dessiner une cible au sol et faire pleuvoir des flèches depuis le haut de l'écran
                        if arrow_rain:
                            arrow_rain_init = True
                            ground_x = arrow.x
                            ground_y = arrow.y + 32
                            width = 100
                            height = 50

                        if laser:
                            shoot = True
                        else:
                            arrow.x = bow_x
                            arrow.y = bow_y
                            arrow.trainee = []

                    arrow.maj_rect(arrow.x, arrow.y)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_SPACE:
                        if perso_y == chateau_y + 225:
                            perso_y = 825
                        else:
                            perso_y = chateau_y + 225
                        bow_y = perso_y + 50

                    if event.key == pygame.K_d and perso_x + 100 < chateau_x + largeur_chateau:  # On ne peut pas démarrer un déplacement au bord du château vers l'extérieur
                        movement = "Droite"
                        perso_x_deplacement = 7.5
                        bow_y = perso_y + 50
                    if event.key == pygame.K_q and perso_x > chateau_x:
                        movement = "Gauche"
                        perso_x_deplacement = -7.5
                        bow_y = perso_y + 50

                    if not shoot:
                        if event.key == pygame.K_1 and 0 in active_competences:
                            arrow_rain, laser_arrow = 0, 0
                            arrow_split_ability = 1
                        if event.key == pygame.K_2 and 1 in active_competences:
                            arrow_split_ability, laser_arrow = 0, 0
                            arrow_rain = 1
                        if event.key == pygame.K_3 and 2 in active_competences:
                            arrow_split_ability, arrow_rain = 0, 0
                            laser_arrow = 1
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_q:
                        perso_x_deplacement = 0

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if boutons_pause.pointe:
                        jeu_pause = True
                    elif boutons_quit.pointe:
                        running = False

                    if not shoot and not competence_active and not jeu_pause:
                        charge_complete = False
                        drawline = True
                        initial_pos = pygame.mouse.get_pos()

                        # Si la compétence "Laser arrow" est active, tirer une flèche enn ligne droite avec une trainée rouge qui traverse les ennemis
                        if laser_arrow:
                            laser_arrow_init = 1
                            particle_dispertion = False
                            max_radius = 60
                            charging_particles = []
                            for i in range(50):
                                charging_particles.append(Particle(max_radius))
                            laser_arrow = 0

                if event.type == pygame.MOUSEBUTTONUP:
                    if not shoot and drawline:
                        drawline = False
                        bow_image = bow_images[0]
                        initial_bow_x = bow_x
                        initial_bow_y = bow_y
                        arrows_list[0].angle = find_angle(initial_pos, pos)
                        shoot = True
                        time = 0

                        if laser_arrow_init:
                            if charge_complete:
                                old_arrow = [initial_bow_x, initial_bow_y]
                                arrows_list[0].power = 500
                                charging_particles = []
                                laser = True
                            else:
                                arrows_list[0].power = (sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 6)
                                for i in range(50):
                                    charging_particles[i] = (Particle(max_radius))
                                particle_dispertion = 1
                            laser_arrow_init = 0
                        else:
                            arrows_list[0].power = (sqrt((line[1][1] - line[0][1]) ** 2 + (line[1][0] - line[0][0]) ** 2) / 6)

            if laser_arrow_init:
                movement = ""
                perso_x_deplacement = 0

            if chateau.vie < 25 / 100 * chateau.vie_max:
                perso_y = 825
                bow_y = perso_y + 50

            if perso_x > chateau_x + largeur_chateau - 175:  # Replacer le perso s'il sort
                perso_x_deplacement = 0
                perso_x = chateau_x + largeur_chateau - 175
            if perso_x < chateau_x + 50:
                perso_x_deplacement = 0
                perso_x = chateau_x + 50

            for i in range(len(slimes)):
                slimes_x_pos[i] += slimes_x_deplacement[i]
                slimes[i].maj_rect(slimes_x_pos[i], slimes_y)  # Mettre à jour les rect des slimes
                if pygame.Rect.colliderect(chateau.rect, slimes[i].rect[slimes[i].frame]):  # Faire se déplacer les ennemis à droite quand ils touchent le château
                    slimes_x_pos[i] += 100
                    chateau.vie -= 10

            for i in range(len(oiseaux)):
                oiseaux_x_pos[i] += oiseaux_x_deplacement[i]
                oiseaux[i].maj_rect(oiseaux_x_pos[i], oiseaux_y[i])  # Mettre à jour les rect des slimes
                if pygame.Rect.colliderect(chateau.rect, oiseaux[i].rect[oiseaux[i].frame]):  # Faire se déplacer les ennemis à droite quand ils touchent le château
                    oiseaux_x_pos[i] += 100
                    chateau.vie -= 10

            if chateau.vie <= 0:
                shoot = False
                Arrow.trainee = []
                slimes_x_deplacement = [x_deplacement for x_deplacement in slimes_x_deplacement]
                oiseaux_x_deplacement = [x_deplacement for x_deplacement in oiseaux_x_deplacement]
                chateau.destruction()
                slimes = []
                oiseaux = []

            if experience > experience_max:  # Limite d'XP
                experience = experience_max

            boutons_pause.afficher()
            boutons_quit.afficher()

        else:
            screen.blit(background_image, (background_x, 0))
            font = pygame.font.Font("freesansbold.ttf", 64)
            screen.blit(font.render(f"Vous avez perdu...", True, (255, 255, 255)), (boutons_play_again.x - 150, 350))

            boutons_play_again.afficher()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and boutons_play_again.pointe:
                    chateau.vie = chateau.vie_max
                    chateau.detruit = False
                    competence_point = 0
                    competence_active = []
                    experience = 0
                    MAXED = []
                    perso_x = chateau_x + 50
                    perso_y = chateau_y + 225  # 825
                    bow_x = perso_x + 40
                    bow_y = perso_y + 50

                    # Recréation des ennemis

                    slimes = [Sprite("slime") for i in range(5)]
                    random.seed(tm.time())
                    slimes_x_pos = [random.randint(1700, 2500) for slime in slimes]  # 1920, 2600
                    slimes_y = 825
                    for i in range(len(slimes)):  # Mettre à jour les rect des slimes une première fois
                        slimes[i].maj_rect(slimes_x_pos[i], slimes_y)
                    slimes_x_deplacement = [random.choice([x / 10 for x in range(-40, -10)]) for slime in slimes]  # Pour avoir des vitesses entre -4.0 et -1.0

                    oiseaux = [Sprite("bird") for i in range(5)]
                    oiseaux_x_pos = [random.randint(1700, 2500) for oiseau in oiseaux]
                    oiseaux_y = [random.randint(600, 675) for oiseau in oiseaux]
                    for i in range(len(slimes)):
                        oiseaux[i].maj_rect(oiseaux_x_pos[i], oiseaux_y[i])
                    oiseaux_x_deplacement = [random.choice([x / 10 for x in range(-60, -30)]) for oiseau in oiseaux]

                    grounded_arrows = []

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

    elif jeu_lance and jeu_pause:
        font = pygame.font.Font("freesansbold.ttf", 35,)
        screen.blit(background_image, (background_x, 0))
        screen.blit(font.render(f"{competence_point} points restant à dépenser", True, (0, 200, 0)), (boutons_competence_1.x + 200, 400))
        screen.blit(font.render(f"Splitting arrow", True, (255, 255, 255)), (boutons_competence_1.x, 756))
        boutons_competence_1.afficher()
        screen.blit(font.render(f"Raining arrows", True, (255, 255, 255)), (boutons_competence_2.x, 756))
        boutons_competence_2.afficher()
        screen.blit(font.render(f"Laser arrow", True, (255, 255, 255)), (boutons_competence_3.x + 30, 756))
        boutons_competence_3.afficher()
        boutons_resume.afficher()
        for value in MAXED:
            font = pygame.font.Font("freesansbold.ttf", 80)
            screen.blit(font.render(f"M A X", True, (200, 0, 0)), ( 525 + 10 + value*300, 628))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boutons_resume.pointe:
                    jeu_pause = False

                elif boutons_competence_1.pointe and competence_point:
                    if not 0 in active_competences:
                        active_competences.append(0)
                        competence_point -= 1
                        MAXED.append(0)

                elif boutons_competence_2.pointe and competence_point > 0:
                    if not 1 in active_competences and arrow_rain_level == 0:
                        active_competences.append(1)
                        arrow_rain_level += 5
                        competence_point -= 1
                    elif arrow_rain_level < 30:
                        arrow_rain_level += 5
                        competence_point -= 1
                    else:
                        arrow_rain_level += 5
                        MAXED.append(1)

                elif boutons_competence_3.pointe and competence_point > 0:
                    if not 2 in active_competences:
                        active_competences.append(2)
                        competence_point -= 1
                        MAXED.append(2)



            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jeu_pause = False

    else:
        screen.blit(background_image, (background_x, 0))
        screen.blit(Titre_image, (boutons_play.x - 250, 300))
        boutons_play.afficher()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and boutons_play.pointe:
                jeu_lance = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.display.update()
