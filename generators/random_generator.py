import random

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class RandomGenerator(BaseGenerator):
    def generate(self, size: int, min_difficulty: int) -> Logic:
        while True:
            balls = []
            for c in range(self.num_colors):
                balls.extend([c] * size)
            random.shuffle(balls)

            flasks = []
            idx = 0

            for _ in range(self.num_colors):
                flasks.append(Flask(size, balls[idx : idx + 4]))
                idx += size

            for _ in range(self.num_flasks - self.num_colors):
                flasks.append(Flask(size, []))

            candidate_logic = Logic(flasks)

            solved, path = self.solver.solve(candidate_logic)

            if solved and len(path) >= min_difficulty:
                return candidate_logic
