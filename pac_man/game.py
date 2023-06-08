import pygame
from pac_man.game_object import GameObject
from pac_man.text import Text
from dataclasses import dataclass


class Player(GameObject):
    sprite_filename = 'player'


class Wall(GameObject):
    sprite_filename = 'wall'


class Chest(GameObject):
    sprite_filename = 'chest'


@dataclass(kw_only=True)
class Context(GameObject):
    player: Player
    walls: pygame.sprite.Group
    score: int
    chest: Chest


def calculate_walls_coordinates(
        screen_width: int,
        screen_height: int,
        wall_block_width: int,
        wall_block_height: int) -> list[tuple[int, int]]:
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height - 2

    walls_coordinates = []
    for block_num in range(horizontal_wall_blocks_amount):
        walls_coordinates.extend([
            (wall_block_width * block_num, 0),
            (wall_block_width * block_num, screen_height - wall_block_height),
        ])

    for block_num in range(1, vertical_wall_blocks_amount + 1):
        walls_coordinates.extend([
            (0, wall_block_height * block_num),
            (screen_width - wall_block_width, wall_block_height * block_num),
        ])

    return walls_coordinates


def compose_context(screen: pygame.surface.Surface) -> Context:
    walls_coordinates = calculate_walls_coordinates(
        screen.get_width(),
        screen.get_height(),
        Wall.width,
        Wall.height
    )

    player = Player(screen.get_width() // 2, screen.get_height() // 2)
    walls = pygame.sprite.Group(*[Wall(x, y) for (x, y) in walls_coordinates])
    score = 0
    chest = Chest(100, 100)

    return Context(player=player, walls=walls, score=score, chest=chest)


def draw_whole_screen(screen: pygame.surface.Surface, context: Context) -> None:
    screen.fill('purple')
    getattr(context, 'player').draw(screen)
    getattr(context, 'walls').draw(screen)
    getattr(context, 'chest').draw(screen)
    Text(str(getattr(context, 'score')), (10, 10)).draw(screen)
