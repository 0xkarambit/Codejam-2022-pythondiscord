import pygame
from ..components.button import Button
from ..components.text import Text
from .scene import Scene

# kinda bad ? YEAHHH
pygame.font.init()


class About(Scene):
    def __init__(self, switch_scene):
        self.screen_surface = pygame.display.get_surface()
        self.scene_ended = False
        self.buttons = []
        window_w, _ = pygame.display.get_window_size()

        # maybe make a btn dataclass later
        self.buttons = [
            Text(
                "About",
                window_w / 2 - 100,
                30,
                200,
                50,
                self.screen_surface,
                False,
                70,
                pygame.Color(223, 143, 45),
            ),
            Text(
                "Game made for python discord game jam",
                window_w / 2 - 100,
                100,
                200,
                50,
                self.screen_surface,
                False,
                40,
                pygame.Color(223, 143, 45),
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
