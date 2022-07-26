import pygame


class Other_Player:
    def __init__(self, x, y, w, h, color: pygame.Color, health):
        self.health = health
        # self.name = "Player 1"
        # self.sprites =

        self.color = color

        self.rect = pygame.Rect(x, y, w, h)

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)

    # will have to interact with the tiles_array and other physical entities like traps for collision detection
    def update(self, events):
        pass
