"""
Coin: a static collectible circle. Drawn as a circle, hit-tested as a
bounding square around it. Each coin has a type (bronze, silver, gold)
that sets its value and color.
"""

import pygame

COIN_TYPES = {
    "bronze": {"value": 1, "color": (205, 127, 50)},
    "silver": {"value": 3, "color": (192, 192, 200)},
    "gold":   {"value": 5, "color": (255, 215, 0)},
}


class Coin:
    def __init__(self, x, y, coin_type="bronze", radius=12):
        if coin_type not in COIN_TYPES:
            raise ValueError(f"Unknown coin type: {coin_type}")
        self.x = x
        self.y = y
        self.radius = radius
        self.coin_type = coin_type
        self.value = COIN_TYPES[coin_type]["value"]
        self.color = COIN_TYPES[coin_type]["color"]

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )