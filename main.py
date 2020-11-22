from tkinter import *
from decorators import type_control, timer
import numpy as np
from math import floor
from functools import partial

cells_number_x = 30
cells_number_y = cells_number_x
cells_number = (cells_number_x, cells_number_y)

global cells
cells = np.zeros(cells_number)

window_width = 700
window_height = window_width
square_size_x = floor(window_width/cells_number_x)
square_size_y = floor(window_height/cells_number_y)
square_size = (square_size_x, square_size_y)

@type_control(Canvas, int, int, tuple)
def squares(cv, canvas_width, canvas_height, square_size):
    for i in range(0, canvas_width, square_size[0]):
        cv.create_line(i, 0, i, canvas_height)
    for i in range(0, canvas_height, square_size[1]):
        cv.create_line(0, i, canvas_width, i)
    return cv

@type_control(tuple, Canvas, tuple)
def black(coordinates, cv, square_size):
    cv.create_rectangle(square_size_x*coordinates[0], square_size_y*coordinates[1], square_size_x*(coordinates[0]+1), square_size_y*(coordinates[1]+1), fill="black")
    return cv

@type_control(tuple, Canvas, tuple)
def white(coordinates, cv, square_size):
    cv.create_rectangle(square_size_x*coordinates[0], square_size_y*coordinates[1], square_size_x*(coordinates[0]+1), square_size_y*(coordinates[1]+1), fill="white")
    return cv

@type_control(Canvas, np.ndarray, tuple)
@timer
def update_view(cv, cells, square_size):
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            if cells[i][j] == 1:
                black((i, j), cv, square_size)
            else:
                white((i, j), cv, square_size)
    return cv

@type_control(int, int, tuple)
def neighbours(x, y, cells_number):
    ng = []
    if x > 0 :
        ng.append((x-1, y))
        if y > 0:
            ng.append((x-1, y-1))
        if y < cells_number[1] - 1:
            ng.append((x-1, y+1))
    if x < cells_number[0] - 1:
        ng.append((x+1, y))
        if y > 0:
            ng.append((x+1, y-1))
        if y < cells_number[1] - 1:
            ng.append((x+1, y+1))
    if y > 0 :
        ng.append((x, y-1))
    if y < cells_number[1] - 1:
        ng.append((x, y+1))
    return ng

@type_control(np.ndarray)
@timer
def evolution(cells):
    cells_new = cells.copy()
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            ng = neighbours(i, j, cells.shape)
            living_neighbours = sum([cells[elt] for elt in ng])
            if cells[i][j] == 0 and living_neighbours == 3:
                cells_new[i][j] = 1
            elif cells[i][j] == 1 and living_neighbours not in [2, 3]:
                cells_new[i][j] = 0
    return cells_new

@type_control(Canvas, tuple)
def generate(cv, square_size):
    global cells
    cells = evolution(cells)
    return update_view(cv, cells, square_size)

def canvas_click(cv, square_size, evt):
    global cells
    cell_x = floor(evt.x/square_size[0])
    cell_y = floor(evt.y/square_size[1])
    try:
        if cells[cell_x][cell_y] == 1:
            cells[cell_x][cell_y] = 0
            white((cell_x, cell_y), cv, square_size)
        elif cells[cell_x][cell_y] == 0:
            cells[cell_x][cell_y] = 1
            black((cell_x, cell_y), cv, square_size)
    except IndexError:
        pass
    

window = Tk()
cv = Canvas(window, width=window_width, height=window_height)
squares(cv, window_width, window_height, square_size)
cv.bind("<ButtonRelease-1>", partial(canvas_click, cv, square_size))
cv.pack()

btn = Button(window, text="Generate", command=partial(generate, cv, square_size))
btn.pack()

window.mainloop()