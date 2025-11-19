import sys
import pygame
from settings import BG_CARUTH
from player import player
from ui import draw_button, draw_scene, draw_inventory, message_scene

def caruth_scene():
    running = True
    while running:
        draw_scene("Caruth Hall", [
            "You arrive at Caruth Hall.",
            "You heard there may be a treasure."
        ], BG_CARUTH)

        b1 = draw_button("Enter classroom", 60, 200, 250, 50)
        b2 = draw_button("Check bulletin board", 60, 270, 300, 50)
        b3 = draw_button("Go to Junkins Building", 60, 340, 330, 50)
        b4 = draw_button("Look at vending machine", 420, 200, 320, 50)
        b5 = draw_button("Look out the window", 420, 270, 320, 50)

        draw_inventory(player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(event.pos):
                    if not player.talked_professor:
                        player.talked_professor = True
                        player.add_item("Professor hint")
                        message_scene("Professor suggests checking Junkins.")
                    else:
                        message_scene("The professor repeats the hint.")
                if b2.collidepoint(event.pos):
                    if not player.saw_poster:
                        player.saw_poster = True
                        player.add_item("Safe code note")
                        message_scene("The board shows code 9183.")
                    else:
                        message_scene("You already know the code.")
                if b3.collidepoint(event.pos):
                    if player.talked_professor:
                        return "junkins"
                    else:
                        message_scene("You feel unsure about going there.")
                if b4.collidepoint(event.pos):
                    player.add_item("Snack wrapper")
                    message_scene("You find an empty wrapper.")
                if b5.collidepoint(event.pos):
                    message_scene("You look outside the window.")
