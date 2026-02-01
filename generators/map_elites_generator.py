import random
import math
import copy
import numpy as np

from tqdm import tqdm

from game.logic import Logic, Flask
from generators.base_generator import EvolutionaryGenerator
from generators.naive_random_walk_generator import NaiveRandomWalkGenerator


class MapElitesGenerator(EvolutionaryGenerator):
    def fitness(self, chromosome):
        score = 0

        solvable, path = self.solver.solve(chromosome)

        if solvable:
            score += 100

        score += len(path) - self.min_difficulty

        return score

    def features(self, chromosome: Logic) -> tuple:
        total_entropy = 0
        num_homogeneous = 0
        empty_flasks = 0

        max_entropy = math.log2(self.num_colors)

        for flask in chromosome.board:
            if len(flask.balls) == 0:
                empty_flasks += 1
                continue

            counts = {}
            for ball in flask.balls:
                counts[ball] = counts.get(ball, 0) + 1

            if len(counts) == 1:
                num_homogeneous += 1

            flask_size = len(flask.balls)
            entropy = 0
            for count in counts.values():
                p = count / flask_size
                if p > 0:
                    entropy -= p * math.log2(p)

            total_entropy += entropy / max_entropy

        total_flasks = len(chromosome.board)

        avg_entropy = total_entropy / total_flasks
        homogeneity_ratio = num_homogeneous / total_flasks

        entropy_bin = min(9, int(avg_entropy * 10))
        homogeneity_bin = min(9, int(homogeneity_ratio * 10))

        return (entropy_bin, homogeneity_bin)

    def place(self, map_elites: dict, chromosome: Logic) -> None:
        score = self.fitness(chromosome)

        hashable_key = self.features(chromosome)

        elite = map_elites.get(hashable_key)

        if elite is None or self.fitness(elite) < score:
            map_elites[hashable_key] = chromosome

    def update(self, map_elites: dict, mut_rate: float, batch_size: int):
        for _ in range(batch_size):
            population: list[Logic] = list(map_elites.values())

            chromosome = random.choice(population)

            if random.random() < mut_rate:
                chromosome = Logic.mutate(chromosome)
                self.place(map_elites, chromosome)

        population = list(map_elites.values())
        return population

    def generate(self, min_difficulty: int, **kwargs) -> Logic:
        map_elites = {}

        self.min_difficulty = min_difficulty

        epochs = kwargs.get("epochs", 1000)
        mut_rate = kwargs.get("mut_rate", 0.01)
        batch_size = kwargs.get("batch_size", 100)

        generator = NaiveRandomWalkGenerator(
            self.solver, self.num_flasks, self.num_colors
        )
        population = [generator.generate(self.flask_size, 5) for _ in range(batch_size)]

        for chromosome in population:
            self.place(map_elites, chromosome)

        with open("save.csv", "w") as f:
            f.write("epoch;avg;max;min;size\n")
            for epoch in tqdm(range(epochs)):
                population = self.update(map_elites, mut_rate, batch_size)
                avg = np.average([self.fitness(x) for x in population])
                maxi = np.max([self.fitness(x) for x in population])
                mini = np.min([self.fitness(x) for x in population])
                size = len(population)
                f.write(f"{epoch};{avg};{maxi};{mini};{size}\n")

        best_map = None
        best_score = 0
        
        with open('map_es_flasks3.txt', 'w') as f:
            for chromosome in population:
                for flask in chromosome.board:
                    f.write(f"{flask.balls} ")
                f.write("\n")
                score = self.fitness(chromosome)

                if score > best_score:
                    best_map = chromosome

        return [best_map]
