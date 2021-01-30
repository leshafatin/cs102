import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.height = self.life.rows * self.cell_size
        self.width = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def pick_a_life(self, cell):
        cell_x = cell[0] // self.cell_size
        cell_y = cell[1] // self.cell_size
        self.life.curr_generation[cell_x][cell_y] = 0 if self.life.curr_generation[cell_x][cell_y] else 1


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for x, row in enumerate(self.life.curr_generation):
            for y, value in enumerate(row):
                coord_x = x * self.cell_size + 1
                coord_y = y * self.cell_size + 1

                colour = pygame.Color("green") if value == 1 else pygame.Color("white")

                pygame.draw.rect(
                    self.screen,
                    colour,
                    (coord_y, coord_x, self.cell_size - 1, self.cell_size - 1)
                )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    reversed_pos = pygame.mouse.get_pos()
                    pos = reversed_pos[1], reversed_pos[0]
                    self.pick_a_life(pos)
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused

            if not paused:
                self.life.step()

            self.draw_lines()
            self.draw_grid()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


def main():
    game = GameOfLife(size=(40, 40))
    app = GUI(game)
    app.run()

if __name__ == '__main__':
    main()
