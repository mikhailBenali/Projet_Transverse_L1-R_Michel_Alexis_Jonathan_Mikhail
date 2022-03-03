import pygame

# Initialisation
pygame.init()

# Initialisation de la fenêtre
screen = pygame.display.set_mode((1920, 1080))  # Attention à bien rentrer un tuple

# Initialisaiton de l'icône et du titre
pygame.display.set_caption("Pana pua")
icone = pygame.image.load("fleche.jpg")
pygame.display.set_icon(icone)

tour_image = pygame.image.load("tour.png")
tour_x = 50
largeur_tour = 201

taille_tour = 256
tour_y = 1080 - taille_tour


def tour(x, y):
    screen.blit(tour_image, (x, y))


# Variable de conditionnement, pour arrêter le programme on passera cette variable à false
running = True

while running:

    # Mise du background en violet (RGB)
    screen.fill((125, 0, 175))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    tour(tour_x, tour_y)

    pygame.display.update()
