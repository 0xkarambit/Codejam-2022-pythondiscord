from abc import ABC, abstractmethod


class Scene(ABC):
    @abstractmethod
    def __init__():
        pass

    @abstractmethod
    def render():
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def exit():
        pass
