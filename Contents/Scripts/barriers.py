import pygame
import math

pygame.init()

#Define the Barrier Class
class GameBarriers:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def display(self, display_screen):
        pygame.draw.rect(display_screen, self.color, (self.x, self.y, self.width, self.height))

    #Define moving states
    def movement(self, object, oscillation, tick, movement, offset=0, y=0):
        if movement == "sine":
            offset = math.sin(tick) * oscillation
        elif movement == "cosine":
            offset = math.cos(tick) * oscillation
        elif movement == "crunch":
            offset -= 0.5
        elif movement == "set-position":
            self.y = y

        object.y -= offset
        object.rect.y = object.y
