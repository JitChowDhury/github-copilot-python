// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_STORAGE_KEY = 'sudokuLeaderboard';
const THEME_STORAGE_KEY = 'sudokuTheme';
const VALID_DIFFICULTIES = ['Easy', 'Medium', 'Hard'];
let puzzle = [];
let currentDifficulty = 'Easy';
let hintCount = 0;
let gameCompleted = false;
let scoreSubmitted = false;
let completedElapsedSeconds = null;
let timerInterval = null;
let timerStartedAt = null;

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
  const toggle = document.getElementById('dark-mode-toggle');
  toggle.setAttribute('aria-pressed', String(isDark));
  toggle.innerText = isDark ? 'Dark mode: On' : 'Dark mode: Off';
}

function initializeTheme() {
  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  } catch (error) {
    // Use the system preference when theme storage is unavailable.
  }
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  applyTheme(savedTheme === 'dark' || (savedTheme !== 'light' && systemPrefersDark) ? 'dark' : 'light');
}

function toggleTheme() {
  const isDark = document.documentElement.dataset.theme !== 'dark';
  const theme = isDark ? 'dark' : 'light';
  applyTheme(theme);
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch (error) {
    // Theme still applies for the current page when storage is unavailable.
  }
}

function formatElapsedTime(seconds) {
  const totalSeconds = Math.max(0, Math.floor(seconds));
  const minutes = Math.floor(totalSeconds / 60);
  const remainingSeconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

function updateTimer() {
  if (timerStartedAt === null) return;
  const elapsedSeconds = (Date.now() - timerStartedAt) / 1000;
  document.getElementById('timer').innerText = formatElapsedTime(elapsedSeconds);
}

function getElapsedSeconds() {
  if (timerStartedAt === null) return completedElapsedSeconds;
  return Math.max(0, Math.floor((Date.now() - timerStartedAt) / 1000));
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
  updateTimer();
  timerStartedAt = null;
}

function startTimer() {
  stopTimer();
  completedElapsedSeconds = null;
  timerStartedAt = Date.now();
  document.getElementById('timer').innerText = formatElapsedTime(0);
  timerInterval = setInterval(updateTimer, 1000);
}

function normalizeScore(score) {
  if (!score || typeof score !== 'object' || Array.isArray(score)) return null;
  if (!Number.isInteger(score.time) || score.time < 0) return null;
  if (!VALID_DIFFICULTIES.includes(score.difficulty)) return null;
  if (!Number.isInteger(score.hints) || score.hints < 0) return null;
  if (typeof score.name !== 'string') return null;
  return {
    name: score.name.trim() || 'Player',
    time: score.time,
    difficulty: score.difficulty,
    hints: score.hints
  };
}

function sortScores(scores) {
  return scores.slice().sort((first, second) => first.time - second.time);
}

function loadScores() {
  try {
    const storedScores = localStorage.getItem(LEADERBOARD_STORAGE_KEY);
    if (!storedScores) return [];
    const parsedScores = JSON.parse(storedScores);
    if (!Array.isArray(parsedScores)) return [];
    return sortScores(parsedScores.map(normalizeScore).filter(Boolean)).slice(0, 10);
  } catch (error) {
    return [];
  }
}

function saveScores(scores) {
  try {
    const validScores = scores.map(normalizeScore).filter(Boolean);
    localStorage.setItem(
      LEADERBOARD_STORAGE_KEY,
      JSON.stringify(sortScores(validScores).slice(0, 10))
    );
  } catch (error) {
    // localStorage may be unavailable or disabled in the browser.
  }
}

function addScore(score) {
  const normalizedScore = normalizeScore(score);
  if (!normalizedScore) return loadScores();
  const scores = sortScores([...loadScores(), normalizedScore]).slice(0, 10);
  saveScores(scores);
  return scores;
}

function renderLeaderboard(scores = loadScores()) {
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  scores.forEach((score, index) => {
    const row = document.createElement('tr');
    [index + 1, score.name, formatElapsedTime(score.time), score.difficulty, score.hints]
      .forEach((value) => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.appendChild(cell);
      });
    body.appendChild(row);
  });
}

function submitCompletedScore() {
  if (scoreSubmitted || completedElapsedSeconds === null) return;
  scoreSubmitted = true;
  const nameInput = document.getElementById('player-name');
  addScore({
    name: nameInput.value,
    time: completedElapsedSeconds,
    difficulty: currentDifficulty,
    hints: hintCount
  });
  renderLeaderboard();
}

function completeGame(inputs) {
  if (gameCompleted) return;
  gameCompleted = true;
  completedElapsedSeconds = getElapsedSeconds();
  stopTimer();
  for (const input of inputs) {
    if (!input.disabled) input.disabled = true;
  }
  submitCompletedScore();
  showMessage('Congratulations! You solved it!', '#388e3c');
}

function showMessage(message, color = '#d32f2f') {
  const msg = document.getElementById('message');
  msg.style.color = color === '#388e3c' ? 'var(--success)' : 'var(--danger)';
  msg.innerText = message;
}

function getBoardFromInputs(inputs) {
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const value = inputs[i * SIZE + j].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return board;
}

function isValidEntry(board, row, col) {
  const value = board[row][col];
  if (value === 0) return true;

  for (let index = 0; index < SIZE; index++) {
    if (index !== col && board[row][index] === value) return false;
    if (index !== row && board[index][col] === value) return false;
  }

  const startRow = row - row % 3;
  const startCol = col - col % 3;
  for (let boxRow = startRow; boxRow < startRow + 3; boxRow++) {
    for (let boxCol = startCol; boxCol < startCol + 3; boxCol++) {
      if ((boxRow !== row || boxCol !== col) && board[boxRow][boxCol] === value) {
        return false;
      }
    }
  }
  return true;
}

function updateCellValidation(input, board) {
  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);
  input.classList.toggle('invalid', !isValidEntry(board, row, col));
  input.classList.remove('incorrect');
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      const regionRow = Math.floor(i / 3);
      const regionColumn = Math.floor(j / 3);
      input.classList.add((regionRow + regionColumn) % 2 === 0 ? 'region-even' : 'region-odd');
      if (j % 3 === 2 && j < SIZE - 1) input.classList.add('region-right');
      if (i % 3 === 2 && i < SIZE - 1) input.classList.add('region-bottom');
      input.dataset.row = i;
      input.dataset.col = j;
      input.inputMode = 'numeric';
      input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
        updateCellValidation(e.target, getBoardFromInputs(inputs));
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  hintCount = 0;
  gameCompleted = false;
  scoreSubmitted = false;
  completedElapsedSeconds = null;
  document.getElementById('hint-count').innerText = 'Hints used: 0';
  document.getElementById('player-name').value = '';
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
        inp.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}, prefilled`);
      } else {
        inp.value = '';
        inp.disabled = false;
        inp.classList.remove('prefilled', 'hinted', 'incorrect', 'invalid');
      }
    }
  }
}

async function requestHint() {
  if (gameCompleted) return;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getBoardFromInputs(inputs);
  try {
    const res = await fetch('/hint', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Unable to request a hint.');
    }

    const index = data.row * SIZE + data.col;
    const input = inputs[index];
    if (input.disabled || board[data.row][data.col] !== 0) {
      throw new Error('The hint returned an unavailable cell.');
    }
    input.value = data.value;
    input.disabled = true;
    input.className = 'sudoku-cell hinted';
    input.setAttribute('aria-label', `Row ${data.row + 1}, column ${data.col + 1}, hint`);
    hintCount += 1;
    document.getElementById('hint-count').innerText = `Hints used: ${hintCount}`;
    showMessage('Hint added.', '#388e3c');
  } catch (error) {
    showMessage(error.message || 'Unable to request a hint.');
  }
}

async function newGame() {
  const difficultySelector = document.getElementById('difficulty');
  currentDifficulty = difficultySelector.value;
  const query = new URLSearchParams({difficulty: currentDifficulty});

  try {
    const res = await fetch(`/new?${query.toString()}`);
    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Unable to start a new game.');
    }
    stopTimer();
    renderPuzzle(data.puzzle);
    startTimer();
    showMessage('');
  } catch (error) {
    showMessage(error.message || 'Unable to start a new game.');
  }
}

async function checkSolution() {
  if (gameCompleted) return;
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getBoardFromInputs(inputs);
  try {
    const res = await fetch('/check', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({board})
    });
    const data = await res.json();
    if (!res.ok || data.error) {
      throw new Error(data.error || 'Unable to check the solution.');
    }
    if (data.completed === true) {
      completeGame(inputs);
      return;
    }

    const incorrect = new Set(
      (Array.isArray(data.incorrect) ? data.incorrect : [])
        .map(x => x[0] * SIZE + x[1])
    );
    for (let idx = 0; idx < inputs.length; idx++) {
      const inp = inputs[idx];
      if (inp.disabled) continue;
      inp.classList.toggle('incorrect', incorrect.has(idx));
    }
    if (incorrect.size === 0) {
      showMessage('The board is incomplete.');
    } else {
      showMessage('Some cells are incorrect.');
    }
  } catch (error) {
    showMessage(error.message || 'Unable to check the solution.');
  }
}

// Wire buttons
window.addEventListener('load', () => {
  const difficultySelector = document.getElementById('difficulty');
  difficultySelector.addEventListener('change', () => {
    currentDifficulty = difficultySelector.value;
  });
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint').addEventListener('click', requestHint);
  renderLeaderboard();
  initializeTheme();
  document.getElementById('dark-mode-toggle').addEventListener('click', toggleTheme);
  // initialize
  newGame();
});