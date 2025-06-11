import pygame

class Sodling(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Contents/Sprites/Game/sodling.png").convert_alpha()
        self.x = x
        self.y = y

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def display(self, display_screen):
        display_screen.blit(self.image, (self.x, self.y))