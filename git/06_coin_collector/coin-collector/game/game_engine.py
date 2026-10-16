"""
GameEngine: owns the player, coins, obstacles, lives and the round timer.

- Coins: bronze 1, silver 3, gold 5; removed once collected.
- Obstacles bounce around; a hit costs a life, then ~1s of invincibility.
- Round lasts 30 seconds. It ends on time-up or 0 lives, shows the final
  score, and pressing R restarts with score, lives and timer reset.
"""

import math
import random
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
NUM_OBSTACLES = 3
STARTING_LIVES = 3
INVINCIBILITY_MS = 1000
ROUND_MS = 30_000
OBSTACLE_SPEED = 2.5
OBSTACLE_MIN_DIST_FROM_PLAYER = 120

COIN_TYPE_NAMES = ["bronze", "silver", "gold"]
COIN_TYPE_WEIGHTS = [60, 30, 10]


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round: score, lives, timer, coins, obstacles."""
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.obstacles = [self._random_obstacle() for _ in range(NUM_OBSTACLES)]
        self.score = 0
        self.lives = STARTING_LIVES
        self.invincible_until = 0
        self.game_over = False
        self.end_reason = ""
        self.round_start = pygame.time.get_ticks()
        self.time_left_ms = ROUND_MS

    def _random_coin(self):
        x = random.randint(30, WIDTH - 30)
        y = random.randint(30, HEIGHT - 30)
        coin_type = random.choices(COIN_TYPE_NAMES, weights=COIN_TYPE_WEIGHTS)[0]
        return Coin(x=x, y=y, coin_type=coin_type)

    def _random_obstacle(self):
        size = 30
        half = size / 2
        # Spawn fully inside the play area and away from the player
        while True:
            x = random.randint(int(half), int(WIDTH - half))
            y = random.randint(int(half), int(HEIGHT - half))
            if math.hypot(x - self.player.x, y - self.player.y) >= OBSTACLE_MIN_DIST_FROM_PLAYER:
                break
        angle = random.uniform(0, 2 * math.pi)
        vx = OBSTACLE_SPEED * math.cos(angle)
        vy = OBSTACLE_SPEED * math.sin(angle)
        return Obstacle(x, y, vx, vy, size)

    def is_invincible(self):
        return pygame.time.get_ticks() < self.invincible_until

    def _end_round(self, reason):
        self.game_over = True
        self.end_reason = reason

    def handle_input(self, keys_pressed):
        if self.game_over:
            if keys_pressed[pygame.K_r]:
                self.reset()
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        if self.game_over:
            return

        # Timer
        elapsed = pygame.time.get_ticks() - self.round_start
        self.time_left_ms = max(0, ROUND_MS - elapsed)

        # Coins
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
        self.coins = [c for c in self.coins if c not in collected]

        # Obstacles
        for obstacle in self.obstacles:
            obstacle.update(WIDTH, HEIGHT)

        if not self.is_invincible():
            player_rect = self.player.get_rect()
            if any(player_rect.colliderect(o.get_rect()) for o in self.obstacles):
                self.lives -= 1  # one life per hit, even if several overlap
                self.invincible_until = pygame.time.get_ticks() + INVINCIBILITY_MS
                if self.lives <= 0:
                    self.lives = 0
                    self._end_round("GAME OVER")
                    return

        if self.time_left_ms <= 0:
            self._end_round("TIME'S UP")

    def draw(self, surface, font):
        from game import renderer
        # Blink the player while invincible
        blink_off = (not self.game_over and self.is_invincible()
                     and (pygame.time.get_ticks() // 100) % 2 == 0)
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles, hide_player=blink_off)

        seconds = math.ceil(self.time_left_ms / 1000)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Time: {seconds}", (WIDTH // 2 - 40, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (WIDTH - 110, 10))

        if self.game_over:
            renderer.draw_game_over(surface, font, self.end_reason, self.score)