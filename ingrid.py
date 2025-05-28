import sys
import pygame
import math
import random
import game_state

WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS

class Player:
    def __init__(self, surface: pygame.Surface, grid_x: int, grid_y: int) -> None:
        self.surface = surface
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.direction = (0, 0)
        self.last_direction = (0, 1)
        self.max_segments = 3
        self.segments = [(self.grid_x, self.grid_y - i) for i in range(self.max_segments)]
        self.grid_x, self.grid_y = self.segments[0]

    def move(self) -> None:
        dx, dy = self.direction
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if new_x < 0 or new_x >= COLS or new_y < 0 or new_y >= ROWS:
            game_state.state = "gameover"
            return

        if (new_x, new_y) in self.segments[1:]:
            game_state.state = "gameover"
            return

        self.grid_x, self.grid_y = new_x, new_y
        self.segments.insert(0, (self.grid_x, self.grid_y))
        if len(self.segments) > self.max_segments:
            self.segments.pop()

    def grow(self, amount: int = 1) -> None:
        self.max_segments += amount

    def keyboard_control(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
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
    text_font = pygame.font.SysFont("Arial", 30)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    p = Player(screen, COLS // 2, ROWS // 2)
    food = SeaUrchin(screen)

    game_state.state = "wait"  # Must press SPACE to start
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if game_state.state == "wait":
                    if event.key == pygame.K_SPACE:
                        game_state.state = "gameon"
                elif game_state.state == "gameon":
                    p.keyboard_control(event)

        if game_state.state == "gameon":
            draw_bg(screen)
            if p.direction != (0, 0):
                p.move()
            head_x, head_y = p.get_head_pos()

            if food.check_collision(head_x, head_y):
                p.grow()
                food.pos = food.generate_new_position()

            p.display()
            food.display()

        elif game_state.state == "wait":
            screen.fill((0, 0, 0))
            draw_text("Press SPACE to Start", text_font, (255, 255, 255), WIDTH // 2 - 140, HEIGHT // 2)

        elif game_state.state == "gameover":
            screen.fill((0, 0, 0))
            draw_text("Game Over", text_font, (255, 255, 255), WIDTH // 2 - 70, HEIGHT // 2)

        pygame.display.flip()
        fps_clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()