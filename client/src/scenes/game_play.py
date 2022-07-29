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

    def render(self):
        self.level.render()

    def update(self, events_list):
        self.level.update(events_list)
        if self.level.death() == True:
            # self.level = Level(self.screen)
            self.level.reset()

    def exit(self):
        self.scene_ended = True
        print("Game scene Ending")
        return True
