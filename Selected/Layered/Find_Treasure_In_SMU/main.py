from scenes.title import title_scene
from scenes.caruth import caruth_scene
from scenes.junkins import junkins_scene
from scenes.library import library_scene
import pygame
import sys

current = "title"

while True:
    if current == "title":
        current = title_scene()
    elif current == "caruth":
        current = caruth_scene()
    elif current == "junkins":
        current = junkins_scene()
    elif current == "library":
        current = library_scene()
    else:
        break

pygame.quit()
sys.exit()
