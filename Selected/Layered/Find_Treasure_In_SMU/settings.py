import os
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find Treasure in SMU")

TITLE_FONT = pygame.font.SysFont("Arial", 40)
FONT = pygame.font.SysFont("Arial", 28)
SMALL_FONT = pygame.font.SysFont("Arial", 22)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (80, 80, 200)
GREY = (200, 200, 200)

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def load_bg(name):
    path = os.path.join(ASSETS_DIR, name)
    img = pygame.image.load(path).convert()
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))
    return img

BG_TITLE = load_bg("title_bg.png")
BG_CARUTH = load_bg("caruth_bg.png")
BG_JUNKINS = load_bg("junkins_bg.png")
BG_LIBRARY = load_bg("library_bg.png")
