import pygame

# move this to constants file
MAXHEALTH = 100


class Player:
    def __init__(self, x, y, w, h, color: pygame.Color):
        self.health = MAXHEALTH
        # self.name = "Player 1"
        # self.sprites =
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        # self.rect
        self.rect = pygame.Rect(x, y, w, h)

        # TODO : tweak physics values
        # movement physics
        self.JUMP = 30
        self.ACCELERATION = 2
        self.ACC_DOWN = 10

        self.FRICTION = 0.5  # shouldnt this come from a world object ?
        # self.DRAG = 2  # shouldnt this come from a world object ?
        self.GRAVITY = 2  # shouldnt this come from a world object ?

        self.MAX_VEL = 10

        self.vel_x = 0
        self.vel_y = 0
        self.can_jump = True

        # input for controls
        self.inputs = {}

        # temporary
        self.ground_ = 500

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)

    # will have to interact with the tiles_array and other physical entities like traps for collision detection
    def update(self, events):
        # setting key presses because pygame raises event for KEYDOWN only when the
        # key is first pressed NOT UNTILL ITS PRESSED !
        for event in events:
            if event.type == pygame.KEYDOWN:
                # print(f"event.key = {event.key}, {event.unicode}, {event.mod}")
                self.inputs[event.unicode] = True
            if event.type == pygame.KEYUP:
                self.inputs[event.unicode] = False

        # looping over pressed keys ! (CONTINUOUSLY PRESSED DOWN ON THE KEYBOARD)
        for key, is_down in self.inputs.items():
            # movign left
            if key == "a" and is_down:
                self.vel_x -= self.ACCELERATION

            # movign right
            if key == "d" and is_down:
                self.vel_x += self.ACCELERATION

            # Jumping   # todo jumping is different
            if key == "w" and is_down:
                if self.can_jump:
                    self.vel_y -= self.JUMP  # self.ACC_Y ???
                    self.can_jump = False

            # coming down faster now !
            if key == "s" and is_down:
                # only add if the Player is not on ground !
                self.vel_y += self.ACC_DOWN

        self.apply_friction()
        self.apply_gravity()  # todo somethings fishy

        # Ceiling the max velocity
        self.vel_x = self.vel_x if self.vel_x < self.MAX_VEL else self.MAX_VEL

        # Changing player coordinates
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # collision detection with the window walls
        width, height = pygame.display.get_window_size()
        if self.rect.x + self.rect.width > width:
            self.rect.x = width - self.rect.width
            self.vel_x = 0
        elif self.rect.x < 0:
            self.rect.x = 0
            self.vel_x = 0

        if self.rect.y + self.rect.height > height:
            self.rect.y = height - self.rect.height
            self.vel_y = 0
        elif self.rect.y < 0:
            self.rect.y = 0
            self.vel_y = 0

    def apply_friction(self):
        """Apply Friction to the player when its moving"""
        x_mov = self.get_x_movement()
        if x_mov == "LEFT":
            self.vel_x += self.FRICTION
            if self.vel_x > 0:
                self.vel_x = 0
        if x_mov == "RIGHT":
            self.vel_x -= self.FRICTION
            if self.vel_x < 0:
                self.vel_x = 0
        # todo: hmm friction should be a bit less in the bit maybe use DRAG here instead

    def apply_gravity(self):
        """Apply gravity to the player when its not on the ground"""
        if self.rect.y + self.rect.height < self.ground_:
            self.vel_y += self.GRAVITY
        elif self.rect.y + self.rect.height > self.ground_:
            self.vel_y = 0
            self.rect.y = self.ground_ - self.rect.height
            if not self.can_jump:
                self.can_jump = True

    def get_movement_dir(self):
        """returns the direction of currect player movement

        Returns:
            Tuple: x direction, y direction
        """
        return (self.get_x_movement(), self.get_y_movement())

    def get_x_movement(self):
        if self.vel_x > 0:
            return "RIGHT"
        if self.vel_x < 0:
            return "LEFT"

    def get_y_movement(self):
        if self.vel_y > 0:
            return "DOWN"
        if self.vel_y < 0:
            return "UP"
