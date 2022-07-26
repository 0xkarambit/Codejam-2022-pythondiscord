import pygame
from components.button import Button
from scenes.scene import Scene

# BAD multile sources of truth
WIDTH, HEIGHT = 800, 600

# kinda bad ? YEAHHH
pygame.font.init()


class Menu(Scene):
    def __init__(self, switch_scene):
        print("Menu scene started")
        self.screen_surface = pygame.display.get_surface()
        self.scene_ended = False
        self.buttons = []

        # maybe make a btn dataclass later
        self.buttons = [
            Button(
                WIDTH / 2 - 100,
                100,
                200,
                50,
                "Play",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: switch_scene("Loading_screen"),
                self.screen_surface,
            )
        ]

    def render(self):
        for btn in self.buttons:
            btn.render()

        pygame.display.update()

    def update(self, events_list):
        for btn in self.buttons:
            btn.update(events_list)

    def exit(self):
        self.scene_ended = True
        print("Menu scene Ending")
        return True
