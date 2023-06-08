import pygame
from random import randint
from pac_man.game import Wall, compose_context, draw_whole_screen


def main() -> None:
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

        old_player_topleft = context.player.rect.topleft

        if keys[pygame.K_w]:
            context.player.rect = context.player.rect.move(0, -1 * player_speed)
        if keys[pygame.K_s]:
            context.player.rect = context.player.rect.move(0, player_speed)
        if keys[pygame.K_a]:
            context.player.rect = context.player.rect.move(-1 * player_speed, 0)
        if keys[pygame.K_d]:
            context.player.rect = context.player.rect.move(player_speed, 0)

        if pygame.sprite.spritecollide(context.player, context.walls, dokill=False):
            context.player.rect.topleft = old_player_topleft

        if context.player.is_collided_with(context.chest):
            context.score += 1
            context.chest.rect.topleft = (
                randint(Wall.width, screen.get_width() - Wall.width * 2),
                randint(Wall.height, screen.get_height() - Wall.height * 2),
            )

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
