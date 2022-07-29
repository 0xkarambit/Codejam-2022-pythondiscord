import pygame
from utils.spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_path):
        super().__init__()

        self.spritesheet = Spritesheet(spritesheet_path)
        self.spritesheet.select_animation("idle_anim")
        self.image = self.spritesheet.get_sprite()
        self.rect = self.image.get_rect(topleft=pos)

        # PLAYER MOVEMENT
        self.speed = 5
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -7
        self.jump_limit = 0
        self.in_air_after_jump = False

    def get_input(self):
        # print("self.in_air_after_jump", self.in_air_after_jump)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.spritesheet.select_animation("run_anim")

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.spritesheet.select_animation("run_anim", True)

        else:
            self.direction.x = 0
            if not self.in_air_after_jump:
                self.spritesheet.select_animation("idle_anim")

        if keys[pygame.K_UP]:
            if self.jump_limit < 15:
                self.jump()

        if self.in_air_after_jump:
            need_inverted = self.direction.x == -1
            if self.spritesheet.selected_animation.startswith("jump_up_anim"):
                # print(need_inverted, self.direction.x)
                self.spritesheet.switch_animation("jump_up_anim", need_inverted)
            else:
                self.spritesheet.select_animation("jump_up_anim", need_inverted)
                self.spritesheet.lock_animation()

        (frame_changed, animation_finished) = self.spritesheet.update()
        if frame_changed:
            self.image = self.spritesheet.get_sprite()
        # if the player is in air | has jumped
        # if self.in_air_after_jump:
        #     self.fc += 1
        #     if self.fc > self.frame_interval_jump:
        #         self.fc = 0
        #         self.image = self.jump_ss.get_sprite()
        #         self.jump_ss.next()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.in_air_after_jump = True
        self.jump_limit += 1

    def update(self):
        self.get_input()
