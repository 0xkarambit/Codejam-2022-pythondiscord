import pygame
from components.button import Button
from level import Level
from scenes.scene import Scene


class gamePlay(Scene):
    def __init__(self, switch_scene):

        self.screen = pygame.display.get_surface()
        self.scene_ended = False
        self.switch_scene = switch_scene
        self.level = Level(self.screen)

    def render(self):
        self.level.render()

    def update(self, events_list):
        if self.level.complete:
            self.switch_scene("Menu")
            return
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
        return True
