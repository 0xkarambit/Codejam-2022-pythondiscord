import random
import webbrowser

import pygame
from components.button import Button
from components.text import Text
from constants import HEIGHT, WIDTH
from scenes.scene import Scene

# kinda bad ? YEAHHH
pygame.font.init()

developers = {
    "Nihal Navath": "https://github.com/NihalNavath",
    "Karambit": "https://github.com/HarshitJoshi9152",
    "DarkDragon": "https://github.com/Arghya-AB",
    "Ruthless": "https://github.com/nsk126",
    "TheLegendBeacon": "https://github.com/TheLegendBeacon",
}


class Credits(Scene):
    def __init__(self, switch_scene):
        self.screen_surface = pygame.display.get_surface()
        self.scene_ended = False
        self.buttons = []

        # maybe make a btn dataclass later
        self.buttons = [
            Text(
                "Developers",
                WIDTH / 2 - 90,
                30,
                200,
                50,
                self.screen_surface,
                False,
                70,
                pygame.Color(223, 143, 45),
            ),
            Button(
                WIDTH / 2 + 350,
                100,
                200,
                50,
                list(developers.keys())[0],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[list(developers.keys())[0]]),
                self.screen_surface,
            ),
            Button(
                WIDTH / 2 + 350,
                150,
                200,
                50,
                list(developers.keys())[1],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[list(developers.keys())[1]]),
                self.screen_surface,
            ),
            Button(
                WIDTH / 2 + 350,
                200,
                200,
                50,
                list(developers.keys())[2],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[list(developers.keys())[2]]),
                self.screen_surface,
            ),
            Button(
                WIDTH / 2 + 350,
                250,
                200,
                50,
                list(developers.keys())[3],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[list(developers.keys())[3]]),
                self.screen_surface,
            ),
            Button(
                WIDTH / 2 + 350,
                300,
                200,
                50,
                list(developers.keys())[4],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[list(developers.keys())[4]]),
                self.screen_surface,
            ),
            Button(
                WIDTH / 2 - 400,
                30,
                200,
                50,
                "<---",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: switch_scene("Menu"),
                self.screen_surface,
            ),
        ]

    def render(self):
        for btn in self.buttons:
            btn.render()

        pygame.display.update()

    def update(self, events_list):
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.update(events_list)

    def exit(self):
        self.scene_ended = True
        return True
