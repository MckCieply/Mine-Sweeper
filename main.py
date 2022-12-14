from venv import create
import pygame
import random
from queue import Queue

from sklearn import neighbors
pygame.init()

WIDTH, HEIGHT = 600, 700

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineSweeper")

BG_COLOR = "white"
ROWS, COLS = 15, 15
BOMBS = 15
SIZE = WIDTH / ROWS

NUM_FONT = pygame.font.SysFont('comicsans', 20)
NUM_COLORS = {1: "black", 2: "green", 3: "red", 4: "orange",
              5: "yellow", 6: "purple", 7: "blue", 8: "pink"}
RECT_COLOR = (200,200,200)
CLICKED_RECT_COLOR = (140,140,140)
FLAG_RECT_COLOR = "green"

def get_neighbors(row, col, rows, cols):
    neighbors=[]

    if row > 0:                         #up
        neighbors.append((row -1, col))
    if row < rows -1:              #down
        neighbors.append((row +1, col))
    if col > 0:                         #left
        neighbors.append((row, col -1))
    if col < cols -1:              #right
        neighbors.append((row, col +1))

    if row > 0 and col > 0:                         #top-left
        neighbors.append((row -1, col -1))
    if row < rows -1 and col < cols -1:   #top-right 
        neighbors.append((row +1, col +1))
    if row < rows -1 and col > 0:              #bot-left
        neighbors.append((row +1, col -1))
    if row > 0 and col < cols -1:              #bot-right
        neighbors.append((row -1, col +1))

    return neighbors
    


def create_minefield(rows, cols, mines):
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

    for mine in mine_positions:
        neighbors = get_neighbors(*mine, rows,cols)
        for r, c in neighbors:
            field[r][c] +=1
    
    return field

def draw(window, field, cover_field):
    window.fill(BG_COLOR)

    SIZE = WIDTH / ROWS
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2
            if is_flag:
                pygame.draw.rect(window, FLAG_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "black", (x, y, SIZE, SIZE), 1)
                continue
            
            if is_covered:
                pygame.draw.rect(window, RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "black", (x, y, SIZE, SIZE), 1)
                continue

            else:
                pygame.draw.rect(window, CLICKED_RECT_COLOR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "black", (x, y, SIZE, SIZE), 1)

            if value > 0:
                text = NUM_FONT.render(str(value), 1, NUM_COLORS[value])
                window.blit(text, (x+ (SIZE/2 -text.get_width()/2), y+(SIZE/2 - text.get_height()/2)))
    pygame.display.update()

def get_grid_pos(mouse_pos):
    mx, my = mouse_pos
    row = int(my // SIZE)
    col = int(mx // SIZE)
    
    return row, col

def uncover_from_pos(row, col, cover_field, field):
    q = Queue()
    q.put((row, col))
    visited = set()
    
    while not q.empty():
        current = q.get()
        
        neighbors = get_neighbors(*current, ROWS, COLS)
        for r, c in neighbors:
            if (r, c) in visited:
                continue
            value = field[r][c]
            cover_field[r][c] = 1
            if value == 0:
                q.put((r, c))
                
            visited.add((r, c))
            

def main():
    run = True
    field = create_minefield(ROWS,COLS, BOMBS)
    cover_field =[[0 for _ in range(COLS)] for _ in range(ROWS)]
    flag_positions = set()
    flags = BOMBS
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_grid_pos(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0]:
                    cover_field[row][col] = 1
                    uncover_from_pos(row,col, cover_field, field)
                elif mouse_pressed[2]:
                    if cover_field[row][col] == -2:
                        cover_field[row][col] = 0
                        flags += 1
                    else: 
                        flags -= 1
                        cover_field[row][col] = -2      
                
        draw(window, field, cover_field)
    pygame.quit()

if __name__ == "__main__":
    main()