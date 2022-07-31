from abc import ABC, abstractmethod

import pygame
from .constants import TILE_COUNT_X, TILE_COUNT_Y, TILE_H, TILE_W

MAP_W = TILE_COUNT_X * TILE_W
MAP_H = TILE_COUNT_Y * TILE_H

# todo add a zoom feature


class Camera:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        draw_dist_x = 48  # need a +18 = 40 draw_dist
        draw_dist_y = 22  # todo change this it looks awesome !
        # the amount of pixels the camera draws
        self.draw_distance = pygame.Vector2(draw_dist_x * TILE_W, draw_dist_y * TILE_H)
        # when the player is this much distance away from the camera borders the camera will move
        self.MOVE_MARGIN = pygame.Vector2(13 * TILE_W, 4 * TILE_H)
        # for moving towards the left and the top
        self.MOVE_MARGIN_INVERTED = pygame.Vector2(10 * TILE_W, 4 * TILE_H)
        # the camera is not to move after this point is reached
        self.Y_LIMIT = MAP_H - self.draw_distance.y
        self.X_LIMIT = MAP_W - self.draw_distance.x
        # to avoid the black glitchy effect on the left side
        self.offset = 2 * TILE_W

    def follow_player(self, player):
        """Updates camera position in the required direction

        checks if the camera is colliding with the borders and then
        checking if it needs to be moved in the specific directions

        Args:
            player (pygame.Rect): the player Rect which is to be followed
        """
        while self.pos.y < self.Y_LIMIT and player.rect.y > (
            self.pos.y + self.draw_distance.y - 1 - self.MOVE_MARGIN.y
        ):
            # DOWN -> y++;
            self.pos.y += 0 if (self.pos.y >= MAP_H) else 1

        while self.pos.x < self.X_LIMIT and player.rect.x > (
            self.pos.x + self.draw_distance.x - 1 - self.MOVE_MARGIN.x
        ):
            # RIGHT -> x++;
            self.pos.x += 0 if (self.pos.x >= MAP_W) else 1

        while self.pos.y > 0 and player.rect.y < (
            self.pos.y + self.MOVE_MARGIN_INVERTED.y
        ):
            # TOP -> y--;
            self.pos.y -= 0 if (self.pos.y <= 0) else 1

        while self.pos.x > 0 and player.rect.x < (
            self.pos.x + self.MOVE_MARGIN_INVERTED.x
        ):
            # LEFT -> x--;
            self.pos.x -= 0 if (self.pos.x <= 0) else 1

    def get_relative_coors(self, coors):
        # adjusting the coordinates to render relative to the self postion
        x = coors.x - self.pos.x
        y = coors.y - self.pos.y
        return pygame.Vector2(x, y)
