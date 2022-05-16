import pygame, random

class Cell:
    def __init__(self, surface, x, y, rect_size = 0):

        self.rect_size = rect_size

        self.alive = False
        self.surface = surface
        self.x = x
        self.y = y
        self.image = pygame.Surface((self.rect_size, self.rect_size))
        self.rect = self.image.get_rect()
        self.neighbours = []
        self.alive_neighbours = 0

        self.id = None
        self.quater_x = random.randint(-10, 10)/10
        self.quater_y = random.randint(-10, 10)/10
        self.Q = 0


    def update(self):
        self.rect.topleft = (self.x*self.rect_size, self.y*self.rect_size)

    def draw(self, mark = 0):
        if mark == 0:
            if self.alive:
                self.image.fill(((255-self.id*10)%255, (255-self.id*20)%255, (255-self.id*30)%255)) 
            else:
                self.image.fill((0, 0, 0))
                pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 18, 18))
            self.surface.blit(self.image, (self.x*self.rect_size, self.y*self.rect_size))
        else:
            if self.Q == 0:
                self.image.fill((0, 150, 255))
            else:
                self.image.fill((255, 200 - self.Q * 15, 0))
            self.surface.blit(self.image, (self.x*self.rect_size, self.y*self.rect_size))

    def print_cell(self):
        print('x, y', self.x, self.y, 'alive', self.alive, 'id', self.id)