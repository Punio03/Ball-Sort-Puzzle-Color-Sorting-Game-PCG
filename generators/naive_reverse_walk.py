import random

from game.logic import Logic, Flask
from generators.base_generator import BaseGenerator


class NaiveReverseWalkGenerator(BaseGenerator):
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

        step = 0
        cache = []
        while step < min_difficulty:
            while True:
                flask1 = random.choice(flasks)
                
                if not flask1.empty():
                    break
            
            while True:
                flask2 = random.choice(flasks)

                if not flask2.full() and flask1 is not flask2:
                    break
            
            color = flask1.remove()
            flask2.add(color)

            if (flask2.balls, flask1.balls) in cache:
                color = flask2.remove()
                flask1.add(color)
                continue
            
            cache.append((
                flask1.balls,
                flask2.balls
            ))

            step += 1

        return Logic(flasks)