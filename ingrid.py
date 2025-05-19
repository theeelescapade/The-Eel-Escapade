import sys
import pygame
import math


WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS

class Player:
    def __init__(self, surface: pygame.Surface, x: float, y: float) -> None:
        self.surface = surface
        self.grid_x = int(x // TILE_WIDTH)
        self.grid_y = int(y // TILE_HEIGHT)
        self.max_segments = 5
        self.segments = [(self.grid_x * TILE_WIDTH, self.grid_y * TILE_HEIGHT) for _ in range(self.max_segments)]
        self.dx = 0
        self.dy = 0
        self.move_timer = 0
        self.move_delay = 4  

    def update(self) -> None:
        self.move_timer += 1
        if self.move_timer >= self.move_delay:
            self.move_timer = 0
            self.move(self.dx, self.dy)

    def move(self, dx: int, dy: int) -> None:
        if dx == 0 and dy == 0:
            return
        new_x = max(0, min(COLS - 1, self.grid_x + dx))
        new_y = max(0, min(ROWS - 1, self.grid_y + dy))
        if (new_x, new_y) != (self.grid_x, self.grid_y):
            self.grid_x = new_x
            self.grid_y = new_y
            new_head = (self.grid_x * TILE_WIDTH, self.grid_y * TILE_HEIGHT)
            self.segments = [new_head] + self.segments[:-1]

    def handle_keyboard(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.dx, self.dy = 0, -1
            elif event.key == pygame.K_DOWN:
                self.dx, self.dy = 0, 1
            elif event.key == pygame.K_LEFT:
                self.dx, self.dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                self.dx, self.dy = 1, 0
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.dx, self.dy = 0, 0

    def display(self) -> None:
        for sx, sy in self.segments:
            center_x = sx + TILE_WIDTH // 2
            center_y = sy + TILE_HEIGHT // 2
            pygame.draw.circle(self.surface, (0, 0, 255), (center_x, center_y), 16)

def draw_bg(surface: pygame.Surface):
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = (65, 160, 200)
            else:
                color = (67, 130, 225)

            pygame.draw.rect(
                surface,
                color,
                (col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            )

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    fps_clock = pygame.time.Clock()
    p = Player(screen, WIDTH / 2, HEIGHT / 2)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            p.handle_keyboard(event)

        draw_bg(screen)
        p.update()    
        p.display()

        pygame.display.flip()
        fps_clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()