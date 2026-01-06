from dataclasses import dataclass
from typing import List

@dataclass
class RoundResult:
    round_num: int
    user_move: str
    bot_move: str
    winner: str
    reason: str

class GameState:
    def __init__(self):
        self.max_rounds = 3
        self.current_round = 0
        self.scores = {'user': 0, 'bot': 0}
        self.bomb_used = {'user': False, 'bot': False}
        self.history: List[RoundResult] = []
        self.game_over = False

    def is_game_over(self) -> bool:
        return self.current_round >= self.max_rounds

    def use_bomb(self, player: str) -> bool:
        if self.bomb_used.get(player, False):
            return False
        self.bomb_used[player] = True
        return True
    
    def can_use_bomb(self, player: str) -> bool:
        return not self.bomb_used.get(player, False)

    def record_round(self, user_move: str, bot_move: str, winner: str, reason: str):
        self.current_round += 1
        result = RoundResult(
            round_num=self.current_round,
            user_move=user_move,
            bot_move=bot_move,
            winner=winner,
            reason=reason
        )
        self.history.append(result)
        
        if winner in self.scores:
            self.scores[winner] += 1
            
        if self.current_round >= self.max_rounds:
            self.game_over = True
            
    def get_summary(self) -> str:
        if self.scores['user'] > self.scores['bot']:
            final = "User Wins!"
        elif self.scores['bot'] > self.scores['user']:
            final = "Bot Wins!"
        else:
            final = "It's a Draw!"
            
        return (f"Game Over. Final Score - User: {self.scores['user']}, Bot: {self.scores['bot']}. "
                f"{final}")
