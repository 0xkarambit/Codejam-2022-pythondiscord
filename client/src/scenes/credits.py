import random
import webbrowser

import pygame
from components.button import Button
from components.text import Text
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
keys = list(developers.keys())


class Credits(Scene):
    def __init__(self, switch_scene):
        self.screen_surface = pygame.display.get_surface()
        self.scene_ended = False
        self.buttons = []
        window_w, _ = pygame.display.get_window_size()

        # maybe make a btn dataclass later
        self.buttons = [
            Text(
                "Developers",
                window_w / 2 - 105,
                30,
                200,
                50,
                self.screen_surface,
                False,
                70,
                pygame.Color(223, 143, 45),
            ),
            Button(
                window_w / 2 - 110,
                100,
                220,
                50,
                keys[0],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[keys[0]]),
                self.screen_surface,
            ),
            Button(
                window_w / 2 - 100,
                150,
                200,
                50,
                keys[1],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[keys[1]]),
                self.screen_surface,
            ),
            Button(
                window_w / 2 - 100,
                200,
                200,
                50,
                keys[2],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[keys[2]]),
                self.screen_surface,
            ),
            Button(
                window_w / 2 - 100,
                250,
                200,
                50,
                keys[3],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[keys[3]]),
                self.screen_surface,
            ),
            Button(
                window_w / 2 - 145,
                300,
                300,
                50,
                keys[4],
                50,
                pygame.Color(255, 255, 255),
                pygame.Color(105, 255, 105),
                lambda: webbrowser.open(developers[keys[4]]),
                self.screen_surface,
            ),
            Button(
                window_w / 2 - 400,
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
