import pygame
from constants import TILE_W


class Background:
    def __init__(self, bg_layers, speed_list):
        # todo try passing in multiple y coor list
        self.bgs = []
        self.offset = 2 * TILE_W
        self.prev_cam_pos_x = 0

        w_w, w_h = pygame.display.get_window_size()

        for layer, speed in zip(bg_layers, speed_list):
            img = layer.image
            img = pygame.transform.scale(img, (w_w, w_h))
            rect = img.get_rect(topleft=(0, 0))
            rect_r = img.get_rect(topleft=(rect.w, 0))  # rect right
            rect_l = img.get_rect(topleft=(-rect.w, 0))  # rect left

            bg_obj = {"img": img, "speed": speed, "rects": [rect_l, rect, rect_r]}

            self.bgs.append(bg_obj)

    def render(self, surface):
        for bg_obj in self.bgs:
            img = bg_obj["img"]
            rect_r, rect, rect_l = bg_obj["rects"]

            surface.blit(img, rect)
            surface.blit(img, rect_r)
            surface.blit(img, rect_l)

    def update(self, camera_pos_x):
        d_x = camera_pos_x - self.prev_cam_pos_x

        for bg_obj in self.bgs:
            # shifting image backwards according to the bg_speed
            rect_l, rect, rect_r = bg_obj["rects"]
            speed = bg_obj.get("speed")

            rect.x -= d_x * speed
            rect_r.x -= d_x * speed
            rect_l.x -= d_x * speed

            if rect_l.x < -rect.w:
                rect_l.x = rect_r.x + rect_r.w
                bg_obj.get("rects").pop(0)
                bg_obj.get("rects").append(rect_l)

            if rect_r.x > rect.w:
                rect_r.x = rect_l.x - rect_l.w
                bg_obj.get("rects").pop(-1)
                bg_obj.get("rects").insert(0, rect_r)

        self.prev_cam_pos_x = camera_pos_x

    def reset(self):
        self.prev_cam_pos_x = 0
        for bg_obj in self.bgs:
            img = bg_obj["img"]
            rect = bg_obj["rect"]

            bg_obj["rect"] = img.get_rect(topleft=(0, 0))
            bg_obj["rect_r"] = img.get_rect(
                topleft=(rect.w - self.offset, 0)
            )  # rect right
            bg_obj["rect_l"] = img.get_rect(
                topleft=(-rect.w + self.offset, 0)
            )  # rect left


# 10
# 20

# dx = -10
