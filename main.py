import pygame


class Game:
    running: bool = True
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    def init(self) -> None:
        pygame.init()
        pygame.display.set_caption("Super Mario Bros.")

    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill("black")

            # RENDER YOUR GAME HERE

            pygame.display.flip()

            self.clock.tick(60)

    def game_over(self) -> None:
        pygame.quit()


def main() -> None:
    game = Game()
    game.init()
    game.run()


if __name__ == "__main__":
    main()
