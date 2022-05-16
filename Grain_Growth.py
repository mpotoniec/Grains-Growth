import pygame
import random
import numpy as np
from Cell import *
vec = pygame.math.Vector2
import math
from numpy.random import choice

import time

class Field():

    def __init__(self, screen, x, y, rect_size, max_ids = 10, radius = 15):
        self.screen = screen
        self.pos = vec(x, y)
        self.width, self.height = 725, 725
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()

        self.rows = 50
        self.cols = 50
        self.max_ids = max_ids
        self.radius = radius

        self.boundary_option = 'periodic'
        self.neighbourhood = 0
        self.radius_gr = 1
        self.radius_nr = 1

        self.grain_energy = 0

        self.grid = [[Cell(self.image, x,  y, rect_size) for x in range(self.cols) ] for y in range(self.rows)]
        self.set_neighbours()

    
    def update(self):
        self.rect.topleft = self.pos
        for row in self.grid:
            for cell in row:
                cell.update()
    def draw(self):
        self.image.fill((255,255,255))
        for row in self.grid:
            for cell in row:
                cell.draw(self.grain_energy)
        self.screen.blit(self.image, (self.pos.x, self.pos.y))

    def set_boundary_option(self, boundary_option):
        self.boundary_option = boundary_option
        print(self.boundary_option)

    def moore(self):
        if self.boundary_option == 'periodic':
            for x in range(self.cols):
                    for y in range(self.rows):
                        
                        self.grid[x][y].neighbours = []

                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows]) #left top
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows]) #left bottom
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows]) #right top
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows]) #right bottom
        else:
            for x in range(self.cols):
                    for y in range(self.rows):
                        
                        self.grid[x][y].neighbours = []

                        #Absorbujące warunki brzegowe

                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])

                        #left top
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows])
                        #left bottom
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows])
                        #right top
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows])
                        #right bottom
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows])
    def von_neumann(self):
        if self.boundary_option == 'periodic':
            for x in range(self.cols):
                    for y in range(self.rows):
                        
                        self.grid[x][y].neighbours = []

                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
        else:
            for x in range(self.cols):
                    for y in range(self.rows):
                        
                        self.grid[x][y].neighbours = []

                        #Absorbujące warunki brzegowe

                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])
    def pentagonal(self):

        if self.boundary_option == 'periodic':
            for x in range(self.cols):
                for y in range(self.rows):
                    choice = random.choice(['left', 'right', 'top', 'bottom'])
                    self.grid[x][y].neighbours = []
                    if choice == 'left':
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows]) #left top
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows]) #left bottom
                    elif choice == 'right':
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows]) #right top
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows]) #right bottom
                    elif choice == 'top':
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows]) #left top
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows]) #right top
                    else:
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows]) #left bottom
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows]) #right bottom
        else:
            for x in range(self.cols):
                for y in range(self.rows):
                    choice = random.choice(['left', 'right', 'top', 'bottom'])                            
                    self.grid[x][y].neighbours = []
                    if choice == 'left':
                        #Absorbujące warunki brzegowe
                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])

                        #left top
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows])
                        #left bottom
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows])
                    elif choice == 'right':
                        #Absorbujące warunki brzegowe
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])
                        #right top
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows])
                        #right bottom
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows])
                    elif choice == 'top':
                        #Absorbujące warunki brzegowe
                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])

                        #left top
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows])
                        #right top
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows])
                    else:
                        #Absorbujące warunki brzegowe
                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])

                        #left bottom
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows])
                        #right bottom
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows])
    def hexagonal(self):
        choice = random.choice(['left', 'right'])
        if self.boundary_option == 'periodic':
            for x in range(self.cols):
                for y in range(self.rows):
                    choice = random.choice(['left', 'right'])    
                    self.grid[x][y].neighbours = []
                    if choice == 'left':
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows]) #left top
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows]) #right bottom
                    else:
                        #Periodyczne warunki brzegowe
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y]) #left
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y]) #right
                        self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows]) #top
                        self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows]) #bottom
                        self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows]) #left bottom
                        self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows]) #right top
        else:
            for x in range(self.cols):
                for y in range(self.rows):
                    choice = random.choice(['left', 'right'])     
                    self.grid[x][y].neighbours = []
                    if choice == 'left':
                        #Absorbujące warunki brzegowe
                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])

                        #left top
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y - 1) % self.rows])
                        #right bottom
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y + 1) % self.rows])
                    else:  
                        #Absorbujące warunki brzegowe
                        #left
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][y])
                        #right
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][y])
                        #top
                        if y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y - 1) % self.rows])
                        #bottom
                        if y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[x][(y + 1) % self.rows])

                        #left bottom
                        if x == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == self.rows - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x - 1) % self.cols][(y + 1) % self.rows])
                        #right top
                        if x == self.cols - 1: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        elif y == 0: self.grid[x][y].neighbours.append(Cell(None, None, None))
                        else: self.grid[x][y].neighbours.append(self.grid[(x + 1) % self.cols][(y - 1) % self.rows])
    def radius_neighbours(self):
        if self.boundary_option == 'periodic':
            for x in range(self.cols):
                for y in range(self.rows):            
                    self.grid[x][y].neighbours = []

                    for x_r in range(self.radius_nr*(-1), self.radius_nr, 1):
                        for y_r in range(self.radius_nr*(-1), self.radius_nr, 1):
                            
                            x_n = self.grid[(x + x_r) % self.cols][(y + y_r) % self.rows].x + self.grid[(x + x_r) % self.cols][(y + y_r) % self.rows].quater_x
                            y_n = self.grid[(x + x_r) % self.cols][(y + y_r) % self.rows].y + self.grid[(x + x_r) % self.cols][(y + y_r) % self.rows].quater_y
                            
                            if x_n <= self.radius_nr and y_n <= self.radius_nr:
                                self.grid[x][y].neighbours.append(self.grid[(x + x_r) % self.cols][(y + y_r) % self.rows])
        else:
            for x in range(self.cols):
                for y in range(self.rows):            
                    self.grid[x][y].neighbours = []

                    for x_r in range(self.radius_nr*(-1), self.radius_nr, 1):
                        for y_r in range(self.radius_nr*(-1), self.radius_nr, 1):
                            
                            if x + x_r < 0 or x + x_r > self.cols - 1:
                                continue
                            if y + y_r < 0 or y + y_r > self.rows - 1:
                                continue

                            #print(x+x_r, y+y_r)  

                            x_n = self.grid[(x + x_r)][(y + y_r)].x + self.grid[(x + x_r)][(y + y_r)].quater_x
                            y_n = self.grid[(x + x_r)][(y + y_r)].y + self.grid[(x + x_r)][(y + y_r)].quater_y
                            if x_n <= self.radius_nr and y_n <= self.radius_nr:
                                self.grid[x][y].neighbours.append(self.grid[(x + x_r)][(y + y_r)])
                                                     
    def set_neighbours(self, flag = 0):
        if flag == 0:
            self.moore()
        elif flag == 1:
            self.von_neumann()
        elif flag == 2:
            self.pentagonal()
        elif flag == 3:
            self.hexagonal()
        else:
            self.radius_neighbours()
                    
    def set_grid(self, rows, cols, rect_size):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(self.image, x,  y, rect_size) for x in range(self.rows) ] for y in range(self.cols)]
        self.set_neighbours(self.neighbourhood)
    def set_custom_cell_vars(self, option, number_of_grains):

        self.max_ids = number_of_grains

        if option == 1:
            self.set_constant()

        if option == 2:
            self.set_with_radius()

        elif option == 3: #losowe wypełnienie
            self.set_random()            

    def set_random(self):
        id = 0
        while id < self.max_ids:
            random_x = random.randint(0, self.cols - 1)
            random_y = random.randint(0, self.rows - 1)
            if self.grid[random_x][random_y].alive:
                continue
            self.grid[random_x][random_y].alive = True
            self.grid[random_x][random_y].id = id
            id+=1

    def set_constant(self):
        id = 0
        radius = int((self.rows + self.cols)/self.max_ids) + int((self.cols+self.rows)/10) - int((self.cols+self.rows)/20) - 1

        for y in range(radius, self.cols, radius):
            for x in range(radius, self.rows, radius):
                if id < self.max_ids:
                    self.grid[y][x].alive = True
                    self.grid[y][x].id = id
                    id+=1

    def set_with_radius(self):
        id = 0
        while id < self.max_ids:
            random_x = random.randint(0, self.cols - 1)
            random_y = random.randint(0, self.rows - 1)

            to_break = False
            for x in range(self.radius_gr*(-1), self.radius_gr, 1):
                for y in range(self.radius_gr*(-1), self.radius_gr, 1):
                    if self.grid[(random_x + x) % self.cols][(random_y + y) % self.rows].alive:
                        to_break = True
                        #print('break')
                    #print(x, y)
            if to_break: continue
            self.grid[random_x][random_y].alive = True
            self.grid[random_x][random_y].id = id
            id+=1

    def evaluate(self):
        
        to_change = []

        for row in self.grid:
            for cell in row:
                if cell.alive == False:

                    ids = []
                    for neighbour in cell.neighbours:
                        if neighbour.alive:
                            ids.append(neighbour.id)
                    
                    if len(ids) > 0:
                        ids_count = [0 for i in range(self.max_ids)]
                        for id in ids:
                            ids_count[id] = ids_count[id] + 1
                        max_count = np.max(ids_count)
                        indexes = []
                        for i in range(self.max_ids):
                            if ids_count[i] == max_count: indexes.append(i)

                        vars_to_change = []
                        vars_to_change.append(cell.x)
                        vars_to_change.append(cell.y)
                        vars_to_change.append(random.choice(indexes))

                        to_change.append(vars_to_change)

        for var in to_change:
            self.grid[var[1]][var[0]].alive = True
            self.grid[var[1]][var[0]].id = var[2]
 
    def calculate_distance(self, x1, y1, x2, y2, mark1 = 0, mark2 = 0):

        if mark1 == 1:
            x1 = x1 + 0.5
            y1 = y1 - 0.5
        elif mark1 == 2:
            x1 = x1 + 0.5
            y1 = y1 + 0.5
        elif mark1 == 3:
            x1 = x1 - 0.5
            y1 = y1 + 0.5
        elif mark1 == 4:
            x1 = x1 - 0.5
            y1 = y1 - 0.5

        if mark2 == 1:
            x2 = x2 + 0.5
            y2 = y2 - 0.5
        elif mark1 == 2:
            x2 = x2 + 0.5
            y2 = y2 + 0.5
        elif mark1 == 3:
            x2 = x1 - 0.5
            y2 = y1 + 0.5
        elif mark1 == 4:
            x2 = x2 - 0.5
            y2 = y2 - 0.5    

        return abs(((x2 - x1)**2 + (y2 - y1)**2)**0.5)   

    def mc_algorithm(self, MC_steps, kt):

        #start = time.time()

        for i in range(MC_steps):
            if i == 0:
                coordinates = []
                for row in range(self.rows):
                    for col in range(self.cols):
                        coordinates.append([row, col])
            else:
                coordinates = []
                for row in range(self.rows):
                    for col in range(self.cols):
                        if self.grid[col][row].Q != 0:
                            coordinates.append([row, col])  

            while len(coordinates) > 0:
                coordinate = random.choice(coordinates)
                
                old_id = self.grid[coordinate[1]][coordinate[0]].id

                current_cell = self.grid[coordinate[1]][coordinate[0]]
                current_cell.Q = 0
                for neighbour in current_cell.neighbours:
                    if neighbour.alive:
                        if current_cell.id != neighbour.id: current_cell.Q+=1
                self.grid[coordinate[1]][coordinate[0]].Q = current_cell.Q

                while True:
                    neighbour_to_change = random.choice(current_cell.neighbours)
                    if neighbour_to_change.alive:
                        current_cell.id = neighbour_to_change.id
                        break
                    
                new_id = self.grid[coordinate[1]][coordinate[0]].id
                Q_before = current_cell.Q
                current_cell.Q = 0
                for neighbour in current_cell.neighbours:
                    if neighbour.alive:
                        if current_cell.id != neighbour.id: current_cell.Q+=1
                Q_after = current_cell.Q
                Q_delta = Q_after - Q_before
                p = [0,0]
                if Q_delta <= 0: 
                    p[0] = 1
                else:
                    p[0] = math.exp((Q_delta*(-1))/kt)
                
                p[1] = 1 - p[0]

                ids = []
                ids.append(new_id)
                ids.append(old_id)
                id_to_write = choice(ids, p = p)

                self.grid[coordinate[1]][coordinate[0]].id = id_to_write
                
                coordinates.remove(coordinate)
            #print(i + 1, time.time()-start2)

        #print(time.time()-start)
