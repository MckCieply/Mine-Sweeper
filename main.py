import pygame
pygame.init()

WIDTH, HEIGHT = 500, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MineSweeper")

BG_COLOR = "white"

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