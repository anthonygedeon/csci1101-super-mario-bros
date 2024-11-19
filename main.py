import pygame
import constants
from pygame.math import Vector2
from pytmx.util_pygame import load_pygame

TILESET_WIDTH = 16
TILESET_HEIGHT = 16

JUMP_FORCE = 100

GRAVITY = 80


class Camera(pygame.sprite.Group):
    pass


class Mario(pygame.sprite.Sprite):
    speed: int = constants.SPEED
    jump_force: int = constants.JUMP_FORCE

    def __init__(self):
        self.position: Vector2 = Vector2(0, 0)
        self.acceleration: Vector2 = Vector2(0, 0)
        self.velocity: Vector2 = Vector2(1.0, 1.0)


class World:
    pass


class Game:
    running: bool = True
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    tiled_map = load_pygame("assets/game.tmx")
    player = pygame.Rect(16 * 2, 16 * 11, 16, 16)
    camera_pos = Vector2(0.0, 0.0)
    speed_x = 60
    player_x = 0
    player_y = 0
    pos_y = 0
    pos_x = 0

    velocity_y: float = 6

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Super Mario Bros.")
        self.update()
        pygame.quit()

    def update(self) -> None:
        world = pygame.surface.Surface((3360, 220))
        while self.running:
            self.pos_x = 0
            delta = self.clock.tick(constants.FPS) / 1000

            self.pos_y += GRAVITY * delta

            world.fill(constants.BACKGROUND_COLOR)
            self.screen.fill(constants.BACKGROUND_COLOR)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.camera_pos[0] >= 0:
                    self.camera_pos[0] += 0.3
                self.pos_x -= self.speed_x * delta
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.camera_pos[0] -= 0.3
                self.pos_x += self.speed_x * delta
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.pos_y -= JUMP_FORCE * delta
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.pos_y += 20 * delta

            for layer in self.tiled_map.layers:
                if layer.name in [
                    "Ground",
                    "Clouds",
                    "Bushes",
                    "Bottom Castle",
                    "Top Castle",
                    "Flag",
                    "Clouds",
                    "Bushes",
                ]:
                    for x, y, gid in layer:
                        tile = self.tiled_map.get_tile_image_by_gid(gid)
                        if tile:
                            world.blit(tile, (x * TILESET_WIDTH, y * TILESET_HEIGHT))

            for tile_objects in self.tiled_map.visible_layers:
                if tile_objects.name == "Collision":
                    for obj in tile_objects:
                        collider = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        pygame.draw.rect(world, (255, 000, 000), collider, 1)

                        if collider.colliderect(self.player):
                            # print("hello")
                            self.player.y = collider.y - self.player.height
                            self.pos_y = 0

            pygame.draw.rect(world, (255, 0, 0), self.player)
            # pygame.draw.rect(world, (255, 000, 000), (0, 0, 420, 220), 1)

            self.player.move_ip(self.player_x, self.player_y)

            display = world.subsurface(pygame.Rect(0, 0, 420, 220))
            zoomed_camera = pygame.transform.scale(
                display.convert_alpha(),
                (self.screen.get_width(), self.screen.get_height()),
            )

            self.screen.blit(zoomed_camera, self.camera_pos)

            self.player.y += round(self.pos_y)
            self.player.x += round(self.pos_x)

            pygame.display.flip()

            pygame.display.update()

    def draw(self) -> None:
        pass


Game()
