from typing import Optional

class Flask:
    def __init__(self, max_size: int, balls: Optional[list[int]]=None) -> None:
        self.balls = balls if balls else []
        self.MAX_SIZE = max_size
        
    def remove(self) -> int:
        return self.balls.pop()

    def add(self, color) -> None:
        self.balls.append(color)

    def size(self) -> int:
        return len(self.balls)
    
    def empty(self) -> bool:
        return self.size() != 0
    
    def full(self) -> bool:
        return self.size() < self.MAX_SIZE

class Logic:
    def __init__(self, board: Optional[list[Flask]]=None) -> None:
        self.board = board if board else []
        self.history = []

    def move(self, from_id: int, to_id: int) -> bool:
        from_flask = self.board[from_id]
        to_flask = self.board[to_id]

        if not from_flask.empty() and not to_flask.full():
            self.history.append((from_id, to_id))
            color = from_flask.remove()
            to_flask.add(color)
            
            return True
        
        return False
    
    def undo(self) -> None:
        from_id, to_id = self.history.pop()
        self.move(to_id, from_id)
    
    def is_game_over(self) -> bool:
        for flask in self.board:
            if len(set(flask.balls)) != 1:
                return False
        
        return True
