import pytest

import sudoku_logic


VALID_PARTIAL_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def test_create_empty_board_has_nine_rows_of_nine_empty_cells():
    board = sudoku_logic.create_empty_board()

    assert board == [[0] * 9 for _ in range(9)]


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 6) is True


def test_fill_board_creates_a_valid_complete_board():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert all(sorted(row) == list(range(1, 10)) for row in board)
    assert all(
        sorted(board[row][column] for row in range(9)) == list(range(1, 10))
        for column in range(9)
    )


def test_generate_puzzle_returns_solution_and_requested_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=45)

    assert len(puzzle) == 9
    assert len(solution) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert all(len(row) == 9 for row in solution)
    assert sum(cell != 0 for row in puzzle for cell in row) == 45
    assert all(
        puzzle[row][column] in (0, solution[row][column])
        for row in range(9)
        for column in range(9)
    )


def test_validate_board_accepts_valid_partial_board():
    assert sudoku_logic.validate_board(VALID_PARTIAL_BOARD) is True
    assert sudoku_logic.is_valid_board(VALID_PARTIAL_BOARD) is True


@pytest.mark.parametrize(
    "board",
    [
        [[0] * 9 for _ in range(8)],
        [[0] * 9 for _ in range(9 - 1)] + [[0] * 8],
        [[10] + [0] * 8] + [[0] * 9 for _ in range(8)],
        [[1, 1] + [0] * 7] + [[0] * 9 for _ in range(8)],
        [[1] + [0] * 8, [1] + [0] * 8] + [[0] * 9 for _ in range(7)],
        [[1, 0, 0] + [0] * 6, [0, 1, 0] + [0] * 6, [0, 0, 1] + [0] * 6]
        + [[0] * 9 for _ in range(6)],
    ],
)
def test_validate_board_rejects_invalid_shape_values_and_duplicates(board):
    assert sudoku_logic.validate_board(board) is False


def test_count_solutions_returns_zero_for_unsatisfiable_valid_board():
    board = [[0] * 9 for _ in range(9)]
    board[0] = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    board[1][0] = 9

    assert sudoku_logic.count_solutions(board) == 0


def test_count_solutions_returns_one_for_unique_board():
    assert sudoku_logic.count_solutions(VALID_PARTIAL_BOARD) == 1


def test_count_solutions_stops_at_two_for_multiple_solution_board():
    assert sudoku_logic.count_solutions(sudoku_logic.create_empty_board()) == 2


def test_generated_puzzle_has_exactly_one_solution_and_matches_solution():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=45)

    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sudoku_logic.validate_board(solution) is True
    assert sudoku_logic.count_solutions(solution) == 1
    assert all(
        puzzle[row][column] in (0, solution[row][column])
        for row in range(9)
        for column in range(9)
    )


@pytest.mark.parametrize("difficulty", ["Easy", "Medium", "Hard"])
def test_generate_puzzle_accepts_each_difficulty(difficulty):
    puzzle, _ = sudoku_logic.generate_puzzle(difficulty=difficulty)

    assert sum(cell != 0 for row in puzzle for cell in row) == sudoku_logic.DIFFICULTY_CLUES[
        difficulty
    ]


def test_generate_puzzle_rejects_invalid_difficulty():
    with pytest.raises(ValueError, match="Invalid difficulty"):
        sudoku_logic.generate_puzzle(difficulty="Expert")


def test_difficulty_levels_have_decreasing_prefilled_cells():
    clue_counts = {
        difficulty: sum(
            cell != 0
            for row in sudoku_logic.generate_puzzle(difficulty=difficulty)[0]
            for cell in row
        )
        for difficulty in sudoku_logic.DIFFICULTY_CLUES
    }

    assert clue_counts["Easy"] > clue_counts["Medium"] > clue_counts["Hard"]


@pytest.mark.parametrize("difficulty", ["Easy", "Medium", "Hard"])
def test_each_difficulty_has_one_consistent_solution(difficulty):
    puzzle, solution = sudoku_logic.generate_puzzle(difficulty=difficulty)

    assert sudoku_logic.count_solutions(puzzle) == 1
    assert sudoku_logic.validate_board(solution) is True
    assert all(
        puzzle[row][column] in (0, solution[row][column])
        for row in range(9)
        for column in range(9)
    )