import pygame

class Text():
    def __init__(self, text: str, x: int, y: int, w: int, h: int, screen_surface: pygame.surface, font_size: int, text_color: pygame.Color = pygame.Color(0, 0, 0)) -> None:
        """A text component that can be rendered on a surface.

        Args:
            text (str): The text to render
            x (int): The x coordinate of the text
            y (int): The y coordinate of the text
            w (int): The width of the text
            h (int): The height of the text
            screen_surface (pygame.surface): The surface to render the text on
            font_size (int): The size of the font
            text_color (pygame.Color, optional): The color of the text. Defaults to pygame.Color(0, 0, 0).
        """
        self.text = text
        self.font_size = font_size
        self.screen = screen_surface
        self.color = text_color

        self.font = pygame.font.SysFont(None, font_size)
        t_w, t_h = self.font.size(text)

        padding_x = (w - t_w) / 2
        padding_y = (h - t_h) / 2

        self.text_rect = pygame.Rect(x + padding_x, y + padding_y, w, h)


    def render(self):
        rend = self.font.render(self.text, True, self.color)
        self.screen.blit(rend, self.text_rect)