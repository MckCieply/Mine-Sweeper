import pygame
import random
pygame.init()

WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineSweeper")

BG_COLOR = "white"
ROWS, COLS = 30,30
MINES = 15

def get_neighbors(row, col, rows, cols):
    neighbors=[]

    if row > 0:                         #up
        neighbors.append((row -1, col))
    if row < len(rows) -1:              #down
        neighbors.append((row +1, col))
    if col > 0:                         #left
        neighbors.append((row, col -1))
    if col < len(cols) -1:              #right
        neighbors.append((row, col +1))

    if row > 0 and col > 0:                         #top-left
        neighbors.append((row -1, col -1))
    if row < len(rows) -1 and col < len(cols) -1:   #top-right 
        neighbors.append((row +1, col +1))
    if row < len(rows) -1 and col > 0:              #bot-left
        neighbors.append((row +1, col -1))
    if row > 0 and col < len(cols) -1:              #bot-right
        neighbors.append((row -1, col-1))

    return neighbors
    


def create_minefield(rows,cols, mines):
    field =[[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randrange(0,rows)
        col = random.randrange(0,cols)
        pos = row, col

        if pos in mine_positions:
            continue

        mine_positions.add(pos)
        field[row][col] = -1

def draw(window):
    window.fill(BG_COLOR)
    pygame.display.update()

def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window)
    pygame.quit()

if __name__ == "__main__":
    main()