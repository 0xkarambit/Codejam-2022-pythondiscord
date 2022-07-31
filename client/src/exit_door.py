import pygame


class Exit_door(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.type = "exit_door"
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.group = group

    def update(self, events, player):
        if self.rect.colliderect(player.rect):
            player.has_won = True

    def render(self, surface, camera, player):
        pos = pygame.Vector2(self.rect.x, self.rect.y)
        rel_pos = camera.get_relative_coors(pos)
        rel_rect = self.image.get_rect(topleft=rel_pos)
        surface.blit(self.image, rel_rect)
