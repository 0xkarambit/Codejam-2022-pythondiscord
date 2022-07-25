from typing import Dict

# Import all scenes
from scenes.menu import Menu
from scenes.scene import Scene
from scenes.game_play import gamePlay

# Dict of all registered scenes
SCENES_MAP: Dict[str, Scene] = {"Menu": Menu, "Gameplay": gamePlay}
