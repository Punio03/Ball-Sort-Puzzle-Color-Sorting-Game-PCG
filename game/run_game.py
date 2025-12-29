import pygame
import sys

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puste Okno Pygame")

# Kolory
WHITE = (255, 255, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Główna pętla gry
running = True
while running:
    clock.tick(FPS)

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rysowanie (czyszczenie ekranu)
    SCREEN.fill(WHITE)

    # Odświeżenie ekranu
    pygame.display.flip()

# Zakończenie Pygame
pygame.quit()
sys.exit()
