import pygame

from level import Level
from settings import level_map, _screenWidht, _screenHeight
from components.button import Button
from scenes.scene import Scene

class gamePlay(Scene):

    def __init__(self, switch_scene):
        # debug
        print("Init Gameplay Screen")

        _screenReso = (_screenWidht, _screenHeight)

        # create screen and init clock
        self.screen = pygame.display.set_mode(_screenReso)

        # self.screen = pygame.display.get_surface()
        self.scene_ended = False

        self.level = Level(level_map, self.screen)

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
        # Fill screen black
        self.screen.fill('black')

        self.back_btn.render()

        self.level.run()


        # pygame final display renderer
        pygame.display.update()

    def update(self, events_list):
        self.back_btn.update(events_list)

    def exit(self):
        self.scene_ended = True
        print("Game scene Ending")
        return True
