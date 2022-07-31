import pygame
from constants import TILE_H, TILE_W


class Spike(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.type = "spike"
        self.image = surf
        self.image = pygame.transform.scale(self.image, (TILE_W, TILE_H))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.group = group

    def update(self, events, player):
        if self.rect.colliderect(player.rect):
            player.death()

    def render(self, surface, camera, player):
        pos = pygame.Vector2(self.rect.x, self.rect.y)
        rel_pos = camera.get_relative_coors(pos)
        rel_rect = self.image.get_rect(topleft=rel_pos)
        surface.blit(self.image, rel_rect)
