# AI Game Referee (Rock-Paper-Scissors-Plus)

A minimal AI-powered referee for a CLI-based Rock-Paper-Scissors-Plus game, built using Google's Generative AI SDK.

## Overview
The bot acts as a referee, managing a "Best of 3" game. It enforces rules, tracks state (scores, bomb usage), and limits the game duration.

## Rules
- **Moves**: Rock, Paper, Scissors, Bomb.
- **Bomb**: Beats everything, used 1x per game.
- **Failures**: Invalid input wastes a round.
- **Duration**: Max 3 rounds.

## Architecture

### 1. State Model (`game_state.py`)
- `GameState` class: Singleton-style state tracker.
- Persists: `round_count`, `scores`, `bomb_used`.

### 2. Game Logic / Tools (`game_logic.py`)
- `play_round(user_move)`: The primary tool exposed to the AI.
- Handles validation, bot move generation (RNG), rule enforcement, and state updates.
- Returns structured JSON-like dictionaries into the AI context.

### 3. Agent (`main.py`)
- Uses `gemini-2.5-flash` (or falls back to other available models).
- System Prompt: strict instruction to rely on `play_round` for all logic.
- Automatic Function Calling: The SDK handles the tool execution loop.

## Usage
1.  **Install dependencies**:
    ```bash
    pip install google-generativeai
    ```
2.  **Set API Key**:
    You can set the `GOOGLE_API_KEY` environment variable, or the script will prompt you for it.
    ```powershell
    $env:GOOGLE_API_KEY = "your_key_here"
    ```
3.  **Run**:
    ```bash
    python main.py
    ```

## Files
- `main.py`: Entry point.
- `game_logic.py`: Core game rules and tool definitions.
- `game_state.py`: Data class for managing game state.
