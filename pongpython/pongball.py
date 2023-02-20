import pygame
import math
import random


class PongBall:
    """
    Implements game ball and its movement functionality
    """
    def __init__(self, x: int, y: int, direction: bool, color: tuple, radius: int =6, vel: int =5):
        self.x = self.orig_x = x
        self.y = self.orig_y = y

        self.color = color
        self.radius = radius
        self.vel = vel
        self.orig_direction = 1 if direction else -1

        self._init_vel()
        
       

    def _init_vel(self):
        angle = math.radians(random.randint(-25, 25))

        self.x_vel = self.orig_direction * abs(math.cos(angle) * self.vel)
        self.y_vel = math.sin(angle) * self.vel


    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.orig_x
        self.y = self.orig_y

        self._init_vel()
