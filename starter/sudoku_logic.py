import copy
import random

SIZE = 9
EMPTY = 0

DIFFICULTY_CLUES = {
    "Easy": 45,
    "Medium": 35,
    "Hard": 25,
}


def deep_copy(board):
    return copy.deepcopy(board)


def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def validate_board(board):
    """Return whether board has a valid Sudoku shape and partial state."""
    if not isinstance(board, (list, tuple)) or len(board) != SIZE:
        return False

    if any(
        not isinstance(row, (list, tuple)) or len(row) != SIZE
        for row in board
    ):
        return False

    if any(
        not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= SIZE
        for row in board
        for value in row
    ):
        return False

    for row in board:
        values = [value for value in row if value != EMPTY]
        if len(values) != len(set(values)):
            return False

    for column in range(SIZE):
        values = [board[row][column] for row in range(SIZE) if board[row][column] != EMPTY]
        if len(values) != len(set(values)):
            return False

    for start_row in range(0, SIZE, 3):
        for start_col in range(0, SIZE, 3):
            values = [
                board[row][column]
                for row in range(start_row, start_row + 3)
                for column in range(start_col, start_col + 3)
                if board[row][column] != EMPTY
            ]
            if len(values) != len(set(values)):
                return False

    return True


is_valid_board = validate_board


def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def _find_empty_cell(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None


def solve_board(board):
    """Fill board in place and return whether a solution was found."""
    if not validate_board(board):
        return False

    empty_cell = _find_empty_cell(board)
    if empty_cell is None:
        return True

    row, col = empty_cell
    possible = list(range(1, SIZE + 1))
    random.shuffle(possible)
    for candidate in possible:
        if is_safe(board, row, col, candidate):
            board[row][col] = candidate
            if solve_board(board):
                return True
            board[row][col] = EMPTY
    return False


def fill_board(board):
    return solve_board(board)


def count_solutions(board, limit=2):
    """Count solutions, stopping when the count reaches the requested limit."""
    if not validate_board(board) or limit < 1:
        return 0

    working_board = deep_copy(board)
    solution_count = 0

    def search():
        nonlocal solution_count
        empty_cell = _find_empty_cell(working_board)
        if empty_cell is None:
            solution_count += 1
            return solution_count >= limit

        row, col = empty_cell
        for candidate in range(1, SIZE + 1):
            if is_safe(working_board, row, col, candidate):
                working_board[row][col] = candidate
                if search():
                    return True
                working_board[row][col] = EMPTY
        return False

    search()
    return solution_count

def remove_cells(board, clues):
    cells_to_remove = SIZE * SIZE - clues
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    for row, col in positions:
        if cells_to_remove == 0:
            break
        value = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) == 1:
            cells_to_remove -= 1
        else:
            board[row][col] = value

def generate_puzzle(clues=35, difficulty=None):
    if difficulty is not None:
        try:
            clues = DIFFICULTY_CLUES[difficulty]
        except (KeyError, TypeError):
            supported = ", ".join(DIFFICULTY_CLUES)
            raise ValueError(
                f"Invalid difficulty '{difficulty}'. Choose one of: {supported}."
            )

    board = create_empty_board()
    if not fill_board(board):
        raise RuntimeError("Unable to generate a Sudoku solution")
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution
