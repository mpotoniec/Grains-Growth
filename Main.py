import pygame
import sys

from Grain_Growth import Field
from Button import Button
from Text_Box import TextBox
from Text import Text

WIDTH, HEIGHT = 1000, 775
FPS = 60 
BACKGROUND = (255, 255, 255) 
GRID_HEIGHT = 50 
GRID_WIDTH = 50 
RECT_SIZE = 14 

number_of_grains = 20 
courent_id = 0 
radius = 1 

MC_steps = 5 
kt = 0.1 

visualisation = 0

def get_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_on_grid(mouse_pos):
                click_cell(mouse_pos)
            else:
                for button in buttons:
                    button.click()
                for box in text_boxes:
                    box.check_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            for box in text_boxes:
                if box.active:
                    box.add_text(event.key)
def update():
    field.update()
    for button in buttons:
        button.update(mouse_pos, game_state=state)
def draw():
    window.fill(BACKGROUND)
    for button in buttons:
        button.draw()
    for box in text_boxes:
        box.draw(window)
    for text in texts:
        text.draw(window)    
    field.draw()

def running_get_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_on_grid(mouse_pos):
                click_cell(mouse_pos)
            else:
                for button in buttons:
                    button.click()
def running_update():
    field.update()
    for button in buttons:
        button.update(mouse_pos, game_state=state)
    if frame_count%(FPS/speed) == 0:
        field.evaluate()
def running_draw():
    window.fill(BACKGROUND)
    for button in buttons:
        button.draw()
    for text in texts:
        text.draw(window)
    field.draw()

def paused_get_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_on_grid(mouse_pos):
                click_cell(mouse_pos)
            else:
                for button in buttons:
                    button.click()
                for box in text_boxes:
                    box.check_click(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            for box in text_boxes:
                if box.active:
                    box.add_text(event.key)
def paused_update():
    field.update()
    for button in buttons:
        button.update(mouse_pos, game_state=state)
def paused_draw():
    window.fill(BACKGROUND)
    for button in buttons:
        button.draw()
    for box in text_boxes:
        box.draw(window)
    for text in texts:
        text.draw(window)
    field.draw()

def mouse_on_grid(pos):
    if pos[0] > 25 and pos[0] < WIDTH - 250:
        if pos[1] > 25 and pos[1] < HEIGHT - 25:
            return True
    else: return False
def click_cell(pos):
    global courent_id
    grid_pos = [pos[0] - 25, pos[1] - 25]
    grid_pos[0] = grid_pos[0]//RECT_SIZE
    grid_pos[1] = grid_pos[1]//RECT_SIZE
    if field.grid[grid_pos[1]] [grid_pos[0]].alive:
        field.grid[grid_pos[1]] [grid_pos[0]].id = None
        field.grid[grid_pos[1]] [grid_pos[0]].alive = False
    else: 
        field.grid[grid_pos[1]] [grid_pos[0]].id = courent_id
        field.grid[grid_pos[1]] [grid_pos[0]].alive = True
        courent_id+=1
        if courent_id == number_of_grains: courent_id = 0
def make_buttons():
    buttons = []

    buttons.append(Button(window, 825, 30, 100, 30, text = 'run/pause',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = run_pause, state = ''))

    buttons.append(Button(window, 825, 70, 100, 30, text = 'periodic',
                          colour = (255, 0, 0), hover_colour=(255, 0, 0), bold_text=False, function = set_periodic_boundary_conditions, state = ''))

    buttons.append(Button(window, 825, 100, 100, 30, text = 'absorbic',
                          colour = (130, 130, 130), hover_colour=(255, 0, 0), bold_text=False, function = set_absorbic_boundary_conditions, state = ''))
    
    buttons.append(Button(window, 825, 140, 100, 30, text = 'moore',
                          colour = (0, 255, 0), hover_colour=(0, 255, 0), bold_text=False, function = set_Moore_neighborhood, state = ''))

    buttons.append(Button(window, 825, 170, 100, 30, text = 'neumann',
                          colour = (130, 130, 130), hover_colour=(0, 255, 0), bold_text=False, function = set_von_Neumann_neighborhood, state = ''))

    buttons.append(Button(window, 825, 200, 100, 30, text = 'pentagonal',
                          colour = (130, 130, 130), hover_colour=(0, 255, 0), bold_text=False, function = set_Pentagonal_random_neighborhood, state = ''))

    buttons.append(Button(window, 825, 230, 100, 30, text = 'hexagonal',
                          colour = (130, 130, 130), hover_colour=(0, 255, 0), bold_text=False, function = set_Hexagonal_neighborhood, state = ''))

    buttons.append(Button(window, 825, 260, 100, 30, text = 'radius',
                          colour = (130, 130, 130), hover_colour=(0, 255, 0), bold_text=False, function = set_Radius_neighborhood, state = ''))

    buttons.append(Button(window, 825, 380, 100, 30, text = 'set grid',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = set_grid, state = ''))

    buttons.append(Button(window, 825, 470, 100, 30, text = 'const',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = set_const_cells, state = ''))

    buttons.append(Button(window, 825, 500, 100, 30, text = 'random',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = set_random_cells, state = ''))

    buttons.append(Button(window, 825, 530, 100, 30, text = 'with_radius',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = set_radius_cells, state = ''))
    
    buttons.append(Button(window, 825, 670, 100, 30, text = 'MC',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = mc, state = ''))

    buttons.append(Button(window, 825, 700, 100, 30, text = 'speed up',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = speedUP, state = ''))

    buttons.append(Button(window, 825, 730, 100, 30, text = 'slow down',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = slowDOWN, state = ''))

    buttons.append(Button(window, 825, 580, 100, 30, text = 'Grain/Energy',
                          colour = (130, 130, 130), hover_colour=(170, 170, 170), bold_text=False, function = grain_energy, state = ''))


    return buttons
def make_text_boxes():
    text_boxes = []

    text_boxes.append(TextBox(825, 345, 40, 30, border = 1)) #Width
    text_boxes[0].text = '50'
    text_boxes.append(TextBox(885, 345, 40, 30, border = 1)) #Height
    text_boxes[1].text = '50'
    text_boxes.append(TextBox(950, 440, 40, 30, border = 1)) #Grows
    text_boxes[2].text = '20'
    text_boxes.append(TextBox(950, 610, 40, 30, border = 1)) #MCS
    text_boxes[3].text = '5'
    text_boxes.append(TextBox(950, 640, 40, 30, border = 1)) #kt
    text_boxes[4].text = '0.1'
    text_boxes.append(TextBox(950, 290, 40, 30, border = 1)) #radius sąsiedztwo
    text_boxes[5].text = '1'
    text_boxes.append(TextBox(950, 530, 40, 30, border = 1)) #radius zarodkowanie
    text_boxes[6].text = '1'


    return text_boxes
def make_texts():
    texts = []

    texts.append(Text(825, 440, 100, 30))
    texts[0].text = 'Grains = 20'
    texts.append(Text(825, 315, 40, 30, text_size = 15))
    texts[1].text = 'Width'
    texts.append(Text(885, 315, 40, 30, text_size = 15))
    texts[2].text = 'Height'
    texts.append(Text(825, 410, 120, 30))
    texts[3].text = 'Grid = 50x50'
    texts.append(Text(825, 610, 120, 30))
    texts[4].text = 'MC steps = 5'
    texts.append(Text(825, 640, 120, 30))
    texts[5].text = 'kt = 0.1'
    texts.append(Text(825, 290, 120, 30))
    texts[6].text = 'radius = 1'

    return texts

def run_pause():
    global state
    if state == 'paused' or state == 'setting':
        state = 'running'
    elif state == 'running':
        state = 'paused'

def set_const_cells():
    global state
    state = 'setting'
    global number_of_grains
    if int(text_boxes[2].text) > 0: number_of_grains = int(text_boxes[2].text)
    texts[0].text = 'Grains = ' + str(number_of_grains)  
    set_grid()
    field.set_custom_cell_vars(1, number_of_grains)
def set_radius_cells():
    global state
    state = 'setting'
    global number_of_grains
    if int(text_boxes[2].text) > 0: number_of_grains = int(text_boxes[2].text)
    texts[0].text = 'Grains = ' + str(number_of_grains)  
    set_grid()
    if int(text_boxes[6].text) > 0: 
        field.radius_gr = int(text_boxes[6].text)
    field.set_custom_cell_vars(2, number_of_grains)
def set_random_cells():
    global state
    state = 'setting'
    global number_of_grains
    if int(text_boxes[2].text) > 0: number_of_grains = int(text_boxes[2].text)
    texts[0].text = 'Grains = ' + str(number_of_grains)  
    set_grid()
    field.set_custom_cell_vars(3, number_of_grains)

def speedUP():
    global speed
    if speed == 5:
        speed = 10
    elif speed == 10:
        speed = 30
    else: speed = 60
def slowDOWN():
    global speed
    if speed == 60:
        speed = 30
    elif speed == 30:
        speed = 10
    else: speed = 5

def set_periodic_boundary_conditions():
    field.set_boundary_option('periodic')
    field.set_neighbours(field.neighbourhood)
    buttons[1].colour = (255,0,0)
    buttons[2].colour = (130,130,130)
def set_absorbic_boundary_conditions():
    field.set_boundary_option('absorbic')
    field.set_neighbours(field.neighbourhood)
    buttons[2].colour = (255,0,0)
    buttons[1].colour = (130,130,130)

def set_Moore_neighborhood():
    field.set_neighbours(0)
    field.neighbourhood = 0
    buttons[3].colour = (0,255,0)
    buttons[4].colour = (130,130,130)
    buttons[5].colour = (130,130,130)
    buttons[6].colour = (130,130,130)
    buttons[7].colour = (130,130,130)
def set_von_Neumann_neighborhood():
    field.set_neighbours(1)
    field.neighbourhood = 1
    buttons[3].colour = (130,130,130)
    buttons[4].colour = (0,255,0)
    buttons[5].colour = (130,130,130)
    buttons[6].colour = (130,130,130)
    buttons[7].colour = (130,130,130)
def set_Pentagonal_random_neighborhood():
    field.set_neighbours(2)
    field.neighbourhood = 2
    buttons[3].colour = (130,130,130)
    buttons[4].colour = (130,130,130)
    buttons[5].colour = (0,255,0)
    buttons[6].colour = (130,130,130)
    buttons[7].colour = (130,130,130)
def set_Hexagonal_neighborhood():
    field.set_neighbours(3)
    field.neighbourhood = 3
    buttons[3].colour = (130,130,130)
    buttons[4].colour = (130,130,130)
    buttons[5].colour = (130,130,130)
    buttons[6].colour = (0,255,0)
    buttons[7].colour = (130,130,130)
def set_Radius_neighborhood():
    global radius
    if int(text_boxes[5].text) > 0: 
        radius = int(text_boxes[5].text)
        texts[6].text = 'radius = ' + str(text_boxes[5].text)
    field.radius_nr = radius
    field.set_neighbours(4)
    buttons[3].colour = (130,130,130)
    buttons[4].colour = (130,130,130)
    buttons[5].colour = (130,130,130)
    buttons[6].colour = (130,130,130)
    buttons[7].colour = (0,255,0)

def set_grid():
    global RECT_SIZE
    global state
    global GRID_HEIGHT
    global GRID_WIDTH
    state = 'setting'
    if text_boxes[0].text.isdigit() and int(text_boxes[0].text) > 0: GRID_WIDTH = int(text_boxes[0].text)
    if text_boxes[1].text.isdigit() and int(text_boxes[1].text) > 0: GRID_HEIGHT = int(text_boxes[1].text)
    RECT_SIZE = int(1450 / (GRID_HEIGHT + GRID_WIDTH)) + 1
    texts[3].text = 'Grid = ' + str(GRID_WIDTH) + 'x' + str(GRID_HEIGHT)
    field.set_grid(GRID_WIDTH, GRID_HEIGHT, RECT_SIZE)

def grain_energy():
    global visualisation
    if visualisation == 0: visualisation = 1
    else: visualisation = 0

    field.grain_energy = visualisation

def mc():
    global MC_steps
    global kt
    MC_steps = int(text_boxes[3].text)
    if (float(text_boxes[4].text) >= 0.1) and (float(text_boxes[4].text) <= 6): kt = float(text_boxes[4].text)
    texts[4].text = 'MC steps = ' + str(MC_steps)
    texts[5].text = 'kt = ' + str(kt)
    field.mc_algorithm(MC_steps, kt)

pygame.init()
pygame.display.set_caption('Rozrost Ziaren')
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

field = Field(window, 25, 25, RECT_SIZE, number_of_grains)
buttons = make_buttons()
text_boxes = make_text_boxes()
texts = make_texts()

state = 'setting'
frame_count = 0
speed = 60

running = True

while running:
    frame_count += 1
    mouse_pos = pygame.mouse.get_pos()
    if state == 'setting':
        get_events()
        update()
        draw()
    if state == 'running':
        running_get_events()
        running_update()
        running_draw()
    if state == 'paused':
        paused_get_events()
        paused_update()
        paused_draw()
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
sys.exit()
