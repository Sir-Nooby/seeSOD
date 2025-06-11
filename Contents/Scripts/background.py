#Background
import pygame
import math
import random

pygame.init()

class BackgroundManager(): #Chnagbe color
    def __init__(self, mode, display_screen):
        self.display_screen = display_screen
        self.mode = mode
        self.color_switch = 0 #Combine timers
        self.flame_switch = 0
        self.shape_switch = 0
        self.circle_spawn = 0
        self.bubble_spawn = 0
        self.circle_color = 1
        self.angle = 0
        self.objects_bubbles = []
        self.objects_shape = []
        self.objects_fire = []
        self.circles = []
        self.palette = [self.random_color() for i in range(16)]
        self.palettes = [
            ["#8DBCC7", "#A4CCD9", "#C4E1E6", "#EBFFD8", "#EBFFD8", "#C4E1E6", "#A4CCD9", "#8DBCC7"],
            ["#5409DA", "#4E71FF", "#8DD8FF", "#BBFBBF", "#BBFBBF", "#8DD8FF", "#4E71FF", "#5409DA"],
            ["#819A91", "#A7C1A8", "#D1D8BE", "#EEEFE0", "#EEEFE0", "#D1D8BE", "#A7C1A8", "#819A91"],
            ["#B33791", "#C562AF", "#DB8DD0", "#FEC5F6", "#FEC5F6", "#DB8DD0", "#C562AF", "#B33791"],
            ["#3A0519", "#670D2F", "#A53860", "#EF88AD", "#EF88AD", "#A53860", "#670D2F", "#3A0519"],
            ["#FFB200", "#EB5B00", "#D91656", "#640D5F", "#640D5F", "#D91656", "#EB5B00", "#FFB200"],
            ["#222831", "#393E46", "#948979", "#DFD0B8", "#DFD0B8", "#948979", "#393E46", "#222831"],
            ["#E3FDFD", "#CBF1F5", "#A6E3E9", "#71C9CE", "#71C9CE", "#A6E3E9", "#CBF1F5", "#E3FDFD"],
            ["#F9F7F7", "#DBE2EF", "#3F72AF", "#112D4E", "#112D4E", "#3F72AF", "#DBE2EF", "#F9F7F7"],
            ["#1B262C", "#0F4C75", "#3282B8", "#BBE1FA", "#BBE1FA", "#3282B8", "#0F4C75", "#1B262C"],
            ["#AD8B73", "#CEAB93", "#E3CAA5", "#FFFBE9", "#FFFBE9", "#E3CAA5", "#CEAB93", "#AD8B73"],
            ["#F4EEFF", "#DCD6F7", "#A6B1E1", "#424874", "#424874", "#A6B1E1", "#DCD6F7", "#F4EEFF"],
            ["#08D9D6", "#252A34", "#FF2E63", "#EAEAEA", "#EAEAEA", "#FF2E63", "#252A34", "#08D9D6"],
            ["#EDF1D6", "#9DC08B", "#609966", "#40513B", "#40513B", "#609966", "#9DC08B", "#EDF1D6"],
        ]
        self.current_palette = random.randint(1, len(self.palettes))-1

    def update(self):
        if self.mode == "color_bars":
            self.color_bars()
        elif self.mode == "smear":
            self.paint_smear()
        elif self.mode == "shapes":
            self.random_shapes()
        elif self.mode == "sine":
            self.sinusodal_wave()
        elif self.mode == "sine16":
            self.sinusodal_wave_16()
        elif self.mode == "flag":
            self.color_flag()
        elif self.mode == "spiral":
            self.spiral()
        elif self.mode == "bubbles":
            self.bubbles()
        elif self.mode == "static":
            self.static_color()
    
    #Random Color Generation
    def random_color(self):
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return random_color
    
    def new_palette(self):
        self.palette = [self.random_color() for i in range(16)]
        self.current_palette = random.randint(1, len(self.palettes))-1

    #Define all background methods
    def static_color(self):
        self.display_screen.fill(self.palettes[self.current_palette][0])
    
    def paint_smear(self): #paint smear, also broken
        if self.flame_switch == 0:
            self.flame_switch = 5
            for i in range(2):
                self.objects_fire.append([random.uniform(0, 300), 150, 5, random.uniform(-10, 10), random.randint(10, 15), random.randint(0, 7)])
            
        for f in self.objects_fire[:]:
            color_rgb = self.palettes[self.current_palette][f[5]]
            pygame.draw.circle(self.display_screen, color_rgb, (f[0], f[1]), f[4])

            f[0] += random.uniform(-0.5, 0.5)
            f[2] -= 0.05
            f[4] -= 0.05
            f[1] -= f[3]
            if f[1] <= 0 or f[1] >= 300 or f[2] <= 0 or f[4] <= 0:
                self.objects_fire.remove(f)

        self.flame_switch -= 1

    def bubbles(self):
        if self.bubble_spawn == 0:
            self.bubble_spawn = 10
            self.objects_bubbles.append([random.randint(0, 300), random.randint(0, 300), random.randint(9, 12)])

        for i in self.objects_bubbles[:]:
            pygame.draw.circle(self.display_screen, (0, 0, 0), (i[0], i[1]), i[2])
            i[2] -= 1
            
            if i[2] <= 0:
                self.objects_bubbles.remove(i)

        self.bubble_spawn -= 1

    def sinusodal_wave(self): #Menu thing
            for i in range(8):
                for j in range(101):
                    x = j * 5 
                    y = (i * 40) + math.sin(self.angle + (j / 100.0)) * (20.0 * (j / 100.0)) + 80
                    radius = 100
                    color = self.palettes[self.current_palette][i]
                    pygame.draw.circle(self.display_screen, color, (x, y), radius)  
            self.angle += 0.02
            if self.angle > 2 * math.pi:
                self.angle -= 2 * math.pi
                           
    def sinusodal_wave_16(self):
        for i in range(16):
            for j in range(101):
                x = j * 5 #Spacim
                y = (i * 20) + math.sin(self.angle + (j / 100.0)) * (10.0 * (j / 100.0)) + 10
                radius = 20
                if i >= 8:
                    color = self.palettes[self.current_palette][i-8]
                else:
                    color = self.palettes[self.current_palette][i]
                pygame.draw.circle(self.display_screen, color, (x, y), radius)  
        self.angle += 0.02
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def color_bars(self): #streamline palette on color bars and flags
        if self.color_switch == 0:
            self.color_switch = 50
            self.palette = self.palette[1:] + [self.palette[0]]
            for i in range(4):
                pygame.draw.rect(self.display_screen, self.palette[i], [75*i, 0, 75, 300])
        self.color_switch -= 1

    def color_flag(self):
        if self.color_switch == 0:
            self.color_switch = 50
            self.palette = self.palette[1:] + [self.palette[0]]
            for i in range(10):
                pygame.draw.rect(self.display_screen, self.palette[i], [0, 30 * i, 300, 75])
        self.color_switch -= 1

    def random_shapes(self):
        if self.shape_switch == 0:
            self.shape_switch = 10
            for i in range(15):
                self.objects_shape.append([random.randint(-10, 300), random.randint(-10, 300), random.randint(35, 60), random.randint(35, 60)])
            
        for s in self.objects_shape[:]:
            pygame.draw.rect(self.display_screen, self.palettes[self.current_palette][2], (s[0], s[1], s[2], s[3]))
            if s[2] <= 0 or s[3] <= 0:
                self.objects_shape.remove(s)
        
        self.shape_switch -= 1
    
    def spiral(self):
        if self.circle_spawn == 0:
            self.circle_spawn = 10
            if self.circle_color == 1:
                self.circles.append([5, self.palettes[self.current_palette][0]])
                self.circle_color = 0
            else:
                self.circles.append([5, self.palettes[self.current_palette][1]])
                self.circle_color = 1
        
        for i in self.circles[:]:
            pygame.draw.circle(self.display_screen, i[1], (150, 150), i[0])
            i[0] += 2

            if i[0] >= 250:
                self.circles.remove(i)
        
        self.circle_spawn -= 1

