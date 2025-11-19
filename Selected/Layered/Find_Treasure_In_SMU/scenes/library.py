import sys
import pygame
from settings import BG_LIBRARY
from player import player
from ui import draw_button, draw_scene, draw_inventory, message_scene, password_input_scene, ending_scene

def library_scene():
    running = True
    while running:
        draw_scene("Library", [
            "You arrive at the library.",
            "There is a locker with a safe inside."
        ], BG_LIBRARY)

        b1 = draw_button("Open safe", 60, 260, 220, 50)

        draw_inventory(player)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(event.pos):
                    if not player.got_key:
                        message_scene("The locker is locked.")
                    elif not player.saw_poster:
                        message_scene("You do not know the code.")
                    else:
                        ok = password_input_scene()
                        if ok:
                            ending_scene()
                            return "end"
