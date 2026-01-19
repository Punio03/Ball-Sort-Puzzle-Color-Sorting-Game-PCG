import heapq
from typing import Tuple, List

from game.logic import Logic
from solvers.base_solver import BaseSolver


class AStarSolver(BaseSolver):
    def __init__(self, max_steps=10000):
        self.max_steps = max_steps

    @staticmethod
    def _calculate_heuristic(state_matrix, max_capacity):
        penalty = 0
        for tube in state_matrix:
            if not tube:
                continue

            prev_color = tube[0]
            changes = 0
            for color in tube[1:]:
                if color != prev_color:
                    changes += 1
                prev_color = color

            penalty += changes * 10

            if len(set(tube)) == 1 and len(tube) < max_capacity:
                penalty += max_capacity - len(tube)
        return penalty

    def solve(self, logic_start: Logic) -> Tuple[bool, List[Tuple[int, int]]]:
        initial_board = [list(f.balls) for f in logic_start.board]
        max_cap = logic_start.board[0].MAX_SIZE

        start_h = self._calculate_heuristic(initial_board, max_cap)
        queue = []
        heapq.heappush(queue, (start_h, 0, initial_board, []))

        visited = {self._get_canonical(initial_board)}
        nodes_explored = 0

        while queue:
            est_cost, moves_count, current_board, path = heapq.heappop(queue)
            nodes_explored += 1

            if nodes_explored > self.max_steps:
                return False, []

            is_win = True
            for tube in current_board:
                if not tube:
                    continue
                if len(tube) != max_cap or len(set(tube)) != 1:
                    is_win = False
                    break

            if is_win:
                return True, path

            for i in range(len(current_board)):
                src = current_board[i]
                if not src:
                    continue
                ball = src[-1]

                for j in range(len(current_board)):
                    if i == j:
                        continue
                    dst = current_board[j]

                    if len(dst) < max_cap:
                        if not dst or dst[-1] == ball:
                            if len(src) > 1 and src[-2] == ball and not dst:
                                continue

                            new_board = [list(t) for t in current_board]
                            new_board[i].pop()
                            new_board[j].append(ball)

                            canonical = self._get_canonical(new_board)

                            if canonical not in visited:
                                visited.add(canonical)
                                h = self._calculate_heuristic(new_board, max_cap)
                                g = moves_count + 1
                                heapq.heappush(
                                    queue, (g + h, g, new_board, path + [(i, j)])
                                )

        return False, []
