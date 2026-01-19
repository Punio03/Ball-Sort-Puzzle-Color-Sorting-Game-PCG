from collections import deque
from typing import Tuple, List

from game.logic import Logic
from solvers.base_solver import BaseSolver


class BFSSolver(BaseSolver):
    @staticmethod
    def _get_canonical(board_data):
        return tuple(sorted([tuple(t) for t in board_data]))

    def solve(self, logic_start: Logic) -> Tuple[bool, List[Tuple[int, int]]]:
        initial_board = [list(f.balls) for f in logic_start.board]
        max_cap = logic_start.board[0].MAX_SIZE
        queue = deque([(initial_board, [])])
        visited = {self._get_canonical(initial_board)}
        nodes_checked = 0
        MAX_NODES = 100000

        while queue:
            current_board, path = queue.popleft()
            nodes_checked += 1

            if nodes_checked > MAX_NODES:
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
                                queue.append((new_board, path + [(i, j)]))

        return False, []
