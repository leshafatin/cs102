from typing import Tuple, List, Set, Optional
import multiprocessing, time, random

def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[n * k:n * (k + 1)] for k in range(n)]





def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [ grid[k][pos[1]] for k in range(len(grid)) ]


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    square_x = pos[0]//3
    square_y = pos[1]//3
    list = [ ]
    k = 3
    for i in range(square_x*k, square_x*k+k):
        for j in range(square_y*k, square_y*k+k):
            list.append(grid[i][j])
    return list


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    pos=''
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                pos = (i,j)
                break
    return pos

def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    a = set(get_row(grid,pos))
    b = set(get_col(grid,pos))
    c = set(get_block(grid,pos))

    numbers = {str(i) for i in range(1,10)}
    numbers = numbers.difference(a)
    numbers = numbers.difference(b)
    numbers = numbers.difference(c)

    return numbers



def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    pos = find_empty_positions(grid)

    if not pos:
        return grid

    possible = list(find_possible_values(grid, pos))

    for i in range(len(possible)):
        grid[pos[0]][pos[1]] = possible[i]
        if solve(grid):
            return grid
        else:
            grid[pos[0]][pos[1]] = '.'



def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    # TODO: Add doctests with bad puzzles
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            block = get_block(solution, (i,j))
            for k in range(9):
                if block.count(k) > 1:
                    return False
        row = get_row(solution, (i,0))
        col = get_col(solution, (0,i))
        if row.count('.')>0 or col.count('.')>0:
            return False

        for m in range(1,10):
            if row.count(str(m))>1 or col.count(str(m))>1:
                return False

    return True


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = [[str(((i * 3 + i // 3 + j) % 9 + 1)) for j in range(9)] for i in range(9)]

    for i in range(20):
        n1 = random.randrange(0, 9, 1)
        n2 = random.randrange(0, 9, 1)
        while (n1 == n2):
            n2 = random.randrange(0, 9, 1)

        for j in range(9):
            grid[n1][j], grid[n2][j] = grid[n2][j], grid[n1][j]

        for j in range(9):
            grid[j][n1], grid[j][n2] = grid[j][n2], grid[j][n1]

    if N < 81:
        while sum(1 for row in grid for e in row if e == '.') != (81 - N):
            grid[random.randint(0, 8)][random.randint(0, 8)] = '.'

    return grid




def run_solve(filename: str) -> None:
    grid = read_sudoku(filename)
    start = time.time()
    display(grid)
    solution = solve(grid)
    end = time.time()
    display(solution)
    print(f"{filename}: {end - start}")


if __name__ == '__main__':
    for filename in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        p = multiprocessing.Process(target=run_solve, args=(filename,))
        p.start()
