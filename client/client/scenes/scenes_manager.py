from typing import Dict

from .about import About
from .credits import Credits

# Import all scenes
from .game_play import gamePlay
from .loading_screen import Loading_screen
from .menu import Menu
from .scene import Scene

# Dict of all registered scenes
SCENES_MAP: Dict[str, Scene] = {
    "Menu": Menu,
    "Loading_screen": Loading_screen,
    "Gameplay": gamePlay,
    "About": About,
    "Credits": Credits,
}
