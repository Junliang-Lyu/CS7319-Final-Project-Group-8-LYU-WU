import sys
import pygame
from settings import (
    WIN, WIDTH, HEIGHT,
    TITLE_FONT, FONT, SMALL_FONT,
    WHITE, BLACK, BLUE, GREY
)

def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(WIN, GREY, rect)
    label = FONT.render(text, True, BLACK)
    WIN.blit(label, (x + 10, y + 10))
    return rect

def draw_scene(title, lines, bg):
    WIN.blit(bg, (0, 0))
    title_label = TITLE_FONT.render(title, True, BLUE)
    WIN.blit(title_label, (20, 20))
    y = 90
    for line in lines:
        lbl = FONT.render(line, True, BLACK)
        WIN.blit(lbl, (20, y))
        y += 40

def draw_inventory(player):
    text = "Items: "
    if player.items:
        text += ", ".join(player.items)
    else:
        text += "None"
    bar = pygame.Rect(0, HEIGHT - 50, WIDTH, 50)
    pygame.draw.rect(WIN, (230, 230, 230), bar)
    label = SMALL_FONT.render(text, True, BLACK)
    WIN.blit(label, (10, HEIGHT - 35))

def message_scene(msg):
    waiting = True
    while waiting:
        WIN.fill(WHITE)
        label = FONT.render(msg, True, BLACK)
        hint = SMALL_FONT.render("Click anywhere to continue.", True, BLUE)
        WIN.blit(label, (50, 220))
        WIN.blit(hint, (50, 280))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def password_input_scene(correct_code="9183"):
    code = ""
    running = True
    while running:
        WIN.fill(WHITE)
        title = TITLE_FONT.render("Enter 4-digit safe code", True, BLUE)
        WIN.blit(title, (140, 150))
        box = pygame.Rect(220, 240, 360, 60)
        pygame.draw.rect(WIN, GREY, box)
        text_surface = FONT.render(code, True, BLACK)
        WIN.blit(text_surface, (box.x + 10, box.y + 15))
        hint = SMALL_FONT.render("Digits only. Enter = OK, Esc = cancel.", True, BLACK)
        WIN.blit(hint, (170, 330))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return False
                elif e.key == pygame.K_RETURN:
                    if code == correct_code:
                        message_scene("Correct code.")
                        return True
                    else:
                        message_scene("Wrong code.")
                        return False
                elif e.key == pygame.K_BACKSPACE:
                    code = code[:-1]
                else:
                    if e.unicode.isdigit() and len(code) < 4:
                        code += e.unicode

def ending_scene():
    waiting = True
    while waiting:
        WIN.fill(WHITE)
        t1 = TITLE_FONT.render("YOU FOUND THE SMU TREASURE!", True, BLUE)
        t2 = FONT.render("The real treasure is knowledge.", True, BLACK)
        t3 = SMALL_FONT.render("Click anywhere to quit.", True, BLACK)
        WIN.blit(t1, (40, 200))
        WIN.blit(t2, (40, 260))
        WIN.blit(t3, (40, 310))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()
