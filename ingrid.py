import sys
import pygame
import math
import random

class Player:
    def __init__(self, surface: pygame.Surface, grid_x: int, grid_y: int) -> None:
        self.surface = surface
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.direction = (0, 0)  
        self.last_direction = self.direction
        self.segments = [(self.grid_x, self.grid_y)]
        self.max_segments = 3

    def move(self) -> None:
        dx, dy = self.direction
        new_x = max(0, min(COLS - 1, self.grid_x + dx))
        new_y = max(0, min(ROWS - 1, self.grid_y + dy))

        if (new_x, new_y) != (self.grid_x, self.grid_y):
            self.grid_x, self.grid_y = new_x, new_y
            self.segments.insert(0, (self.grid_x, self.grid_y))
            if len(self.segments) > self.max_segments:
                self.segments.pop()

    def grow(self, amount: int = 1) -> None:
        self.max_segments += amount

    def keyboard_control(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_UP:
                dx, dy = 0, -1
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, 1
            elif event.key == pygame.K_LEFT:
                dx, dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = 1, 0

            if (dx, dy) != (-self.last_direction[0], -self.last_direction[1]):
                self.direction = (dx, dy)
                self.last_direction = (dx, dy)

    def display(self) -> None:
        for x, y in self.segments:
            screen_x = x * TILE_WIDTH + TILE_WIDTH // 2
            screen_y = y * TILE_HEIGHT + TILE_HEIGHT // 2
            pygame.draw.circle(self.surface, (0, 0, 255), (screen_x, screen_y), TILE_WIDTH // 2)

    def get_head_pos(self):
        head_x = self.grid_x * TILE_WIDTH + TILE_WIDTH // 2
        head_y = self.grid_y * TILE_HEIGHT + TILE_HEIGHT // 2
        return head_x, head_y


class SeaUrchin:
    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.pos = self.generate_new_position()

    def generate_new_position(self):
        grid_x = random.randint(0, COLS - 1)
        grid_y = random.randint(0, ROWS - 1)
        return (grid_x * TILE_WIDTH + TILE_WIDTH // 2,
                grid_y * TILE_HEIGHT + TILE_HEIGHT // 2)

    def display(self):
        pygame.draw.circle(self.surface, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 10)

    def check_collision(self, head_x, head_y) -> bool:
        dist = math.hypot(head_x - self.pos[0], head_y - self.pos[1])
        return dist < TILE_WIDTH // 2


WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS

def draw_bg(surface: pygame.Surface):
    for row in range(ROWS):
        for col in range(COLS):
            color = (65, 160, 200) if (row + col) % 2 == 0 else (67, 130, 225)
            pygame.draw.rect(
                surface,
                color,
                (col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            )

def main():
    pygame.init()
    fps = 6  
    fps_clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    p = Player(screen, COLS // 2, ROWS // 2)
    food = SeaUrchin(screen)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                p.keyboard_control(event)

        draw_bg(screen)
        p.move()
        head_x, head_y = p.get_head_pos()

        if food.check_collision(head_x, head_y):
            p.grow()
            food.pos = food.generate_new_position()

        p.display()
        food.display()

        pygame.display.flip()
        fps_clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()