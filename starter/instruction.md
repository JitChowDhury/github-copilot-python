# GitHub Copilot Instructions — Flask Sudoku

## Project Goal

This project is a Flask-based Sudoku game that is being refactored from legacy Python code into a clean, maintainable, feature-rich application.

The final application must provide:

- A working 9x9 Sudoku board
- Easy, Medium, and Hard difficulty levels
- Puzzles with exactly one valid solution
- Locked prefilled cells
- Immediate visual feedback for invalid entries
- A Check button for identifying incorrect entries
- A Hint button that fills and locks one correct cell
- A completion message when the puzzle is solved
- A game timer
- A Top 10 fastest-times leaderboard
- Player name, completion time, difficulty, and hint count in leaderboard entries
- Persistent leaderboard data using browser localStorage
- Dark mode
- Responsive desktop and mobile layouts
- Accessible and readable controls

## Development Principles

Follow these principles when modifying the project:

1. Prefer clear, readable, maintainable Python and JavaScript.
2. Use modular functions and components with clear responsibilities.
3. Avoid unnecessary duplication.
4. Keep game logic separate from presentation and UI logic where practical.
5. Prefer descriptive names over abbreviated variable or function names.
6. Add comments when they clarify non-obvious logic, algorithms, or design decisions.
7. Do not add comments that merely restate obvious code.
8. Use consistent formatting throughout the project.
9. Handle expected errors gracefully and provide useful feedback.
10. Avoid introducing unnecessary dependencies.
11. Preserve existing functionality unless a requirement specifically calls for changing it.
12. Make the smallest reasonable change needed to implement each feature.

## Sudoku Rules and Correctness

Sudoku logic must be reliable and deterministic where appropriate.

- A valid Sudoku solution contains the numbers 1–9 exactly once in every row.
- A valid Sudoku solution contains the numbers 1–9 exactly once in every column.
- A valid Sudoku solution contains the numbers 1–9 exactly once in every 3x3 subgrid.
- Generated puzzles must have exactly one solvable solution.
- Difficulty levels must meaningfully change the number of prefilled cells.
- Prefilled cells must not be editable by the player.
- Hints must always place a value that belongs to the puzzle's unique solution.

Do not assume that a puzzle is uniquely solvable without actually validating the solution count.

## Testing

Testing is required before major refactoring and should be maintained as the project evolves.

- Establish a baseline test suite before changing the legacy implementation.
- Run the tests after refactoring and feature changes.
- Do not remove tests simply to make the test suite pass.
- When fixing a failing test, determine whether the implementation or the test is incorrect before changing either.
- Add tests for important new functionality when practical.
- Tests should verify behavior rather than implementation details whenever possible.

## Frontend and Accessibility

Use semantic HTML and accessible controls.

- Buttons should have clear labels.
- Form controls should have appropriate labels.
- Keyboard interaction should remain possible.
- Maintain sufficient contrast in both light and dark modes.
- Do not rely on color alone to communicate important information.
- Ensure the interface remains usable on small screens.
- Avoid layout shifts when displaying validation feedback.

## Styling

The Sudoku board should:

- Maintain a clear 9x9 structure.
- Visually distinguish the nine 3x3 subgrids using alternating styling.
- Remain aligned when the viewport changes size.
- Scale appropriately between desktop and mobile screens.
- Remain readable in light and dark modes.

Avoid unnecessary visual complexity.

## Copilot Behavior

When assisting with this project:

1. First inspect the existing code before proposing major changes.
2. Explain important architectural or algorithmic decisions when they are not obvious.
3. Do not rewrite unrelated parts of the application.
4. Preserve working functionality while implementing new requirements.
5. Prefer incremental changes that can be tested after implementation.
6. If there are multiple reasonable approaches, briefly explain the trade-offs.
7. Do not assume a library or dependency is available without checking the project first.
8. Flag potentially risky changes before making them.
9. When a generated solution is uncertain or complex, suggest an appropriate test or verification step.
10. Do not hide errors or silently ignore failing tests.

## Code Review Expectations

Treat Copilot suggestions as proposals rather than automatically correct solutions.

Before accepting a substantial change:

- Check that it satisfies the project requirements.
- Check that it fits the existing architecture.
- Check for regressions.
- Run the relevant tests.
- Reject or modify suggestions that introduce unnecessary complexity, incorrect behavior, or violations of these instructions.

## Project Scope

Focus on completing the Sudoku application and its required functionality.

Do not introduce unrelated frameworks, services, databases, authentication systems, or external infrastructure unless a project requirement explicitly requires them.