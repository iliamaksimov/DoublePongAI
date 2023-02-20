import pygame

class PongPaddle:
    """
    Implements game paddle and its movement functionality
    """
    def __init__(self, x: int, y: int, color: tuple, vel: int =4, width: int =20, height: int =100):
        self.x = self.original_x = x
        self.y = self.original_y = y

        self.vel = vel
        self.width = width
        self.height = height
        self.color = color

    def draw(self, window):
        pygame.draw.rect(
            window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, down=True):
        if down:
            self.y += self.vel
        else:
            self.y -= self.vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
