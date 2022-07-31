import asyncio
import threading

import pygame
import websockets
from connection import authenticate, searching
from scenes.scene import Scene


# socket = None
async def load():
    async with websockets.connect("ws://localhost:8765") as ws:
        await authenticate(ws)
        await searching(ws, lambda m: print(f"\x1b[91m joining room {m} \x1b[0m"))


pygame.font.init()
WHITE = pygame.Color(255, 255, 255)


class Loading_screen(Scene):
    def __init__(
        self,
        switch_scene,
    ):
        print("Scene Loading_screen starts !")
        self.switch_scene = switch_scene
        self.screen = pygame.display.get_surface()
        self.scene_ended = False
        # writing Loading on the screen
        font_size = 40
        font = pygame.font.SysFont(None, font_size)
        text = "Loading"
        text_color = WHITE
        self.loading_img = font.render(text, True, text_color)

        t_w, t_h = font.size(text)
        x_padding = 80
        y_padding = 65

        w, h = pygame.display.get_window_size()
        x = w - t_w - x_padding
        y = h - t_h - y_padding

        self.text_rect = pygame.Rect(x, y, 10, 10)

        # loading bars
        self.bars = []
        self.bar_h = t_h - 5
        bar_padding = 5
        bars_count = 3

        bar_x = x + t_w + 10
        bar_w = 10

        for _ in range(bars_count):
            bar = pygame.Rect(bar_x, y - 3, bar_w, self.bar_h)
            bar_x += bar_w + bar_padding
            self.bars.append(bar)

        self.delta_h = [-2, -3, -4]  # used to reduce the height of the bars

        self.frame_interval = 4  # animation interval in frames
        self.frame_counter = 0

        # self.next_scene = "Circle_scene"
        # self.has_loaded = False

        self.thread = threading.Thread(
            target=asyncio.get_event_loop().run_until_complete, args=[load()]
        )  # doesnt work for async functions
        self.thread.daemon = True
        self.thread.start()

    def render(self):
        self.screen.fill(pygame.Color(0, 0, 0))
        self.screen.blit(self.loading_img, self.text_rect)

        # spinning circle
        for bar_rect in self.bars:
            pygame.draw.rect(self.screen, WHITE, bar_rect, 0)

    def update(self, events_list):

        if not self.thread.is_alive():
            print("CLOSED THE THREAD")
            self.switch_scene("Gameplay")

        self.frame_counter += 1
        if self.frame_counter > self.frame_interval:
            self.frame_counter = 0
            for i, bar_rect in enumerate(self.bars, 0):
                bar_rect.height += self.delta_h[i]
                bar_rect.y -= self.delta_h[i]
                # toggling increasing and decreasing the bar
                if bar_rect.height <= 1:
                    self.delta_h[i] = -self.delta_h[i]
                elif bar_rect.height >= self.bar_h:
                    self.delta_h[i] = -self.delta_h[i]

    def exit(self):
        print("Scene Loading_screen Over!")
        # To disable the timer for an event, set the milliseconds argument to 0.
        # pygame.time.set_timer(self.UPDATE_BARS, 0)
        self.scene_ended = True
        # destroy thread can't
        return True
