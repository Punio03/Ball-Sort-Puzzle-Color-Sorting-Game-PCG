from typing import Optional, Tuple

from game.logic import Logic
from generators.base_generator import BaseGenerator


class HeuristicReverseWalkGenerator(BaseGenerator):
    def generate(
        self, difficulty_steps: int = 250, generations: Optional[int] = None
    ) -> Logic:
        while True:
            flasks = self._create_solved_board()
            last_move: Optional[Tuple[int, int]] = None

            for _ in range(difficulty_steps):
                moves = self._get_possible_moves(flasks)

                if not moves:
                    break

                valid_moves = []
                for m in moves:
                    if last_move and m[0] == last_move[1] and m[1] == last_move[0]:
                        continue
                    valid_moves.append(m)

                if not valid_moves:
                    valid_moves = moves

                chosen_move = self._smart_choice(flasks, valid_moves)
                self._apply_move(flasks, chosen_move)
                last_move = chosen_move

            candidate_logic = Logic(flasks)
            is_win, _, _ = self.solver.solve(candidate_logic)
            if is_win:
                return candidate_logic
