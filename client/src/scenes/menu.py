import pygame
from components.button import Button
from components.text import Text
from scenes.scene import Scene

# kinda bad ? YEAHHH
pygame.font.init()


def exit_game():
    pygame.quit()
    quit()


class Menu(Scene):
    def __init__(self, switch_scene):
        print("Menu scene started")
        self.screen_surface = pygame.display.get_surface()
        self.scene_ended = False
        self.buttons = []

        w, h = pygame.display.get_window_size()

        # maybe make a btn dataclass later
        self.buttons = [
            Text(
                "BugsLand",
                w / 2 - 100,
                100,
                200,
                50,
                self.screen_surface,
                False,
                70,
                pygame.Color(223, 143, 45),
            ),
            Button(
                w / 2 - 100,
                200,
                200,
                50,
                "Play",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: switch_scene("Loading_screen"),
                # lambda: switch_scene("Gameplay"),
                self.screen_surface,
            ),
            Button(
                w / 2 - 100,
                300,
                200,
                50,
                "About",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: switch_scene("About"),
                self.screen_surface,
            ),
            Button(
                w / 2 - 100,
                400,
                200,
                50,
                "Credits",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: switch_scene("Credits"),
                self.screen_surface,
            ),
            Button(
                w / 2 - 100,
                500,
                200,
                50,
                "Exit",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                lambda: exit_game(),
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
        print("Menu scene Ending")
        return True
