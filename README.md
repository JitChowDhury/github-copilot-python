# Refactor a Sudoku Game written in Python Flask

This repository contains a completed Sudoku game built with Python, Flask, HTML, CSS, and JavaScript.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Dependencies

```
- Modern web browser (Chrome, Firefox, Edge, etc.)
- Python 3
```

### Installation

1. Fork this repository to your GitHub account. (You can use the "Fork" button on the top right corner of the repository page.)

2. Clone your forked repository to your local machine.

3. Open a terminal window and navigate to the `starter` directory.

4. Create a Python virtual environment and activate it (optional but highly recommended).

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
```

5. Install required Python packages.

```bash
pip install -r requirements.txt
```

6. Run the Flask app.

```bash
python app.py
```

7. Open http://127.0.0.1:5000 in your browser.

## Features

- Generates Sudoku puzzles with a unique solution.
- Provides Easy, Medium, and Hard difficulty levels.
- Locks prefilled cells so they cannot be edited.
- Gives immediate feedback for invalid moves.
- Includes a Check button that highlights incorrect cells.
- Provides hints, tracks the hint count, and locks hinted cells.
- Displays a completion message when the puzzle is solved.
- Includes a puzzle timer.
- Stores a Top 10 leaderboard in browser `localStorage`.
- Supports light and dark modes with accessible UI states.
- Provides a responsive interface for desktop and mobile screens.

## Testing

Run the test suite from the `starter` directory:

```bash
python -m pytest -q
```

The current test suite contains 47 tests, and all tests should pass.

### JavaScript Validation

From the `starter` directory, validate the JavaScript syntax with:

```bash
node --check static/main.js
```

## Screenshots

Copilot milestone evidence is available in the `SCREENSHOTS` folder.
