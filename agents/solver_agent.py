import time
from typing import List, Any, Optional, Tuple

from agents.base_agent import BaseAgent
from solvers.base_solver import BaseSolver


class SolverAgent(BaseAgent):
    def __init__(self, solver: BaseSolver, delay: float = 0.5):
        self.solver = solver
        self.moves_queue = []
        self.delay = delay
        self.last_move_time = 0

    def get_action(self, env, events: List[Any]) -> Optional[Tuple[int, int]]:
        if not self.moves_queue:
            solved, path = self.solver.solve(env.logic)
            if solved:
                self.moves_queue = path
            else:
                return None

        current_time = time.time()
        if current_time - self.last_move_time > self.delay:
            if self.moves_queue:
                self.last_move_time = current_time
                action = self.moves_queue.pop(0)
                return action

        return None
