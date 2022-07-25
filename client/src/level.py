import pygame

from tiles import Tile
from settings import tile_size, _screenWidht, _screenHeight
from player import Player


# DECLARE LEVEL CLASS

class Level:
    def __init__(self, level_data, surface):

        # PROPS OF LEVEL CLASS
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    # CLASS METHOD TO IDENTIFY REQ TILES FOR LEVEL
    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # USE ENUMERATE TO GET VALUE AND INDEX OF ARRAY
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size

                if cell == "1":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)

                if cell == "P":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < _screenWidht / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0

        elif player_x > _screenWidht * (3 / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0

        else:
            self.world_shift = 0
            player.speed = 8

    # LEVEL CLASS METHOD - HORIZONTAL COLLISIONS
    def horizontal_movement_collision(self):

        # DECLARE PLAYER SPRITE
        # HANDLE PLAYER MOTION
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # ITERATE THRU EVERY SPRITE
        # CHECK IF PLAYER RECT COLLIDES WITH SPRITE RECT
        # REQ CHECKING FOR LEFT OR RIGHT SURFACE COLLISION
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right

                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left

    # LEVEL CLASS METHOD - VERTICAL COLLISIONS
    def vertical_movement_collision(self):

        # DECLARE PLAYER SPRITE
        # APPLY GRAVITY i.e Y-AXIS MOVEMENT INIT to PLAYER SPRITE
        player = self.player.sprite
        player.apply_gravity()

        # ITERATE THRU EVERY SPRITE
        # CHECK IF PLAYER RECT COLLIDES WITH SPRITE RECT
        # REQ CHECKING FOR TOP OR BOTTOM SURFACE COLLISION
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.jump_limit = 0

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

    # CLASS METHOD FOR DEATH AND RESPAWN
    def death(self):
        player = self.player.sprite
        # print("y = " + str(player.rect.y) + "  x = " + str(player.rect.x))
        # print(str(_screenHeight))

        # CONDITIONAL STATEMENT TO CHECK IF PLAYER IS OUT-OF-BOUNDS IN Y-AXIS
        if player.rect.y > _screenHeight:
            return True

    # CLASS METHOD TO DRAW ALL TILES
    def run(self):

        # LEVEL TILE
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # PLAYER DRAW
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)