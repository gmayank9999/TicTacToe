# How the Minimax Algorithm Works in This Tic-Tac-Toe AI

## Overview
Yes, this project **does follow the Minimax algorithm** for AI decision-making. The AI is **unbeatable** because it evaluates all possible future game states before making each move.

---

## What is Minimax?

Minimax is a decision-making algorithm used in turn-based games. It works by:
1. **Exploring all possible future moves** (game tree)
2. **Evaluating each outcome** with a score
3. **Choosing the move** that maximizes the AI's chances of winning

---

## How It Works in This Project

### 1. **The Core Minimax Function** (lines 77-104)

```python
def minimax(minimax_board, depth, is_max):
```

**Parameters:**
- `minimax_board`: A copy of the game board
- `depth`: How many moves deep we are in the tree
- `is_max`: `True` for AI's turn (maximize), `False` for player's turn (minimize)

**Base Cases (Terminal States):**
- **AI wins** → Returns `10 - depth` (positive score, prefers faster wins)
- **Player wins** → Returns `depth - 10` (negative score, prefers slower losses)
- **Draw** → Returns `0` (neutral)

**Recursive Cases:**
- **When `is_max = True`** (AI's turn):
  - Try every possible move
  - Evaluate the resulting position recursively
  - Return the **maximum** score (best for AI)
  
- **When `is_max = False`** (Player's turn):
  - Assume the player plays optimally
  - Try every possible player move
  - Return the **minimum** score (worst for AI, best for player)

**Key Point:** The algorithm uses **backtracking** - after evaluating a move, it undoes it (`board[row][col] = 0`) to try other moves.

---

### 2. **The Best Move Finder** (lines 106-121)

```python
def best_move():
```

This function:
1. Tries **every empty square** on the board
2. For each move, calls `minimax()` to evaluate all future possibilities
3. Picks the move with the **highest score**
4. Makes that move

---

## Visual Example

Imagine this game state:
```
X _ _
_ O _
_ _ _
```

The AI (X) needs to find the best move. Minimax will:

1. Try placing X at position (0,1):
   - Evaluate all possible player responses
   - Evaluate all AI responses to those
   - ...and so on until game ends
   - Get a score (e.g., +8 = good for AI)

2. Try placing X at position (1,2):
   - Evaluate all possible outcomes
   - Get a score (e.g., +10 = even better!)

3. Try all other positions...

4. Choose the move with the **highest score**

---

## Why It's Unbeatable

The AI is **unbeatable** (not just hard to beat) because:

1. **Complete information**: It sees all possible future moves
2. **Optimal play**: It always chooses the best move available
3. **No mistakes**: Unlike humans, it never makes a tactical error

**The best you can do is draw!** The AI will:
- Block your winning moves
- Take winning opportunities
- Force optimal responses

---

## Depth Optimization

Notice the `depth` parameter in the score calculation:
- `10 - depth` for AI wins
- `depth - 10` for player wins

This means:
- **Winning in 2 moves** (depth=2) scores `8`
- **Winning in 4 moves** (depth=4) scores `6`

The AI prefers **faster wins** because shorter paths get higher scores!

---

## Algorithm Complexity

- **Time Complexity**: O(b^d)
  - `b` = branching factor (number of empty squares)
  - `d` = depth (moves until game ends)
  - For Tic-Tac-Toe: maximum 9 moves, so this is manageable

- **Space Complexity**: O(d)
  - Depth of recursion (maximum 9 levels for Tic-Tac-Toe)

---

## Summary

✅ **Yes, this project uses Minimax!**

The algorithm:
1. Recursively explores all possible game states
2. Scores each terminal state (win/loss/draw)
3. Propagates scores up the game tree
4. AI chooses moves that maximize its score
5. Assumes the player plays optimally (minimizes AI's score)

This makes the AI **perfect** at Tic-Tac-Toe - the best possible outcome for a human player is a draw!

