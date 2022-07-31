import pygame
from utils.spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, spritesheet_path):
        super().__init__()
        self.default_pos = pos
        self.spritesheet = Spritesheet(spritesheet_path)
        self.spritesheet.select_animation("idle_anim")
        self.image = self.spritesheet.get_sprite()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        # todo rm |  for development
        # self.rect.w = 64
        # self.rect.h = 64

        # PLAYER MOVEMENT
        self.default_speed = 8
        self.speed = self.default_speed
        self.sprint_speed = self.speed * 2
        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.4  # 0.8
        self.jump_speed = -9
        self.jump_limit = 0
        self.in_air_after_jump = False
        self.last_direction = 1
        self.state = "idle"
        # possible states -> jump, run, idle, sprint ?
        # pos, dir, self.spritesheet.selected_animation
        self.is_dead = False
        # self.respawn_time = 30 # no of intervals so 30 * 10 = 300 frames game @ 60 fps so 5 Seconds roughly
        self.respawn_time = 5  # in seconds

        # frame counting
        self.fc = 0
        self.frames_interval = 10
        self.REVIVE_SIGNAL = pygame.USEREVENT + 1

    def death(self):
        if not self.is_dead:
            self.is_dead = True
            self.dir = 0
            self.in_air_after_jump = False
            self.last_direction = 1
            pygame.time.set_timer(self.REVIVE_SIGNAL, 1000 * self.respawn_time)

    def respawn(self):
        self.is_dead = False
        # to unset the timer !
        pygame.time.set_timer(self.REVIVE_SIGNAL, 0)

        self.rect.x = self.default_pos[0]
        self.rect.y = self.default_pos[1]
        print()
        print("THE PLAYER HAS RESPAWNED !")
        # self.rect.x = last_check_point_x
        # self.rect.y = last_check_point_y

    def reset_speed(self):
        self.speed = self.default_speed

    def sprint(self):
        self.speed = self.sprint_speed
        self.spritesheet.select_animation("pushing_foward_anim")
        self.spritesheet.queue_animation("idle_anim")
        self.state = "sprinting"

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.last_direction = 1
            self.spritesheet.select_animation("run_anim")
            # self.set_state("run")  # todo rm me

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.last_direction = -1
            self.spritesheet.select_animation("run_anim", True)
            # self.set_state("run")  # todo rm me

        else:
            self.direction.x = 0
            if not self.in_air_after_jump:
                inverted = self.last_direction == -1
                self.spritesheet.select_animation("idle_anim", inverted)
                # self.set_state("idle")  # todo rm me

        if keys[pygame.K_UP] or keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.jump_limit < 12:
                need_inverted = self.last_direction == -1

                # show double jump animation if *already in air*
                if self.in_air_after_jump:
                    # was in the air already
                    self.spritesheet.select_animation(
                        "jump_double_anim", need_inverted, forced=True
                    )
                    self.spritesheet.queue_animation("jump_up_anim", need_inverted)
                else:
                    # jumping for the first time
                    self.spritesheet.select_animation(
                        "before_or_after_jump_srip_2", need_inverted, forced=True
                    )
                    self.spritesheet.queue_animation("jump_up_anim", need_inverted)
                    # effect_after_jump_dust_anim

                self.spritesheet.lock_animation()
                self.jump()

        if keys[pygame.K_LSHIFT]:
            self.sprint()

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            # self.jump_speed
            self.direction.y += abs(self.jump_speed) / 10

        if self.in_air_after_jump:
            # switching face direction when moving in different direction
            need_inverted = self.last_direction == -1
            if self.spritesheet.selected_animation.startswith("jump_up_anim"):
                self.spritesheet.invert_animation(need_inverted)

            # switching to down jump when comming down
            if self.direction.y >= 0:
                self.spritesheet.select_animation(
                    "jump_down_anim", need_inverted, forced=True, noreset=True
                )
            # locking animation so that other run_anim or idle_anim does not play when jumped
            # unlocked when the player comes on ground
            self.spritesheet.lock_animation()

    def apply_gravity(self):
        if self.is_dead:
            return
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.in_air_after_jump = True
        self.jump_limit += 1

    def update(self, events):
        # respawn counter
        for e in events:
            print()
            print(e.type)
            if e.type == self.REVIVE_SIGNAL:
                self.respawn()

        if self.is_dead:
            return

        # accept player input
        self.get_input()

        # self.rect.x += self.direction.x * self.speed
        # self.apply_gravity()

        (frame_changed, animation_finished) = self.spritesheet.update()
        if frame_changed:
            self.image = self.spritesheet.get_sprite()
            # todo rm | for development
            # self.image = pygame.transform.scale(self.image, (self.rect.w, self.rect.h))

        self.fc += 1
        # reseting speed to normal after sprinting
        if self.fc > self.frames_interval:
            self.fc = 0
            if self.state == "sprinting":
                self.reset_speed()

    def render(self, surface, camera):
        if self.is_dead:
            return
        # converting player coordinates to relative camera coordinates
        coor = pygame.Vector2(self.rect.x, self.rect.y)
        rel_coor = camera.get_relative_coors(coor)
        # p_rel_pos = self.camera.get_relative_coors(p_pos)
        rel_rect = self.image.get_rect(topleft=rel_coor)
        # rendering the player img
        surface.blit(self.image, rel_rect)
