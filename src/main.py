import pygame

from menu import Menu
from scene import Scene

# Setting up the window
pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BugsLand")
FPS = 60


should_run = True


def stop_running():
    global should_run
    should_run = False


current_scene: Scene = Menu(stop_running)


def switch_scene(new_scene: Scene):
    if current_scene.exit() == True:
        current_scene = new_scene()
        return True
    return False


def main():
    """main loop for the game"""
    clock = pygame.time.Clock()
    while should_run:
        # locking FPS
        clock.tick(FPS)

        # Rendering Everything
        current_scene.render()

        # Updating Everything
        current_scene.update()

    if current_scene.scene_ended != True:
        current_scene.exit()
    pygame.quit()


if __name__ == "__main__":
    main()
