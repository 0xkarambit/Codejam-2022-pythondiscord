import os
from pathlib import Path

import pygame
from constants import FPS, HEIGHT, WIDTH
from scenes.game_play import gamePlay
from scenes.menu import Menu
from scenes.scene import Scene
from scenes.scenes_manager import SCENES_MAP

# Setting up the window
pygame.font.init()
pygame.mixer.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
w, h = pygame.display.get_window_size()
WIN = pygame.display.set_mode((w, h), pygame.FULLSCREEN)

print("\x1b[91m")
print(f"{w},{h}")
print("\x1b[0m")


# setting currect directory manually to be able to run the project from anywhere
os.chdir(Path(__file__).resolve().parent)


music = pygame.mixer.music.load(
    Path(__file__).resolve().parent.parent
    / "assets"
    / "Sounds"
    / "04-Meydan-Surreal-Forest.mp3"
)
pygame.mixer.music.play(-1)
pygame.display.set_caption("BugsLand")


# setting up current scene
current_scene: Scene = None


def switch_scene(new_scene: str):
    global current_scene
    if current_scene.exit():
        next_scene = SCENES_MAP.get(new_scene)
        if not next_scene:
            raise Exception(f"Scene {new_scene} not found")
        current_scene = next_scene(switch_scene)
        return True
    else:
        print("Unable to Switch Scenes !!!")
    return False


current_scene = Menu(switch_scene)


def main():
    """main loop for the game"""
    clock = pygame.time.Clock()
    while True:
        # locking FPS
        clock.tick(FPS)

        # pygame.event.get() removes the events in the queue and returns them inside a list.
        # events once removed from the queue cannot be accessed in a later call to pygame.event.get()
        # so we pass the events to the update method of the current scene
        events_list = pygame.event.get()
        for event in events_list:
            # for closing the game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # clearing screen for the next render
        white = (255, 255, 255)
        WIN.fill(white)

        # Rendering Everything
        current_scene.render()

        # updating the display
        pygame.display.update()

        # Updating Everything
        current_scene.update(events_list)


if __name__ == "__main__":
    main()
