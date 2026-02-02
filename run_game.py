import time
import random

import pygame

from agents.human_agent import HumanAgent
from agents.solver_agent import SolverAgent

from game.game_env import GameEnv
from generators.es_generator import EsGenerator
from generators.heuristic_reverse_walk_generator import HeuristicReverseWalkGenerator
from generators.naive_random_walk_generator import NaiveRandomWalkGenerator
from generators.map_elites_generator import MapElitesGenerator
from solvers.astar_solver import AStarSolver


def main():
    solver = AStarSolver()
    generator = HeuristicReverseWalkGenerator(solver, num_flasks=22, flask_size=4, num_colors=20)
    logic = generator.generate()
    # evo_generator = MapElitesGenerator(solver, num_flasks=22, num_colors=20)
    # logic = evo_generator.generate(size=4, min_difficulty=50)
    # logic = random.choice(logic)

    # agent = HumanAgent()
    agent = SolverAgent(solver, delay=1.0)

    env = GameEnv(render_mode=True)
    env.load_logic(logic)

    running = True

    while running:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        env.draw()

        if env.logic.is_game_over():
            time.sleep(2)
            running = False
            continue

        action = agent.get_action(env, events)
        if action is not None:
            env.step(action)

    env.close()


if __name__ == "__main__":
    main()
