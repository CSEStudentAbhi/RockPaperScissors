import random
from game_state import GameState

_GAME_STATE = GameState()

def reset_game():
    global _GAME_STATE
    _GAME_STATE = GameState()
    return "Game Reset."

def validate_move(move: str, player: str = 'user') -> bool:
    valid_moves = ['rock', 'paper', 'scissors', 'bomb']
    if move not in valid_moves:
        return False
    if move == 'bomb' and not _GAME_STATE.can_use_bomb(player):
        return False
    return True

def get_bot_move() -> str:
    moves = ['rock', 'paper', 'scissors']
    if _GAME_STATE.can_use_bomb('bot'):
        if random.random() < 0.2: 
            return 'bomb'
    return random.choice(moves)

def determine_winner(user_move: str, bot_move: str) -> tuple[str, str]:
    if user_move == bot_move:
        return 'draw', f"Both chose {user_move}"
    
    if user_move == 'bomb':
        return 'user', "Bomb beats everything!"
    if bot_move == 'bomb':
        return 'bot', "Bomb beats everything!"
        
    wins = {
        'rock': 'scissors',
        'paper': 'rock',
        'scissors': 'paper'
    }
    
    if wins[user_move] == bot_move:
        return 'user', f"{user_move} beats {bot_move}"
    
    return 'bot', f"{bot_move} beats {user_move}"

def play_round(user_move: str):
    global _GAME_STATE
    
    if _GAME_STATE.game_over:
        return {"error": "Game is already over. Please reset to play again.", "game_over": True}

    user_move = user_move.lower().strip()
    
    valid_basic = user_move in ['rock', 'paper', 'scissors', 'bomb']
    
    if not valid_basic:
        _GAME_STATE.record_round(user_move, "N/A", "none", "Invalid input")
        return {
            "round": _GAME_STATE.current_round,
            "status": "Invalid Move",
            "message": f"'{user_move}' is not a valid move. Round wasted.",
            "scores": _GAME_STATE.scores,
            "game_over": _GAME_STATE.game_over
        }

    if user_move == 'bomb':
        if not _GAME_STATE.use_bomb('user'):
             _GAME_STATE.record_round(user_move, "N/A", "none", "Bomb already used")
             return {
                "round": _GAME_STATE.current_round,
                "status": "Invalid Move",
                "message": "You have already used your Bomb! Round wasted.",
                "scores": _GAME_STATE.scores,
                "game_over": _GAME_STATE.game_over
            }

    bot_move = get_bot_move()
    if bot_move == 'bomb':
        _GAME_STATE.use_bomb('bot')

    winner, reason = determine_winner(user_move, bot_move)
    _GAME_STATE.record_round(user_move, bot_move, winner, reason)
    
    result = {
        "round": _GAME_STATE.current_round,
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner,
        "reason": reason,
        "scores": _GAME_STATE.scores,
        "game_over": _GAME_STATE.game_over
    }

    if _GAME_STATE.game_over:
        result["final_result"] = _GAME_STATE.get_summary()

    return result

tools_list = [play_round]
