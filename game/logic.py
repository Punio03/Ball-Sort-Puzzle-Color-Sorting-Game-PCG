from typing import Optional


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
        return Flask(self.MAX_SIZE, self.balls)


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
