
#PLACEHOLDER UNTIL I DECIDE TO CHANGE
import pygame
pygame.init()

font = pygame.font.Font("Contents/Typeface/soddy.otf", 15)
font_mini = pygame.font.Font("Contents/Typeface/soddy.otf", 10)
font_sized = pygame.font.Font("Contents/Typeface/soddy.otf", 12)
font_big = pygame.font.Font("Contents/Typeface/soddy.otf", 22)
font_biggest = pygame.font.Font("Contents/Typeface/soddy.otf", 30)
font_fredoka = pygame.font.Font("Contents/Typeface/fredoka.ttf", 10)

start_hint_x, start_key_x, intro_fade, intro_slide = 105, 90, 255, False

def Intro(display_screen, tick, top_barrier, bottom_barrier, intro_fade):
    global start_hint_x, start_key_x
    
    start_hint = font_biggest.render("Press", False, (255, 255, 255))
    start_key = font_big.render("E to Start", False, (255, 255, 255))

    if intro_slide:
        start_hint_x += 5
        start_key_x -= 5

        if top_barrier.y >= 80:
            top_barrier.y -= 1
        if bottom_barrier.y <= 220:
            bottom_barrier.y += 1
        if intro_fade > 0:
            intro_fade -= 5

    top_barrier.movement(top_barrier, 0.2, tick, "sine")
    bottom_barrier.movement(bottom_barrier, -0.2, tick, "sine")

    alpha_surface = pygame.Surface(display_screen.get_size(), pygame.SRCALPHA)
    alpha_surface.fill((0, 0, 0, intro_fade))

    display_screen.blit(alpha_surface, (0, 0))
    display_screen.blit(start_hint, (start_hint_x, top_barrier.y-40))
    display_screen.blit(start_key, (start_key_x, bottom_barrier.y+15))