import pygame
import math
import random

pygame.init()


#Define the Bullet Class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, type, movement=1, direction_x=1, direction_y=1):
        self.image = pygame.image.load("Contents/Sprites/Game/bullet-8.png").convert_alpha()
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.type = type
        self.movement = movement
        self.directionx = direction_x
        self.directiony = direction_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self, display_screen, top_barrier, bottom_barrier, tick): 
        offset_x = 0
        offset_y = 0
        if self.type == "x-shift":
            offset_x = self.movement * self.directionx
        elif self.type == "y-shift":
            offset_y = self.movement * self.directiony
        elif self.type == "diagonal":
            offset_x = self.movement * self.directionx
            offset_y = self.movement * self.directiony
        elif self.type == "sine":
            offset_y = math.sin(tick) * 1.25 * self.movement
            offset_x = self.movement * self.directionx
        elif self.type == "cosine":
            offset_y = math.cos(tick) * 1.25 * self.movement
            offset_x = self.movement * self.directionx
        elif self.type == "closer-left":
            offset_y = math.sin(tick) * 1.25 * self.movement
            offset_x = -1
        elif self.type == "closer-right":
            offset_y = math.sin(tick) * 1.25 * self.movement
            offset_x = 1
        elif self.type == "root":
            offset_x = math.sqrt(tick) * 0.25
            offset_y = 0.5
        elif self.type == "spiral":
            angle = tick * (2 * math.pi / 12)
            offset_x = math.cos(angle) * 2.5
            offset_y = math.sin(angle) * 2.5

        if self.rect.colliderect(top_barrier.rect) or self.rect.colliderect(bottom_barrier.rect):
            self.kill()
        if self.rect.x >= display_screen.get_width() or self.rect.x <= -20:
            self.kill()
        
        
        self.x += offset_x
        self.rect.x += offset_x
        self.y += offset_y
        self.rect.y += offset_y

def random_bullet_spawn(top_barrier, bottom_barrier):
    return (random.randint(0, 300), random.uniform(top_barrier.y + 10, bottom_barrier.y - 10))

def t_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "x-shift"))
    bullets_group.add(Bullet(random_x, random_y, "x-shift", -1))
    bullets_group.add(Bullet(random_x, random_y, "y-shift"))
    bullets_group.add(Bullet(random_x, random_y, "y-shift", -1))

def x_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "diagonal"))
    bullets_group.add(Bullet(random_x, random_y, "diagonal", 1, -1, 1))
    bullets_group.add(Bullet(random_x, random_y, "diagonal", 1, -1, -1))
    bullets_group.add(Bullet(random_x, random_y, "diagonal", 1, 1, -1))

def tri_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "y-shift", -1))
    bullets_group.add(Bullet(random_x, random_y, "root", 0.25))
    bullets_group.add(Bullet(random_x, random_y, "root", -0.25))

def flower_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "y-shift", -1))
    bullets_group.add(Bullet(random_x, random_y, "x-shift"))
    bullets_group.add(Bullet(random_x, random_y, "x-shift", -1))
    bullets_group.add(Bullet(random_x, random_y, "root", 0.25))
    bullets_group.add(Bullet(random_x, random_y, "root", -0.25))

def line_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "y-shift", -1))
    bullets_group.add(Bullet(random_x, random_y, "y-shift", 1))
    bullets_group.add(Bullet(random_x, random_y, "y-shift", -2))
    bullets_group.add(Bullet(random_x, random_y, "y-shift", 2))

def sine_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "sine", movement=1, direction_x=1))
    bullets_group.add(Bullet(random_x, random_y, "sine", movement=-1, direction_x=1))
    bullets_group.add(Bullet(random_x, random_y, "sine", movement=-1, direction_x=-1))
    bullets_group.add(Bullet(random_x, random_y, "sine", movement=1, direction_x=-1))\

def cosine_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "cosine", movement=1, direction_x=1))
    bullets_group.add(Bullet(random_x, random_y, "cosine", movement=-1, direction_x=1))
    bullets_group.add(Bullet(random_x, random_y, "cosine", movement=-1, direction_x=-1))
    bullets_group.add(Bullet(random_x, random_y, "cosine", movement=1, direction_x=-1))

def closer_left(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "closer-left"))
    bullets_group.add(Bullet(random_x, random_y, "closer-left", -1))

def closer_right(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "closer-right"))
    bullets_group.add(Bullet(random_x, random_y, "closer-right", -1))

def spiral_pattern(random_x, random_y, bullets_group):
    bullets_group.add(Bullet(random_x, random_y, "spiral"))