"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (35, 45, 35)
COLOR_PLAYER = (80, 180, 255)
COLOR_OBSTACLE = (220, 60, 60)
COLOR_TEXT = (255, 255, 255)
COLOR_BANNER = (255, 220, 80)


def draw_scene(surface, player, coins, obstacles=(), hide_player=False):
    surface.fill(COLOR_BG)
    for coin in coins:
        pygame.draw.circle(surface, coin.color, (int(coin.x), int(coin.y)), coin.radius)
    for obstacle in obstacles:
        pygame.draw.rect(surface, COLOR_OBSTACLE, obstacle.get_rect())
    if not hide_player:
        pygame.draw.rect(surface, COLOR_PLAYER, player.get_rect(), border_radius=4)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, COLOR_BANNER)
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_game_over(surface, font, title, score):
    """Dim the scene and show title, final score and restart hint."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    surface.blit(overlay, (0, 0))

    cx = surface.get_width() // 2
    cy = surface.get_height() // 2
    lines = [
        (title, COLOR_BANNER, -40),
        (f"Final score: {score}", COLOR_TEXT, 0),
        ("Press R to restart", COLOR_TEXT, 40),
    ]
    for text, color, offset in lines:
        surf = font.render(text, True, color)
        surface.blit(surf, surf.get_rect(center=(cx, cy + offset)))