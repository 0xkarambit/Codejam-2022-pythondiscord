import asyncio
import os
import threading

import pygame
import websockets
from camera import Camera
from connection import update_data
from other_player import OtherPlayer
from player import Player
from pytmx import util_pygame
from settings import TILE_W, _screenHeight, _screenWidth
from tiles import Tile
from utils.background import Background

other_player = {}


def update_other_player_data(data):
    global other_player
    print("\x1b[94m")
    print("data", data)
    if data == []:
        return
    x, y, is_dead, anim = data[0]
    print([x, y, is_dead, anim])
    print("\x1b[0m")

    other_player.rect.x = x
    other_player.rect.y = y
    other_player.is_dead = is_dead
    other_player.spritesheet.selected_animation = anim


async def tick(player):
    async with websockets.connect("ws://localhost:8765") as ws:
        anim = player.spritesheet.selected_animation
        await update_data(
            ws,
            [player.rect.x, player.rect.y, player.is_dead, anim],
            update_other_player_data,
        )


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
        self.background.reset()
        self.camera = Camera()

    def load_map(self):
        if os.getcwd().endswith("\\client\\src"):
            # changing cwd because all asset paths are set relative to ./Levels
            os.chdir("./Levels")

        self.tmx_data = util_pygame.load_pygame("./1.tmx")
        self.has_loaded = True

        # print(self.tmx_data.get_layer_by_name("Background"))
        self.bg_layer = self.tmx_data.get_layer_by_name("Background")

        self.background = Background([self.bg_layer], [2])

        # os.chdir("./..")  # reseting the cwd

    # CLASS METHOD TO IDENTIFY REQ TILES FOR LEVEL
    def setup_level(self):
        global other_player
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
                # OtherPlayer
                other_player = OtherPlayer((0, 0), path)

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

        # TODO NOTIFY OTHER PLAYER OF DEATH
        # CONDITIONAL STATEMENT TO CHECK IF PLAYER IS OUT-OF-BOUNDS IN Y-AXIS
        if player.rect.y > _screenHeight:
            return True

    def render(self):
        # background
        self.background.render(self.display_surface)
        # drawing tiles relative to camera

        for tile in self.tiles.sprites():
            # tiles are looped rowwise
            if (
                tile.rect.x >= self.camera.pos.x - self.camera.offset
                and tile.rect.x < (self.camera.pos.x + self.camera.draw_distance.x)
            ):
                pos = pygame.Vector2(tile.rect.x, tile.rect.y)
                rel_pos = self.camera.get_relative_coors(pos)
                rel_rect = tile.image.get_rect(topleft=rel_pos)
                self.display_surface.blit(tile.image, rel_rect)

        # drawing player relative to camera
        player = self.player.sprite
        player.render(self.display_surface, self.camera)

        # rendering the other_player
        global other_player
        other_player.render(self.display_surface, self.camera)

    def update(self, events_list):
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.camera.follow_player(self.player.sprite)
        # print(self.camera.pos)
        self.background.update(self.camera.pos.x)

        # sending and receiving player positions
        self.thread = threading.Thread(
            target=asyncio.get_event_loop().run_until_complete,
            args=[tick(self.player.sprite)],
        )
        self.thread.daemon = True
        self.thread.start()
