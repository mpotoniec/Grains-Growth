import pygame
vec = pygame.math.Vector2

class Text():
    def __init__(self, x, y, width, height, bg_colour = (255, 255, 255), text_size = 18, text_colour = (0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x, y)
        self.size = vec(width, height)
        self.image = pygame.Surface((width, height))
        self.bg_colour = bg_colour
        self.text = ""
        self.text_size = text_size
        self.font = pygame.font.SysFont("Times New Roman", self.text_size)
        self.text_colour = text_colour


    def update(self):
        pass

    def draw(self, window):
        self.image.fill(self.bg_colour)
        text = self.font.render(self.text, False, self.text_colour)
        text_height = text.get_height()
        self.image.blit(text, (5, (self.height - text_height)/2))
        window.blit(self.image, self.pos)