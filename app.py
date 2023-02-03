import pygame
import time

from grid import Grid
from construct import glider




if __name__ == "__main__":
    WIDTH = 500
    HEIGHT = 350

    # pygame related
    PIXEL_PER_GRID = 3
    window_size = (WIDTH * PIXEL_PER_GRID, HEIGHT * PIXEL_PER_GRID)
    pygame.init()
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Conway's Game of Life")


    # initialize grid
    grid = Grid(width=WIDTH, height=HEIGHT)
    grid.insert_construct(glider, (50, 50))
    while True:
        t1 = time.time()

        # pygame detect event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                happened_at = event.pos
                pixel_at = (
                    int(happened_at[0] / PIXEL_PER_GRID),
                    int(happened_at[1] / PIXEL_PER_GRID),
                )
                grid.randomize(pixel_at)

        # pygame rendering
        window.fill((0, 0, 0))
        indices = grid.get_ones()
        for (row, col) in indices:
            pygame.draw.rect(
                window,
                (255, 255, 255),
                pygame.Rect(
                    row * PIXEL_PER_GRID,
                    col * PIXEL_PER_GRID,
                    PIXEL_PER_GRID,
                    PIXEL_PER_GRID,
                ),
            )
        pygame.display.update()
        t2 = time.time()
        grid.step()
        t3 = time.time()

        print(
            f"Refresh rate: {1 / (t3 - t1)}. \n\t"
            # f"- Graphical rendering took {t2 - t1} sec.\n\t"
            # f"- Stepping took {t3 - t2} sec. "
        )
