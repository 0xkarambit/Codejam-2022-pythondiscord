import pygame
from components.button import Button
from level import Level
from scenes.scene import Scene
from settings import _screenHeight, _screenWidth


class gamePlay(Scene):
    def __init__(self, switch_scene):
        # debug
        print("Init Gameplay Screen")

        _screenReso = (_screenWidth, _screenHeight)

        # create screen and init clock
        # self.screen = pygame.display.set_mode(_screenReso, pygame.RESIZABLE)
        self.screen = pygame.display.set_mode(_screenReso, pygame.SCALED)
        # self.screen = pygame.display.set_mode(_screenReso)

        # self.screen = pygame.display.get_surface()
        self.scene_ended = False

        self.level = Level(self.screen)

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
        self.screen.fill("black")

        self.back_btn.render()

        self.level.render()

        # pygame final display renderer
        pygame.display.update()

    def update(self, events_list):
        self.back_btn.update(events_list)
        self.level.update(events_list)
        if self.level.death() == True:
            # self.level = Level(self.screen)
            self.level.reset()

    def exit(self):
        self.scene_ended = True
        print("Game scene Ending")
        return True
