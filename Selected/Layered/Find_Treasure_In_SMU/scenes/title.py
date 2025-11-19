import sys
import pygame
from settings import WIN, WHITE, BLUE, BG_TITLE, TITLE_FONT, FONT
from ui import draw_button

def title_scene():
    running = True
    while running:
        WIN.blit(BG_TITLE, (0, 0))
        t1 = TITLE_FONT.render("Find Treasure in SMU", True, BLUE)
        t2 = FONT.render("Click START to begin.", True, (0, 0, 0))
        WIN.blit(t1, (140, 150))
        WIN.blit(t2, (150, 210))
        start_btn = draw_button("START", 280, 300, 240, 60)
        quit_btn = draw_button("QUIT", 280, 380, 240, 60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return "caruth"
                if quit_btn.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
