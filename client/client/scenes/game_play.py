import pygame
from ..components.button import Button
from ..level import Level
from .scene import Scene


class gamePlay(Scene):
    def __init__(self, switch_scene):
        # debug
        print("Init Gameplay Screen")

        # create screen and init clock
        # self.screen = pygame.display.set_mode(_screenReso, pygame.RESIZABLE)
        # self.screen = pygame.display.set_mode(_screenReso, pygame.SCALED)
        # adding pygame.FULLSCREEN didnt work
        # self.screen = pygame.display.set_mode(_screenReso)

        self.screen = pygame.display.get_surface()
        self.scene_ended = False

        self.level = Level(self.screen)

    def render(self):
        self.level.render()

    def update(self, events_list):
        # todo remove me i am for development
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        self.level.update(events_list)
        if self.level.death() == True:
            # self.level = Level(self.screen)
            self.level.reset()

    def exit(self):
        self.scene_ended = True
        print("Game scene Ending")
        return True
