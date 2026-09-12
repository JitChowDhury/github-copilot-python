from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'completed': False,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    try:
        clues = int(request.args.get('clues', 35))
        difficulty = request.args.get('difficulty')
        puzzle, solution = sudoku_logic.generate_puzzle(
            clues=clues,
            difficulty=difficulty,
        )
    except ValueError as error:
        return jsonify({'error': str(error)}), 400

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['completed'] = False
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'board' not in data:
        return jsonify({'error': 'Request must contain a board'}), 400

    board = data['board']
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Board must have 9 rows'}), 400
    if any(
        not isinstance(row, list) or len(row) != sudoku_logic.SIZE
        for row in board
    ):
        return jsonify({'error': 'Each board row must contain 9 cells'}), 400
    if any(
        not isinstance(value, int) or isinstance(value, bool)
        or not 0 <= value <= sudoku_logic.SIZE
        for row in board
        for value in row
    ):
        return jsonify({'error': 'Board cells must be integers from 0 to 9'}), 400

    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != 0 and board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    completed = (
        not incorrect
        and all(
            1 <= board[row][col] <= sudoku_logic.SIZE
            and board[row][col] == solution[row][col]
            for row in range(sudoku_logic.SIZE)
            for col in range(sudoku_logic.SIZE)
        )
    )
    if completed:
        CURRENT['completed'] = True

    return jsonify({'incorrect': incorrect, 'completed': completed})

@app.route('/hint', methods=['POST'])
def request_hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'board' not in data:
        return jsonify({'error': 'Request must contain a board'}), 400

    board = data['board']
    if not isinstance(board, list) or len(board) != sudoku_logic.SIZE:
        return jsonify({'error': 'Board must have 9 rows'}), 400
    if any(
        not isinstance(row, list) or len(row) != sudoku_logic.SIZE
        for row in board
    ):
        return jsonify({'error': 'Each board row must contain 9 cells'}), 400
    if any(
        not isinstance(value, int) or isinstance(value, bool)
        or not 0 <= value <= sudoku_logic.SIZE
        for row in board
        for value in row
    ):
        return jsonify({'error': 'Board cells must be integers from 0 to 9'}), 400

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):
            if puzzle[row][col] == sudoku_logic.EMPTY and board[row][col] == sudoku_logic.EMPTY:
                return jsonify({
                    'row': row,
                    'col': col,
                    'value': solution[row][col],
                })

    return jsonify({'error': 'No empty cells remain'}), 409

if __name__ == '__main__':
    app.run(debug=True)