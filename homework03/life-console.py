import curses
from life import GameOfLife
from ui import UI
from time import sleep


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.screen = curses.initscr()

    def draw_borders(self) -> None:
        self.screen.border(0)

    def draw_grid(self) -> None:
        """ Отобразить состояние клеток. """
        for x, row in enumerate(self.life.curr_generation):
            for y, value in enumerate(row):
                sign = "0" if value == 1 else "."
                self.screen.addch(x + 1, y + 1, sign)
        self.screen.refresh()

    def run(self) -> None:
        self.draw_borders()

        running = True
        while running:
            self.draw_borders()
            self.draw_grid()
            self.screen.refresh()

            sleep(0.25)

            self.life.step()

        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 10))
    console = Console(game)
    console.run()