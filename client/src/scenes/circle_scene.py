import asyncio
import random
import threading

import pygame
import websockets
from components.button import Button
from components.other_player import Other_Player
from components.player import Player
from connection import update_data
from constants import HEIGHT, WIDTH
from scenes.scene import Scene

NO_OF_PLAYERS = 2

other_positions = []


def update_pos(positions):
    global other_positions
    other_positions = positions


async def tick(player):
    async with websockets.connect("ws://localhost:8765") as ws:
        await update_data(ws, [player.rect.x, player.rect.y], update_pos)
        # dont use this code v.high cpu usage
        # t = time.time()
        # while True:
        #     if time.time() - t > 1:
        #         t = time.time()


class Circle_scene(Scene):
    def __init__(self, switch_scene):
        print("Scene Game starts !")
        self.screen = pygame.display.get_surface()
        self.scene_ended = False
        self.back_btn = Button(
            50,
            50,
            80,
            30,
            "Go Back",
            30,
            pygame.Color(12, 43, 64),
            None,
            lambda: switch_scene("Menu"),
            self.screen,
        )

        # main player
        self.player = Player(100, 100, 50, 50, pygame.Color(254, 89, 0))

        # creating other players
        self.other_players = []
        for i in range(NO_OF_PLAYERS):
            other_player = Other_Player(i, 100, 50, 50, random_color(), 100)
            self.other_players.append(other_player)

    def render(self):
        self.back_btn.render()
        center = (WIDTH / 2, HEIGHT / 2)
        blue = pygame.Color(12, 32, 43)
        pygame.draw.circle(self.screen, blue, center, 150, 0)

        # rendering other players
        for other_player in self.other_players:
            other_player.render(self.screen)

        self.player.render(self.screen)

    def update(self, events_list):
        self.back_btn.update(events_list)
        self.player.update(events_list)

        # sending and receiving player positions
        self.thread = threading.Thread(
            target=asyncio.get_event_loop().run_until_complete, args=[tick(self.player)]
        )
        self.thread.daemon = True
        self.thread.start()

        # updating self.other_players positions
        for i, pos in enumerate(other_positions, 0):
            if isinstance(pos, list):  # we have to check every time.. sed
                self.other_players[i].rect.x = pos[0]
                self.other_players[i].rect.y = pos[1]

    def exit(self):
        print("Scene Game Over !")
        self.scene_ended = True
        return True


def random_color() -> pygame.Color:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return pygame.Color(r, g, b)
