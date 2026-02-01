from typing import Optional
import random
import numpy as np
import copy


class Flask:
    def __init__(self, max_size: int, balls: Optional[list[int]] = None) -> None:
        self.balls = balls if balls else []
        self.MAX_SIZE = max_size

    def remove(self) -> int:
        return self.balls.pop()

    def add(self, color: int) -> None:
        self.balls.append(color)

    def size(self) -> int:
        return len(self.balls)

    def empty(self) -> bool:
        return self.size() == 0

    def full(self) -> bool:
        return self.size() == self.MAX_SIZE

    def top(self) -> Optional[int]:
        if self.empty():
            return None
        return self.balls[-1]

    def clone(self):
        return Flask(self.MAX_SIZE, copy(self.balls))


class Logic:
    def __init__(self, board: Optional[list[Flask]] = None) -> None:
        self.board = board if board else []
        self.history: list[tuple[int, int]] = []

    def can_move(self, from_id: int, to_id: int) -> bool:
        if from_id == to_id:
            return False

        if (
            from_id < 0
            or from_id >= len(self.board)
            or to_id < 0
            or to_id >= len(self.board)
        ):
            return False

        src = self.board[from_id]
        dst = self.board[to_id]

        if src.empty() or dst.full():
            return False

        if dst.empty():
            return True

        return src.top() == dst.top()

    def move(self, from_id: int, to_id: int) -> bool:
        if not self.can_move(from_id, to_id):
            return False

        color = self.board[from_id].remove()
        self.board[to_id].add(color)
        self.history.append((from_id, to_id))
        return True
    
    def reverse_move(self, from_id: int, to_id: int) -> bool:
        if from_id == to_id:
            return False

        if (
            from_id < 0 or
            from_id >= len(self.board) or
            to_id < 0 or
            to_id >= len(self.board)
        ):
            return False

        src = self.board[from_id]
        dst = self.board[to_id]

        if src.empty() or dst.full():
            return False

        color = src.remove()
        dst.add(color)
        self.history.append((from_id, to_id))
        return True

    def undo(self) -> None:
        if not self.history:
            return
        from_id, to_id = self.history.pop()
        color = self.board[to_id].remove()
        self.board[from_id].add(color)

    def is_game_over(self) -> bool:
        for flask in self.board:
            if flask.empty():
                continue
            if len(set(flask.balls)) != 1 or not flask.full():
                return False
        return True

    def get_state_tuple(self):
        state = []
        for f in self.board:
            state.append(tuple(f.balls))
        return tuple(sorted(state))
    
    def get_possible_moves(self):
        moves = []

        for to_id in range(len(self.board)):
            for from_id in range(len(self.board)):
                if self.can_move(from_id, to_id):
                    moves.append((from_id, to_id))

        return moves
    
    def get_possible_reverse_moves(self):
        reverse_moves = []

        for to_id in range(len(self.board)):
            if self.board[to_id].empty():
                continue

            for from_id in range(len(self.board)):
                if from_id == to_id:
                    continue

                if self.board[from_id].full():
                    continue

                color = self.board[to_id].remove()

                legal = (
                    self.board[to_id].empty() or
                    self.board[to_id].top() == color
                )

                self.board[to_id].add(color)

                if legal:
                    reverse_moves.append((to_id, from_id))

        return reverse_moves
    
    def from_state(self, state: tuple) -> None:
        board = []
        self.history.clear()

        for balls in state:
            board.append(
                Flask(self.board[0].MAX_SIZE, list(balls))
            )
        
        self.board = board

    
    @staticmethod
    def mutate(logic: "Logic") -> "Logic":
        new_logic = copy.deepcopy(logic)
        
        non_empty = [i for i, f in enumerate(new_logic.board) if not f.empty()]
        non_full = [i for i, f in enumerate(new_logic.board) if not f.full()]
        
        if not non_empty or not non_full:
            return new_logic
        
        mutation_type = random.random()
        
        if mutation_type < 0.4:
            for _ in range(100):
                from_id = random.choice(non_empty)
                to_id = random.choice(non_full)
                
                if from_id != to_id:
                    color = new_logic.board[from_id].remove()
                    new_logic.board[to_id].add(color)
                    break
        
        elif mutation_type < 0.7:
            if len(non_empty) >= 2:
                f1, f2 = random.sample(non_empty, 2)
                pos1 = random.randint(0, len(new_logic.board[f1].balls) - 1)
                pos2 = random.randint(0, len(new_logic.board[f2].balls) - 1)
                
                new_logic.board[f1].balls[pos1], new_logic.board[f2].balls[pos2] = \
                    new_logic.board[f2].balls[pos2], new_logic.board[f1].balls[pos1]
        
        else:
            shuffleable = [i for i, f in enumerate(new_logic.board) if len(f.balls) > 1]
            if shuffleable:
                flask_idx = random.choice(shuffleable)
                random.shuffle(new_logic.board[flask_idx].balls)
        
        return new_logic