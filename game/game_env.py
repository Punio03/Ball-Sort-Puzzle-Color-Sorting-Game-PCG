from typing import Optional, Tuple

import pygame

from game.logic import Logic
from game.settings import *


class GameEnv:
    def __init__(self, render_mode=True):
        self.logic: Optional[Logic] = None
        self.render_mode = render_mode
        self.selected_flask = None

        if self.render_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Ball Sort Puzzle Color Sorting Game")
            self.clock = pygame.time.Clock()

    def load_logic(self, logic_instance: Logic):
        self.logic = logic_instance
        self.selected_flask = None

    def step(self, action: Tuple[int, int]):
        if not self.logic:
            return None, 0, False
        src, dst = action
        moved = self.logic.move(src, dst)
        reward = 1 if moved else -1
        done = self.logic.is_game_over()
        if done:
            reward = 100
        obs = [list(f.balls) for f in self.logic.board]
        return obs, reward, done

    def draw(self):
        if not self.render_mode or not self.logic:
            return
        self.screen.fill(COLORS_MAP["BG"])

        cols = 11
        for i, flask in enumerate(self.logic.board):
            r, c = divmod(i, cols)
            x = 50 + c * (TUBE_WIDTH + 20)
            y = 100 + r * (TUBE_HEIGHT + 30)

            color = COLORS_MAP["HL"] if i == self.selected_flask else COLORS_MAP["TUBE"]
            pygame.draw.rect(self.screen, color, (x, y, TUBE_WIDTH, TUBE_HEIGHT), 3)

            for b_idx, color_id in enumerate(flask.balls):
                cx = x + TUBE_WIDTH // 2
                cy = y + TUBE_HEIGHT - 25 - (b_idx * 45)
                if i == self.selected_flask and b_idx == len(flask.balls) - 1:
                    cy -= 25

                rgb = COLORS_MAP.get(color_id, (100, 100, 100))
                pygame.draw.circle(self.screen, rgb, (cx, cy), BALL_RADIUS)

        pygame.display.flip()
        self.clock.tick(60)

    def get_flask_at_pos(self, mx, my) -> Optional[int]:
        if not self.logic:
            return None
        cols = 11
        for i in range(len(self.logic.board)):
            r, c = divmod(i, cols)
            x = 50 + c * (TUBE_WIDTH + 20)
            y = 100 + r * (TUBE_HEIGHT + 30)
            rect = pygame.Rect(x, y, TUBE_WIDTH, TUBE_HEIGHT)
            if rect.collidepoint(mx, my):
                return i
        return None

    def close(self):
        if self.render_mode:
            pygame.quit()
