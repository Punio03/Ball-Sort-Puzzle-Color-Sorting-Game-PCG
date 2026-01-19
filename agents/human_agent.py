from typing import List, Any, Optional, Tuple

import pygame

from agents.base_agent import BaseAgent


class HumanAgent(BaseAgent):
    def get_action(self, env, events: List[Any]) -> Optional[Tuple[int, int]]:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_idx = env.get_flask_at_pos(mx, my)

                if clicked_idx is not None:
                    if env.selected_flask is None:
                        if not env.logic.board[clicked_idx].empty():
                            env.selected_flask = clicked_idx
                    else:
                        src = env.selected_flask
                        dst = clicked_idx

                        env.selected_flask = None

                        if src != dst:
                            return src, dst

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    env.logic.undo()
                    env.selected_flask = None
                if event.key == pygame.K_r:
                    while env.logic.history:
                        env.logic.undo()
                    env.selected_flask = None
        return None
