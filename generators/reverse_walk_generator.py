import random

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class ReverseWalkGenerator(BaseGenerator):
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
        initial_state = candidate_logic.get_state_tuple()
        
        stack = [(0, initial_state)]
        visited = {initial_state}

        while stack:
            step, state = stack.pop()
            candidate_logic.from_state(state)

            if step >= min_difficulty:
                return candidate_logic
            
            moves = candidate_logic.get_possible_reverse_moves()
            random.shuffle(moves)

            for move in moves:
                candidate_logic.reverse_move(*move)
                new_state = candidate_logic.get_state_tuple()
                candidate_logic.undo()

                if new_state not in visited:
                    visited.add(new_state)
                    stack.append((step+1, new_state))

        return None
