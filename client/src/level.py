import os

import pygame
from camera import Camera
from player import Player
from pytmx import util_pygame
from settings import _screenHeight, _screenWidht
from tiles import Tile


class Level:
    def __init__(self, surface):

        # PROPS OF LEVEL CLASS
        self.display_surface = surface
        self.has_loaded = False
        self.load_map()
        self.setup_level()
        self.camera = Camera()

    def reset(self):
        self.setup_level()
        self.camera = Camera()

    def load_map(self):
        if os.getcwd().endswith("\\client\\src"):
            # changing cwd because all asset paths are set relative to ./Levels
            os.chdir("./Levels")

        self.tmx_data = util_pygame.load_pygame("./1.tmx")
        self.has_loaded = True

        # os.chdir("./..")  # reseting the cwd

    # CLASS METHOD TO IDENTIFY REQ TILES FOR LEVEL
    def setup_level(self):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.bg_color = self.tmx_data.background_color

        tiles_layer = self.tmx_data.get_layer_by_name("Tile Layer 1")
        for x, y, surf in tiles_layer.tiles():
            pos = (x * surf.get_width(), y * surf.get_height())  # 16 by 16 tiles
            tile = Tile(pos, surf, self.tiles)
            self.tiles.add(tile)

        player_layer = self.tmx_data.get_layer_by_name("Player")
        for obj in player_layer:
            pos = (obj.x, obj.y)
            if obj.image:
                p = Player(pos, obj.image)
                self.player.add(p)
            else:
                path = obj.properties.get("spritesheet")
                p = Player(pos, path)
                self.player.add(p)

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
                    player.in_air_after_jump = False
                    player.spritesheet.unlock_animation()

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

    def render(self):
        # background
        self.display_surface.fill(self.bg_color)
        # drawing tiles relative to camera
        for tile in self.tiles.sprites():
            # tiles are looped rowwise
            if tile.rect.x > self.camera.pos.x and tile.rect.x < (
                self.camera.pos.x + self.camera.draw_distance.x
            ):
                pos = pygame.Vector2(tile.rect.x, tile.rect.y)
                rel_pos = self.camera.get_relative_coors(pos)
                rel_rect = tile.image.get_rect(topleft=rel_pos)
                self.display_surface.blit(tile.image, rel_rect)

        # drawing player relative to camera
        p = self.player.sprite
        # converting player coordinates to relative camera coordinates
        p_pos = pygame.Vector2(p.rect.x, p.rect.y)
        p_rel_pos = self.camera.get_relative_coors(p_pos)
        p_rel_rect = p.image.get_rect(topleft=p_rel_pos)
        # rendering the player img
        p_img = p.image
        self.display_surface.blit(p_img, p_rel_rect)

    def update(self, events_list):
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.camera.follow_player(self.player.sprite)
