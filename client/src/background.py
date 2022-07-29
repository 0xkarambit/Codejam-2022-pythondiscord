import pygame


class Background:
    def __init__(self, bg_layers, speed_list):
        self.bgs = []
        self.offset = 10
        self.prev_cam_pos_x = 0

        w_w, w_h = pygame.display.get_window_size()

        for layer, speed in zip(bg_layers, speed_list):
            img = layer.image
            img = pygame.transform.scale(img, (w_w, w_h))
            rect = img.get_rect(topleft=(0, 0))
            rect_r = img.get_rect(topleft=(rect.w, 0))  # rect right
            rect_l = img.get_rect(topleft=(-rect.w, 0))  # rect left

            bg_obj = {
                "img": img,
                "speed": speed,
                "rect": rect,
                "rect_r": rect_r,
                "rect_l": rect_l,
            }
            self.bgs.append(bg_obj)

    def render(self, surface):
        for bg_obj in self.bgs:
            img = bg_obj["img"]
            rect = bg_obj["rect"]
            rect_r = bg_obj["rect_r"]
            rect_l = bg_obj["rect_l"]

            surface.blit(img, rect)
            surface.blit(img, rect_r)
            surface.blit(img, rect_l)

    def update(self, camera_pos_x):
        d_x = camera_pos_x - self.prev_cam_pos_x

        for bg_obj in self.bgs:
            # shifting image backwards according to the bg_speed
            rect = bg_obj.get("rect")
            rect_r = bg_obj.get("rect_r")
            rect_l = bg_obj.get("rect_l")
            speed = bg_obj.get("speed")

            rect.x -= d_x * speed
            rect_r.x -= d_x * speed
            rect_l.x -= d_x * speed

            rects = [rect, rect_r, rect_l]
            for r in rects:
                # left side
                if r.x < -rect.w:
                    r.x = rect.w - self.offset

                # right side
                if r.x > rect.w:
                    r.x = -rect.w + self.offset

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
