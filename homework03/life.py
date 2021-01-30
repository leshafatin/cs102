import pathlib
import random

from typing import List, Optional, Tuple


Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    
    def __init__(
        self,
        size: Tuple[int, int],
        randomize: bool = True,
        max_generations: Optional[float]=float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []
        row, col = cell
        for row_num in [-1, 0, 1]:
            for col_num in [-1, 0, 1]:
                if (
                        (row_num, col_num) != (0, 0) and
                        0 <= row + row_num < self.rows and
                        0 <= col + col_num < self.cols
                ):
                    neighbors.append(self.curr_generation[row + row_num][col + col_num])

        return neighbors

    def get_next_generation(self) -> Grid:
        next_gen = self.create_grid(False)
        for i in range(self.rows):
            for j in range(self.cols):
                neighbours_count = self.get_neighbours((i, j)).count(1)
                if self.curr_generation[i][j] == 1 and neighbours_count in [2, 3]:
                    next_gen[i][j] = 1
                elif self.curr_generation[i][j] == 0 and neighbours_count == 3:
                    next_gen[i][j] = 1
        return next_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations == self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename) as file:
            for line in file.readlines():
                line = line.replace("\n", "")
                row = []
                for char in line:
                    row.append(int(char))
                grid.append(row)

        size = (len(grid), len(grid[0]))
        life = GameOfLife(size)
        life.curr_generation = grid
        return life

    def save(filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename) as file:
            for row in self.curr_generation:
                file.write("".join([str(char) for char in row]))
                file.write("\n")