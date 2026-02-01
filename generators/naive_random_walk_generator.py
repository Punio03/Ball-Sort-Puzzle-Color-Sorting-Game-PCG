import random

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class NaiveRandomWalkGenerator(BaseGenerator):
    def generate(self, size: int, min_difficulty: int) -> Logic:
        balls = []
        for c in range(self.num_colors):
            balls.extend([c] * size)
        
        flasks = []
        idx = 0
        for _ in range(self.num_colors):
            flasks.append(Flask(size, balls[idx : idx + 4]))
            idx += size

        for _ in range(self.num_flasks - self.num_colors):
            flasks.append(Flask(size, []))

        candidate_logic = Logic(flasks)
    
        for _ in range(min_difficulty):
            moves = candidate_logic.get_possible_moves()
            move = random.choice(moves)

            candidate_logic.move(*move)

        return candidate_logic
