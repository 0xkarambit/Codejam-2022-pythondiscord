import pygame
from ..constants import TILE_H, TILE_W


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

    def render(self, surface, camera, player):
        pos = pygame.Vector2(self.rect.x, self.rect.y)
        rel_pos = camera.get_relative_coors(pos)
        rel_rect = self.image.get_rect(topleft=rel_pos)
        surface.blit(self.image, rel_rect)

    # Override for making the cell disappear
    def horizontal_movement_collision(self, player):
        if self.rect.colliderect(player.rect):
            self.group.remove(self)  # deletes the tile !!!
