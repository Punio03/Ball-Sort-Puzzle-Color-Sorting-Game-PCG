import time

import pygame

from agents.human_agent import HumanAgent
from agents.solver_agent import SolverAgent
from game.game_env import GameEnv
from generators.random_generator import RandomGenerator
from solvers.astar_solver import AStarSolver
from solvers.bfs_solver import BFSSolver


def main():
    solver = AStarSolver()
    generator = RandomGenerator(solver, num_flasks=22, num_colors=20)
    logic = generator.generate(min_difficulty=15)

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
