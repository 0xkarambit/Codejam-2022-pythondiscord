import pygame
from constants import TILE_H, TILE_W


class Breakable_tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.type = "breakable_tile"
        self.image = surf
        self.image = pygame.transform.scale(self.image, (TILE_W, TILE_H))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.group = group

    def update(self, events, player):
        if self.rect.colliderect(player.rect):
            self.group.remove(self)  # deletes the tile !!!
        self.vertical_movement_collision(
            player
        )  # tiles dont break when u stand on them

    def render(self, surface, camera, player):
        pos = pygame.Vector2(self.rect.x, self.rect.y)
        rel_pos = camera.get_relative_coors(pos)
        rel_rect = self.image.get_rect(topleft=rel_pos)
        surface.blit(self.image, rel_rect)

    # Override for making the cell disappear
    def horizontal_movement_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.group.remove(self)  # deletes the tile !!!
            # if player.direction.x < 0:
            #     player.rect.left = self.rect.right

            # elif player.direction.x > 0:
            #     player.rect.right = self.rect.left

    def vertical_movement_collision(self, player):
        if self.rect.colliderect(player.rect):
            if player.direction.y > 0:
                # player.rect.bottom = self.rect.top
                # player.direction.y = 0
                player.jump_limit = 0
                player.in_air_after_jump = False
                player.spritesheet.unlock_animation()

            self.group.remove(self)  # deletes the tile !!!

            # player.rect.top = self.rect.bottom
            # player.direction.y = 0
