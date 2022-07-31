import pygame
from utils.spritesheet import Spritesheet


class OtherPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_path):
        super().__init__()

        self.spritesheet = Spritesheet(spritesheet_path)
        self.effects_spritesheet = Spritesheet(spritesheet_path)
        self.spritesheet.select_animation("idle_anim")
        self.prev_animation = ""
        self.image = self.spritesheet.get_sprite()
        self.rect = self.image.get_rect(topleft=pos)

        # possible states -> jump, run, idle, sprint ?
        # pos, dir, self.spritesheet.selected_animation
        self.is_dead = False

    def render(self, surface, camera):
        coor = pygame.Vector2(self.rect.x, self.rect.y)
        rel_coor = camera.get_relative_coors(coor)

        rel_rect = self.image.get_rect(topleft=rel_coor)
        surface.blit(self.image, rel_rect)

    def update(self):
        (frame_changed, animation_finished) = self.spritesheet.update()
        if frame_changed:
            self.image = self.spritesheet.get_sprite()

        # self.fc += 1
        # # reseting speed to normal after sprinting
        # if self.fc > self.frames_interval:
        #     self.fc = 0
        #     if self.state == "sprinting":
        #         self.reset_speed()


# update -> rendering (DONT send relative coors ig ??? make them relative here only)
