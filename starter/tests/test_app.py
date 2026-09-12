import pytest

import app
import sudoku_logic


@pytest.fixture()
def client():
    app.app.config.update(TESTING=True)
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    app.CURRENT['completed'] = False
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    app.CURRENT['completed'] = False


def test_index_renders_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data
    assert b'id="sudoku-board"' in response.data
    assert b'<label for="difficulty">Difficulty</label>' in response.data
    assert b'<option value="Easy" selected>Easy</option>' in response.data
    assert b'<option value="Medium">Medium</option>' in response.data
    assert b'<option value="Hard">Hard</option>' in response.data


def test_new_game_returns_puzzle_with_requested_number_of_clues(client):
    response = client.get('/new?clues=40')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert len(puzzle) == 9
    assert all(len(row) == 9 for row in puzzle)
    assert sum(cell != 0 for row in puzzle for cell in row) == 40
    assert app.CURRENT['puzzle'] == puzzle
    assert app.CURRENT['solution'] is not None


@pytest.mark.parametrize('difficulty', ['Easy', 'Medium', 'Hard'])
def test_new_game_accepts_difficulty(client, difficulty):
    response = client.get(f'/new?difficulty={difficulty}')

    assert response.status_code == 200
    puzzle = response.get_json()['puzzle']
    assert sum(cell != 0 for row in puzzle for cell in row) == sudoku_logic.DIFFICULTY_CLUES[
        difficulty
    ]


def test_new_game_rejects_invalid_difficulty(client):
    response = client.get('/new?difficulty=Expert')

    assert response.status_code == 400
    assert 'Invalid difficulty' in response.get_json()['error']


def test_check_without_game_returns_error(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_marks_cells_that_differ_from_solution(client):
    client.get('/new')
    solution = app.CURRENT['solution']
    board = [row[:] for row in solution]
    board[0][0] = (solution[0][0] % 9) + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[0, 0]], 'completed': False}


def test_check_accepts_the_current_solution(client):
    client.get('/new')

    response = client.post('/check', json={'board': app.CURRENT['solution']})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [], 'completed': True}
    assert app.CURRENT['completed'] is True


def test_check_does_not_complete_an_incomplete_board_without_conflicts(client):
    client.get('/new')
    board = [row[:] for row in app.CURRENT['solution']]
    board[0][0] = 0

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [], 'completed': False}
    assert app.CURRENT['completed'] is False


@pytest.mark.parametrize(
    'payload',
    [
        None,
        {},
        {'board': [[0] * 9 for _ in range(8)]},
        {'board': [[0] * 9 for _ in range(9 - 1)] + [[0] * 8]},
        {'board': [[10] + [0] * 8] + [[0] * 9 for _ in range(8)]},
        {'board': [['1'] + [0] * 8] + [[0] * 9 for _ in range(8)]},
    ],
)
def test_check_rejects_malformed_or_invalid_board_payloads(client, payload):
    client.get('/new')

    response = client.post('/check', json=payload)

    assert response.status_code == 400
    assert 'error' in response.get_json()


def test_check_does_not_mark_empty_cells_as_incorrect(client):
    client.get('/new')

    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [], 'completed': False}


def test_hint_returns_a_valid_empty_cell_matching_the_solution(client):
    client.get('/new')
    puzzle = app.CURRENT['puzzle']
    solution = app.CURRENT['solution']

    response = client.post('/hint', json={'board': [row[:] for row in puzzle]})

    assert response.status_code == 200
    hint = response.get_json()
    assert puzzle[hint['row']][hint['col']] == 0
    assert hint['value'] == solution[hint['row']][hint['col']]


def test_hint_does_not_overwrite_prefilled_or_player_entered_values(client):
    client.get('/new')
    puzzle = app.CURRENT['puzzle']
    board = [row[:] for row in puzzle]
    player_cell = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle[row][col] == 0
    )
    board[player_cell[0]][player_cell[1]] = 9

    response = client.post('/hint', json={'board': board})

    assert response.status_code == 200
    hint = response.get_json()
    assert [hint['row'], hint['col']] != list(player_cell)
    assert all(
        board[row][col] == puzzle[row][col]
        for row in range(9)
        for col in range(9)
        if puzzle[row][col] != 0
    )


def test_hint_without_game_returns_error(client):
    response = client.post('/hint', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_hint_with_no_empty_cells_returns_error(client):
    client.get('/new')

    response = client.post('/hint', json={'board': app.CURRENT['solution']})

    assert response.status_code == 409
    assert response.get_json() == {'error': 'No empty cells remain'}


@pytest.mark.parametrize('payload', [None, {}, {'board': [[0] * 9 for _ in range(8)]}])
def test_hint_rejects_invalid_requests(client, payload):
    client.get('/new')

    response = client.post('/hint', json=payload)

    assert response.status_code == 400
    assert 'error' in response.get_json()