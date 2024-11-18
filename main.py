import pygame
from pytmx.util_pygame import load_pygame

TILESET_WIDTH = 16
TILESET_HEIGHT = 16


class Game:
    running: bool = True
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    tiled_map = load_pygame("assets/game.tmx")

    camera_pos = [0, 0]

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Super Mario Bros.")
        self.update()
        pygame.quit()

    def update(self) -> None:
        world = pygame.surface.Surface((3360, 220))
        while self.running:
            self.screen.fill("#000000")
            world.fill("#5d94fb")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.camera_pos[0] += 10
            if keys[pygame.K_RIGHT]:
                self.camera_pos[0] -= 10
            if keys[pygame.K_UP]:
                self.camera_pos[1] += 10
            if keys[pygame.K_DOWN]:
                self.camera_pos[1] -= 10

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

            zoomed_camera = pygame.transform.rotozoom(world, 0, 3.3)

            self.screen.blit(zoomed_camera, self.camera_pos)

            pygame.display.flip()

            pygame.display.update()
            self.clock.tick(60)

    def draw(self) -> None:
        pass


Game()
