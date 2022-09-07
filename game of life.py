import pygame
from pygame.locals import *
import sys

ALIVE = (0, 252, 0)
DEAD = (0, 0, 0)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
X = 100
Y = 100
CELL_WIDTH = SCREEN_WIDTH/X
CELL_HEIGHT = SCREEN_HEIGHT/Y


class Cell:
    def __init__(self, x, y):
        self.state = DEAD
        self.rect = Rect(x*CELL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)

        
    def draw(self, c_screen):
        pygame.draw.rect(c_screen, self.state, self.rect)


class Grid:
    def __init__(self, gx, gy):
        self.X = gx
        self.Y = gy
        self.rows = []
        for y in range(gy):
            self.rows.append([])
            for x in range(gx):
                self.rows[y].append(Cell(x, y))

    def get_state(self, gy, gx):
        return self.rows[gy % self.Y][gx % self.X].state

    def set_state(self, gy, gx, state):
        self.rows[gy % self.Y][gx % self.X].state = state

    def draw(self, g_screen):
        for row in self.rows:
            for cell in row:
                cell.draw(g_screen)


def count_neighbors(y, x, get_state):
    n_ = get_state(y-1, x+0)
    ne = get_state(y-1, x+1)
    e_ = get_state(y+0, x+1)
    se = get_state(y+1, x+1)
    s_ = get_state(y+1, x+0)
    sw = get_state(y+1, x-1)
    w_ = get_state(y+0, x-1)
    nw = get_state(y-1, x-1)

    neighbors_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbors_states:
        if state == ALIVE:
            count += 1
    return count


def next_state(state, neighbors):
    if state == ALIVE:
        if neighbors < 2:
            return DEAD
        elif neighbors > 3:
            return DEAD
    else:
        if neighbors ==3:
            return ALIVE
    return state


def step_cell(y, x, get_state,set_state):
    state = get_state(y, x)
    neighbors = count_neighbors(y, x, get_state)
    new_state = next_state(state, neighbors)
    set_state(y, x, new_state)


def simulate(gd):
    new_grid = Grid(gd.X, gd.Y)
    for y in range(gd.Y):
        for x in range(gd.X):
            step_cell(y, x, gd.get_state, new_grid.set_state)
    return new_grid


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game of Life")
    frame_rate = pygame.time.Clock()

    grid = Grid(X, Y)
    grid.set_state(2, 4, ALIVE)
    grid.set_state(2, 2, ALIVE)
    grid.set_state(3, 3, ALIVE)
    grid.set_state(3, 4, ALIVE)
    grid.set_state(4, 4, ALIVE)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        grid.draw(screen)
        grid = simulate(grid)
        pygame.display.update()
        frame_rate.tick(10)

