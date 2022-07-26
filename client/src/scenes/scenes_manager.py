from typing import Dict

# Import all scenes
from scenes.circle_scene import Circle_scene
from scenes.game_play import gamePlay
from scenes.loading_screen import Loading_screen
from scenes.menu import Menu
from scenes.scene import Scene

# Dict of all registered scenes
SCENES_MAP: Dict[str, Scene] = {
    "Menu": Menu,
    "Circle_scene": Circle_scene,
    "Loading_screen": Loading_screen,
    "Gameplay": gamePlay,
}
