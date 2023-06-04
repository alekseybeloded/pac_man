import pygame
from pac_man.game_object import GameObject
from pac_man.text import Text
from random import randint



class Player(GameObject):
    sprite_filename = 'player'

class Wall(GameObject):
    sprite_filename = 'wall'

class Chest(GameObject):
    sprite_filename = 'chest'


def calculate_walls_coordinates(screen_width, screen_height, wall_block_width, wall_block_height):
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

def compose_context(screen):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    
    return {
        'player': Player(screen.get_width() // 2, screen.get_height() // 2),
        'walls': pygame.sprite.Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        'score': 0,
        'chest': Chest(100, 100)
    }
    

    
def draw_whole_screen(screen, context):
    screen.fill("purple")
    context['player'].draw(screen)
    context['walls'].draw(screen)
    context['chest'].draw(screen)
    Text(str(context['score']), (10, 10)).draw(screen)



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    player_speed = 3

    context = compose_context(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        draw_whole_screen(screen, context)
        pygame.display.flip()

        keys = pygame.key.get_pressed()
      
        old_player_topleft = context['player'].rect.topleft
      
        if keys[pygame.K_w]:
            context['player'].rect = context['player'].rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context['player'].rect = context['player'].rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context['player'].rect = context['player'].rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context['player'].rect = context['player'].rect.move(player_speed, 0)

        if pygame.sprite.spritecollide(context['player'], context['walls'], dokill=False):
            context['player'].rect.topleft = old_player_topleft
        
        if context['player'].is_collided_with(context['chest']):
            context['score'] += 1
            context['chest'].rect.topleft = (
                randint(Wall.width, screen.get_width() - Wall.width * 2),
                randint(Wall.height, screen.get_height() - Wall.height * 2),
            )


        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == '__main__':
    main()