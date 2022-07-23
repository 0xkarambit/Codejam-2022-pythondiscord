from dataclasses import dataclass
from typing import Callable

import pygame

from scene import Scene

# BAD multile sources of truth
WIDTH, HEIGHT = 800, 600

# kinda bad ? YEAHHH
pygame.font.init()


class Menu(Scene):
    def __init__(self, stop_running: Callable):
        print("Menu scene started")
        self.WIN = pygame.display.get_surface()
        self.scene_ended = False
        self.stop_running = stop_running
        self.buttons = []

        self.buttons = [
            Button(
                WIDTH / 2 - 50,
                100,
                100,
                30,
                "Play",
                48,
                pygame.Color(123, 243, 145),
                pygame.Color(223, 143, 45),
                self.WIN,
            )
        ]

    def render(self):
        white = (255, 255, 255)
        self.WIN.fill(white)
        # WIN.blits

        for btn in self.buttons:
            btn.render()

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("GOT HERE !")
                self.stop_running()

    def exit(self):
        self.scene_ended = True
        print("Menu scene Ending")


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str,
        font_size: int,
        bgColor: pygame.Color,
        color: pygame.Color,
        screen_surface: pygame.surface,
    ):
        self.text = text
        self.font_size = font_size
        self.bgColor = bgColor
        self.color = color
        self.screen_surface = screen_surface

        self.rect = pygame.Rect(x, y, w, h)
        self.text_rect = pygame.Rect(x, y, w, h)

        font = pygame.font.SysFont(None, font_size)
        t_w, t_h = font.size(text)  # text width , height
        self.img = font.render(text, True, self.color)  # we dont need to store text btw

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(
            self.screen_surface, self.bgColor, self.rect, 5
        )  # 5 is BorderWidth of the rect

        self.screen_surface.blit(self.img, self.rect)
