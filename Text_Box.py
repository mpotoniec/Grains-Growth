import pygame
vec = pygame.math.Vector2

class TextBox():
    def __init__(self, x, y, width, height, bg_colour = (230, 230, 230), active_colour = (255, 255, 255), 
    text_size = 18, text_colour = (0, 0, 0), border = False, border_colour = (0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = vec(x, y)
        self.size = vec(width, height)
        self.image = pygame.Surface((width, height))
        self.bg_colour = bg_colour
        self.active_colour = active_colour
        self.active = False
        self.text = ""
        self.text_size = text_size
        self.font = pygame.font.SysFont("Times New Roman", self.text_size)
        self.text_colour = text_colour
        self.border = border
        self.border_colour = border_colour

    def update(self):
        pass

    def draw(self, window):
        if not self.active:
            if self.border == 0:
                self.image.fill(self.bg_colour)
            else:
                pygame.draw.rect(self.image, 
                self.bg_colour, 
                (self.border, 
                self.border, 
                self.width-self.border*2, 
                self.height-self.border*2))
            text = self.font.render(self.text, False, self.text_colour)
            text_height = text.get_height()
            self.image.blit(text, (5, (self.height - text_height)/2))
        else:
            if self.border == 0:
                self.image.fill(self.active_colour)
            else:
                pygame.draw.rect(self.image, 
                self.active_colour, 
                (self.border, 
                self.border, 
                self.width-self.border*2, 
                self.height-self.border*2))
            text = self.font.render(self.text, False, self.text_colour)
            text_height = text.get_height()
            self.image.blit(text, (5, (self.height - text_height)/2))
        window.blit(self.image, self.pos)

    def add_text(self, key): 
        try:
            if chr(key).isdigit() or chr(key) == '-' or chr(key) == '.':
                text = list(self.text)
                text.append(chr(key))
                self.text = ''.join(text)
            elif key == 8:
                text = list(self.text)
                text.pop()
                self.text = ''.join(text)
        except: pass

    def check_click(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.active = True
            else: self.active = False
        else: self.active = False

    def return_value(self):
        return self.text