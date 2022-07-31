import random

import pygame
from components.button import Button
from components.text import Text
from constants import HEIGHT, WIDTH
from scenes.scene import Scene

# kinda bad ? YEAHHH
pygame.font.init()

developers = ["Nihal Navath", "Karambit", "DarkDragon", "Ruthless", "TheLegendBeacon"]
random.shuffle(developers)
devs_text = "\n".join(list(developers))
credits_text = devs_text


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
            Text(
                credits_text,
                WIDTH / 2 + 350,
                100,
                200,
                50,
                self.screen_surface,
                True,
                50,
                pygame.Color(105, 255, 105),
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
