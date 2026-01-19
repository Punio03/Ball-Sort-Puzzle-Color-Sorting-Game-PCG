import random

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class RandomGenerator(BaseGenerator):
    def generate(self, min_difficulty: int) -> Logic:
        while True:
            balls = []
            for c in range(self.num_colors):
                balls.extend([c] * 4)
            random.shuffle(balls)

            flasks = []
            idx = 0

            for _ in range(self.num_colors):
                flasks.append(Flask(4, balls[idx : idx + 4]))
                idx += 4

            for _ in range(self.num_flasks - self.num_colors):
                flasks.append(Flask(4, []))

            candidate_logic = Logic(flasks)

            solved, path = self.solver.solve(candidate_logic)

            if solved and len(path) >= min_difficulty:
                return candidate_logic
