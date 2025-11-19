import sys
import pygame
from settings import BG_JUNKINS
from player import player
from ui import draw_button, draw_scene, draw_inventory, message_scene

def junkins_scene():
    running = True
    while running:
        draw_scene("Junkins Building", [
            "You arrive at Junkins.",
            "Look around for clues."
        ], BG_JUNKINS)

        b1 = draw_button("Look at model", 60, 200, 320, 50)
        b2 = draw_button("Talk to worker", 60, 270, 380, 50)
        b3 = draw_button("Go to Library", 60, 340, 230, 50)
        b4 = draw_button("Check elevator", 420, 200, 300, 50)
        b5 = draw_button("Read notice", 420, 270, 300, 50)

        draw_inventory(player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(event.pos):
                    message_scene("A note says: treasure is in the place of knowledge.")
                if b2.collidepoint(event.pos):
                    if not player.got_key:
                        player.got_key = True
                        player.add_item("Locker key")
                        message_scene("The worker gives you a key.")
                    else:
                        message_scene("The worker already gave you the key.")
                if b3.collidepoint(event.pos):
                    if player.got_key:
                        return "library"
                    else:
                        message_scene("You may need something first.")
                if b4.collidepoint(event.pos):
                    player.add_item("Loose screw")
                    message_scene("You find a loose screw.")
                if b5.collidepoint(event.pos):
                    message_scene("The notice talks about exams.")
