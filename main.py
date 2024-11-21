from enum import Enum
from typing import List
import pygame
import constants
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame


class Orientation(Enum):
    RIGHT = 0
    LEFT = 1


class Scene:
    pass


class GameMenu(Scene):
    pass


class GameOver(Scene):
    pass


class Enemy(pygame.sprite.Sprite):
    pass


class MysteryBlock(pygame.sprite.Sprite):
    pass


class BrickBlock(pygame.sprite.Sprite):
    pass


class Goomba(Enemy):
    class State(Enum):
        RIGHT = 0
        LEFT = 1

    def __init__(self) -> None:
        pass

    pass


class Koopa(Enemy):
    class State(Enum):
        RIGHT = 0
        LEFT = 1
        SHELL = 2

    def __init__(self) -> None:
        pass

    pass


class Camera(pygame.sprite.Group):
    width, height = (420, 220)

    def __init__(self) -> None:
        self.position = Vector2(0, 0)
        self.viewport = pygame.Rect(self.position, (self.width, self.height))

    def follow_target(self, target):
        half_width = self.width // 2

        if target.position.x > self.position.x + half_width:
            # Move the camera to follow Mario
            self.position.x = target.position.x - half_width

        # Update the viewport's position
        self.viewport.x = max(0, int(self.position.x))

    def zoom(self, surface) -> pygame.Surface:
        self.viewport = self.viewport.clamp(surface.get_rect())
        display = surface.subsurface(self.viewport)
        return pygame.transform.scale(
            display.convert_alpha(),
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT),
        )


class Animation:
    def __init__(self, frames: List[pygame.Surface], duration: int = 100) -> None:
        self.frames = frames
        self.frame_duration = duration
        self.current_frame = 0
        self.last_update = 0

    def flip(self, orientation: Orientation, sprite):
        match orientation:
            case Orientation.RIGHT:
                return pygame.transform.flip(sprite, True, False)
            case Orientation.LEFT:
                return pygame.transform.flip(sprite, True, False)

    def play(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.frames[self.current_frame]
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

    def set_frame(self, surface, frame):
        surface.blit(frame, frame.get_rect())

    def draw(self, surface, hitbox):
        surface.blit(self.get_current_frame(), hitbox)

    def get_current_frame(self):
        return self.frames[self.current_frame]


class Mario(pygame.sprite.Sprite):
    max_speed: int = constants.SPEED
    jump_force: int = constants.JUMP_FORCE

    class State(Enum):
        IDLING = 0
        RUNNING = 1
        JUMPING = 2
        DUCKING = 3

    def __init__(self):
        super().__init__()
        self.idle = pygame.image.load("assets/sprites/mario/idle.png").convert_alpha()
        self.run1 = pygame.image.load("assets/sprites/mario/run1.png").convert_alpha()
        self.run2 = pygame.image.load("assets/sprites/mario/run2.png").convert_alpha()
        self.run3 = pygame.image.load("assets/sprites/mario/run3.png").convert_alpha()

        self.__lives = 10
        self.animation = Animation([self.idle, self.run1, self.run2, self.run3])

        self.sprite = self.animation.get_current_frame()
        self.hitbox = self.animation.get_current_frame().get_rect()

        self.position: Vector2 = Vector2(
            constants.TILE_WIDTH * 2, constants.TILE_HEIGHT * 11
        )
        self.acceleration: Vector2 = Vector2(2.0, 0)
        self.velocity: Vector2 = Vector2(0, 0)

        self.is_jumping = False
        self.is_on_ground = False
        self.is_grown = False

        self.last_orientation = Orientation.RIGHT

    def draw(self, surface) -> None:
        self.animation.draw(surface, self.hitbox)

    def grow(self) -> None:
        pass

    def update(self, delta) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.last_orientation != Orientation.LEFT:
                self.sprite = self.animation.flip(Orientation.LEFT, self.sprite)
                self.last_orientation = Orientation.LEFT

            self.animation.play()

            if self.velocity.x > -self.max_speed:
                self.velocity -= self.acceleration

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.last_orientation != Orientation.RIGHT:
                self.sprite = self.animation.flip(Orientation.RIGHT, self.sprite)
                self.last_orientation = Orientation.RIGHT

            self.animation.play()

            if self.velocity.x < self.max_speed:
                self.velocity += self.acceleration
        else:
            if self.velocity.x > 0:
                self.velocity -= self.acceleration
            elif self.velocity.x < 0:
                self.velocity += self.acceleration
            else:
                self.velocity.x = 0

        if self.velocity.x > 100:
            self.animation.frame_duration = 25
        elif self.velocity.x > 50:
            self.animation.frame_duration = 50
        elif self.velocity.x > 0:
            self.animation.frame_duration = 100

        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_on_ground:
            self.velocity.y = -self.jump_force
            self.is_on_ground = False
            self.is_jump = True

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.is_grown:
            # TODO when mario is grown, he can now duck
            pass

        self.position.x += self.velocity.x * delta
        self.position.y += self.velocity.y * delta

        if not self.is_on_ground:
            self.velocity.y += constants.GRAVITY * delta

        self.hitbox.topleft = (int(self.position.x), int(self.position.y))

        # print(self.velocity)


class World:
    gravity: float = constants.GRAVITY

    screen_width, screen_height = (1280, 720)
    world_width, world_height = (3360, 220)

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen: pygame.Surface = screen
        self.mario: Mario = Mario()
        self.camera: Camera = Camera()

        self.__objects = []
        self.__surface: pygame.Surface = pygame.surface.Surface(
            (self.world_width, self.world_height)
        )
        self.__map = load_pygame("assets/game.tmx")
        self.__layers = {
            "Ground",
            "Clouds",
            "Bushes",
            "Bottom Castle",
            "Top Castle",
            "Flag",
        }

        self.__surface.fill(constants.BACKGROUND_COLOR)

    def draw(self) -> None:
        self.__surface.fill(constants.BACKGROUND_COLOR)
        for layer in self.__map.layers:
            if layer.name in self.__layers:
                for x, y, gid in layer:
                    tile = self.__map.get_tile_image_by_gid(gid)
                    if tile:
                        self.__surface.blit(
                            tile, (x * constants.TILE_WIDTH, y * constants.TILE_HEIGHT)
                        )

        self.mario.draw(self.__surface)

        self.debug(True)

        # print("Camera: ", self.camera.position)

    def debug(self, is_debug) -> None:
        if is_debug:
            for tile_objects in self.__map.visible_layers:
                if tile_objects.name == "Collision":
                    for obj in tile_objects:
                        collider = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        pygame.draw.rect(self.__surface, constants.RED, collider, 1)

                        if collider.colliderect(self.mario.hitbox):
                            self.mario.hitbox.bottom = collider.top
                            self.mario.is_on_ground = True
                            self.mario.is_jumping = False
                            self.mario.velocity.y = 0
            # for isinstance(entities, pygame.sprite.Sprite):

    def update(self, delta) -> None:
        pygame.draw.rect(self.__surface, (255, 0, 0), self.camera.viewport, 1)
        self.mario.update(delta)
        self.__surface = self.camera.zoom(self.__surface)
        self.camera.follow_target(self.mario)

    def get_world_surface(self) -> pygame.Surface:
        return self.__surface


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(
            (constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.RESIZABLE
        )

        self.clock = pygame.time.Clock()
        self.delta: float = self.clock.tick(constants.FPS) / 1000
        self.world: World = World(self.screen)

        self.__running: bool = True

        pygame.init()
        pygame.display.set_caption("Super Mario Bros.")
        self.screen.fill(constants.BACKGROUND_COLOR)
        self.update()
        pygame.quit()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

    def update(self) -> None:
        while self.__running:
            delta = self.clock.tick(constants.FPS) / 1000
            self.screen.fill(constants.BACKGROUND_COLOR)
            self.handle_events()
            self.world.draw()
            self.world.update(delta)
            self.draw()

    def draw(self) -> None:
        # TODO: (0, 0) IDK what this does but it involves the camera
        self.screen.blit(self.world.get_world_surface(), (0, 0))
        pygame.display.flip()
        pygame.display.update()


if __name__ == "__main__":
    Game()
