# Connect 4 Game

A Python implementation of the classic Connect 4 game with multiple gameplay modes and an intelligent computer opponent.

## Features

- **Multiple Game Modes**:
  - Human vs AI: Challenge the computer at different difficulty levels
  - Human vs Human: Play against a friend on the same computer
  - AI vs AI: Watch two AI players compete against each other
  - Assisted Mode: Get strategic hints and move suggestions

- **Smart AI Opponent**:
  - Implements the minimax algorithm with alpha-beta pruning
  - Three difficulty levels (Easy, Medium, Hard)
  - Evaluates board positions based on strategic patterns

- **Polished UI**:
  - Animated piece dropping
  - Visual board with column numbers
  - Game status messages
  - Strategic hints in Assisted Mode

## Requirements

- Python 3.6 or higher
- Tkinter (included with standard Python installations)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/jaimansford/CONNECT-4-VS-AI.git
   ```

2. Navigate to the project directory:
   ```
   cd CONNECT-4-VS-AI
   ```

3. Run the game:
   ```
   python Connect4.py
   ```

## How to Play

1. Select your preferred game mode and difficulty level
2. Click on the column where you want to drop your piece
3. In Assisted Mode, the system will provide strategic hints
4. Connect four of your pieces horizontally, vertically, or diagonally to win

## Game Logic

The AI uses the minimax algorithm with alpha-beta pruning to determine the best move. The evaluation function considers:

- Center column control (pieces in the center have more connection opportunities)
- Horizontal, vertical, and diagonal piece patterns
- Blocking opponent's winning moves
- Creating winning opportunities
