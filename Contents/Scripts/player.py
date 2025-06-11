import pygame

pygame.init()

class Player:
    def __init__(self, x, y, speed):
        self.object = pygame.image.load("Contents/Sprites/Game/sod.png").convert_alpha()
        self.dead = pygame.image.load("Contents/Sprites/Game/sod-sad.png").convert_alpha()
        self.trail = pygame.image.load("Contents/Sprites/Game/sod-trail.png").convert_alpha()
        self.end = pygame.image.load("Contents/Sprites/Game/sod-dark.png").convert_alpha()
        self.state = "alive"
        self.x = x
        self.y = y
        self.lives = 3
        self.invincibility = 0
        self.speed = speed 
        self.velocity = [0, 0]

        self.friction = 0.9

        self.width = self.object.get_width()
        self.height = self.object.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, display_screen):
        for i in range(1, 3):
            display_screen.blit(self.trail, (self.x - (self.velocity[0] * (1.5*i)), self.y - (self.velocity[1] * (1.5*i))))
        if self.state == "alive":
            display_screen.blit(self.object, (self.x, self.y))
        elif self.state == "dead":
            display_screen.blit(self.dead, (self.x, self.y))
        elif self.state == "invincible":
            display_screen.blit(self.trail, (self.x, self.y))
            pygame.draw.circle(display_screen, (0, 0, 255), (self.x + self.width // 2, self.y + self.height // 2), 14, 1)
            if self.invincibility % 3 == 0 and self.invincibility < 50:
                display_screen.blit(self.object, (self.x, self.y))
        elif self.state == "end":
            display_screen.blit(self.end, (self.x, self.y))
        
    def update(self, displacement, top_barrier, bottom_barrier, bullets_group):
    #Update the player's rect position and factor in collisions (x-axis)
        self.velocity[0] += displacement[0] * self.speed
        self.velocity[0] *= self.friction
        self.rect.x += self.velocity[0]

    #Update the player's rect position and factor in collisions (y-axis)
        self.velocity[1] += displacement[1] * self.speed
        self.velocity[1] *= self.friction
        self.rect.y += self.velocity[1]

    #Update player collisions
        if self.rect.colliderect(top_barrier.rect):
            self.rect.top = top_barrier.rect.bottom

        if self.rect.colliderect(bottom_barrier.rect):
            self.rect.bottom = bottom_barrier.rect.top
        
        if pygame.sprite.spritecollide(self, bullets_group, False) and self.state != "invincible" and self.lives > 0:
            self.lives -= 1
            self.invincibility = 100

    #After calculating their position including collisions, update their actual position
        self.x = self.rect.x
        self.y = self.rect.y

        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= (600 // 2) - self.width:
            self.rect.x = (600 // 2) - self.width
        
        self.invincibility -= 1
        if self.invincibility <= 0 and self.state == "invincible":
            self.state = "alive"