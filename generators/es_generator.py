import random
from typing import Optional, Tuple, List

from game.logic import Logic
from generators.base_generator import BaseGenerator


class EsGenerator(BaseGenerator):
    def generate(
        self, difficulty_steps: int = 250, generations: Optional[int] = 100
    ) -> Logic:
        parent_path = self._heuristic_walk(difficulty_steps)
        parent_fitness = self._calculate_fitness(parent_path)

        for gen in range(generations):
            child_path = self._mutate(parent_path)
            child_fitness = self._calculate_fitness(child_path)

            if child_fitness >= parent_fitness:
                parent_path = child_path
                parent_fitness = child_fitness

        return self._simulate_path(parent_path)

    def _simulate_path(self, path) -> Logic:
        flasks = self._create_solved_board()
        for move in path:
            self._apply_move(flasks, move)
        return Logic(flasks)

    def _heuristic_walk(self, steps: int) -> List[Tuple[int, int]]:
        flasks = self._create_solved_board()
        path = []
        last_move = None

        for _ in range(steps):
            moves = self._get_possible_moves(flasks)

            valid_moves = [
                m
                for m in moves
                if not (last_move and m[0] == last_move[1] and m[1] == last_move[0])
            ]

            if not valid_moves:
                valid_moves = moves
                if not valid_moves:
                    break

            chosen_move = self._smart_choice(flasks, valid_moves)

            self._apply_move(flasks, chosen_move)
            path.append(chosen_move)
            last_move = chosen_move

        return path

    def _calculate_fitness(self, path: List[Tuple[int, int]]) -> int:
        candidate_logic = self._simulate_path(path)
        solved, _, solution_path = self.solver.solve(candidate_logic)

        if not solved:
            return 0
        return len(solution_path)

    def _mutate(self, parent_path: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        cut_point = int(len(parent_path) * random.uniform(0.6, 0.9))
        child_path = parent_path[:cut_point]

        flasks = self._create_solved_board()
        last_move = None
        for move in child_path:
            self._apply_move(flasks, move)
            last_move = move

        missing_steps = len(parent_path) - len(child_path)

        for _ in range(missing_steps):
            moves = self._get_possible_moves(flasks)
            valid_moves = [
                m
                for m in moves
                if not (last_move and m[0] == last_move[1] and m[1] == last_move[0])
            ]

            if not valid_moves:
                valid_moves = moves
                if not valid_moves:
                    break

            chosen_move = self._smart_choice(flasks, valid_moves)

            self._apply_move(flasks, chosen_move)
            child_path.append(chosen_move)
            last_move = chosen_move

        return child_path
