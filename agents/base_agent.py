from abc import ABC, abstractmethod
from typing import List, Any, Tuple, Optional


class BaseAgent(ABC):
    @abstractmethod
    def get_action(self, env, events: List[Any]) -> Optional[Tuple[int, int]]:
        pass
