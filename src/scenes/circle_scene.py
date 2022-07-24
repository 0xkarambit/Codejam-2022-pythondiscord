import pygame

from components.button import Button
from scenes.scene import Scene

WIDTH, HEIGHT = 800, 600


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

    def render(self):
        self.back_btn.render()
        center = (WIDTH / 2, HEIGHT / 2)
        blue = pygame.Color(12, 32, 43)
        pygame.draw.circle(self.screen, blue, center, 300, 0)

        pygame.display.update()

    def update(self, events_list):
        self.back_btn.update(events_list)

    def exit(self):
        print("Scene Game Over !")
        self.scene_ended = True
        return True
