import json
from pprint import pprint
from typing import Dict

import pygame


class Spritesheet:
    def __init__(self, filename):
        """Class to parse Spritesheets for animation

        Args:
            filename (str): path to spritesheet

        """
        self.filename = filename
        self.datafile = self.filename.replace("png", "json")

        # loading json data for the spritesheet
        with open(self.datafile) as f:
            self.data = json.load(f)
        f.close()

        # order of animations data in json according to their appearance in the spritesheet
        self.animation_names = self.data.get("animations")

        self.animations: Dict[str, list[pygame.Surface]] = {}
        self.frame_interval = self.data.get(
            "frame_interval"
        )  # no of frames in which the current frame is changed to next frame in the animation

        # loading the .png spritesheet as a surface
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.parse_data()

        # adding inverted animations names too
        self.animation_names += [i + "_inverted" for i in self.animation_names]

        # STATE

        # currently selected sprite
        self.fc = 0
        self.animation_index = 0
        self.selected_animation = "idle"  # ?
        self.select_animation_len = 0

        # to be used during locked animations | animations that cannot be interrupted
        self.locked = False
        # for queuing animation
        self.next_animation = ""

    def update(self) -> None:
        """incrementes the frame_counter and the animation_frames

           * must be called every frame ! *

        Returns:
            Tuple[bool, bool]: (frame_changed, animation_finished)
        """
        self.fc += 1
        if self.fc >= self.frame_interval:
            self.fc = 0
            # time to move to next frame of the animation !
            self.animation_index += 1

            if self.animation_index >= self.select_animation_len:
                self.animation_index = 0
                if self.next_animation != "":
                    self.select_animation(self.next_animation, forced=True)
                    self.next_animation = ""
                return (True, True)
            return (True, False)
        return (False, False)

    def queue_animation(self, animation: str, inverted: bool = False):
        # if self.next_animation == "":
        #     # to be used when the current animation is to be stopped automatically after completing
        #     self.next_animation = animation
        #     return
        animation = animation + "_inverted" if inverted else animation
        if animation in self.animation_names:
            self.next_animation = animation

    def invert_animation(self, inverted):
        animation = self.selected_animation
        already_inverted = animation.endswith("_inverted")
        if inverted and not already_inverted:
            self.selected_animation += "_inverted"
        if not inverted and already_inverted:
            self.selected_animation = animation.replace("_inverted", "")

        # animation = animation + "_inverted" if inverted else animation
        # if animation in self.animation_names:
        #     self.selected_animation = animation

    def select_animation(
        self, animation: str, inverted=False, *, forced=False, noreset=False
    ):
        animation = animation + "_inverted" if inverted else animation

        if self.locked and not forced:
            # print("ANIMATION SEQUENCE HAS BEEN LOCKED")
            return False

        # dont switch/reset animation if its the one going on !
        if self.selected_animation == animation:
            return False

        if animation in self.animation_names:
            self.selected_animation = animation
            self.select_animation_len = self.animations[animation].get("length")
            if not noreset:
                self.fc = 0
                self.animation_index = 0
        else:
            raise Exception(
                f"No such animation {animation} exists on spritesheet {self.filename}"
            )

    def get_sprite(self) -> pygame.surface:
        # pprint(self.animations[self.selected_animation])
        return self.animations[self.selected_animation].get("sprites")[
            self.animation_index
        ]

    def lock_animation(self):
        self.locked = True

    def unlock_animation(self):
        self.locked = False

    def parse_data(self):
        # ? animation_data can also have unique `frame_switching_interval` for each row !

        # general frame_w & frame_h which majority of the items would have in a spritesheet
        default_frame_w, default_frame_h = self.data.get("frame_w"), self.data.get(
            "frame_h"
        )
        x, y = 0, 0
        # looping over animation_names to parse spritesheet in correct order
        for animation_name in self.animation_names:

            animation_data = self.data.get(animation_name)

            # frame_count must always exist !
            f_count = animation_data.get("frame_count")
            # changing f_w if a special f_w has been defined for the row
            f_w = animation_data.get("frame_w", default_frame_w)
            # changing f_h if a special f_h has been defined for the row
            f_h = animation_data.get("frame_h", default_frame_h)

            # pprint(animation_data)

            frames = []  # all sprites in this animation sequence
            inverted_frames = []

            # x, y = animation_data.start_x, animation_data.start_y

            for _ in range(f_count):
                frame = pygame.Surface((f_w, f_h))

                # color that is meant to be transparent, flag to make it faster
                frame.set_colorkey((0, 0, 0), pygame.RLEACCEL)
                frame.blit(self.sprite_sheet, (0, 0), (x, y, f_w, f_h))
                frames.append(frame)

                # ? we can add to_store_inverted on the json file !
                inverted_frame = pygame.transform.flip(frame, True, False)
                inverted_frames.append(inverted_frame)

                x += f_w

            # adding to list of animations
            sprites_list_obj = {"sprites": frames, "length": f_count}
            self.animations.setdefault(animation_name, sprites_list_obj)

            sprites_list_inverted_obj = {"sprites": inverted_frames, "length": f_count}
            self.animations.setdefault(
                animation_name + "_inverted", sprites_list_inverted_obj
            )
            # print(f"\x1b[91m{animation_name}_inverted\x1b[0m")

            # reseting x to scan next row from the beginning and inc y to shift to next col of sprites
            x = 0
            y += f_h


""""
usage:
    selected = select_sprite_anim("animation_name")
    img_to_render = spritesheet.get()
    img_changed_ = spritesheet.update()

    # called every frame to keep track of changes to current sprite to be rendered &
    #  have customised frame_switching_interval for each different type of animation

    {
      animations
      frame_interval
      frame_w, frame_h
      animation: {
        frame_count,
        frame_w, ?
        frame_h ?
      }
    }
"""
