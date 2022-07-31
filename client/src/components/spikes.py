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
        """
        offset_x, offset_y = (self.rect.x - player.rect.x), (
            self.rect.y - player.rect.y
        )
        if self.mask.overlap(player.mask, (offset_x, offset_y)):
            print("\x1b[91m")
            print(f"THE PLAYER HAS DIED")
            print("\x1b[0m")
            player.death()
        """
        # DIDTN WORK
        # if pygame.sprite.collide_mask(self, player) == None:
        #     return
        # else:
        #     player.death()

    def render(self, surface, camera, player):
        pos = pygame.Vector2(self.rect.x, self.rect.y)
        rel_pos = camera.get_relative_coors(pos)
        rel_rect = self.image.get_rect(topleft=rel_pos)
        surface.blit(self.image, rel_rect)
