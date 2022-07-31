from typing import Dict

from scenes.about import About
from scenes.credits import Credits

# Import all scenes
from scenes.game_play import gamePlay
from scenes.loading_screen import Loading_screen
from scenes.menu import Menu
from scenes.scene import Scene

# Dict of all registered scenes
SCENES_MAP: Dict[str, Scene] = {
    "Menu": Menu,
    "Loading_screen": Loading_screen,
    "Gameplay": gamePlay,
    "About": About,
    "Credits": Credits,
}
