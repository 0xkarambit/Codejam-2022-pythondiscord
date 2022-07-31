import pygame
from constants import TILE_H, TILE_W


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.image = pygame.transform.scale(self.image, (TILE_W, TILE_H))
        self.rect = self.image.get_rect(topleft=pos)
        # print(pos)
        self.mask = pygame.mask.from_surface(self.image)
