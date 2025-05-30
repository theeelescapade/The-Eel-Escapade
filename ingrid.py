import sys
import pygame
import math
import random
import os
import game_state

WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS

f = open("highscore.txt", "r")
high_score = int(f.read())
f.close()

class GameState:
    def __init__(self):
        self.state = "wait"
        self.lives = 3

game_state = GameState()

class Player:
    def __init__(self, surface: pygame.Surface, grid_x: int, grid_y: int) -> None:
        self.surface = surface
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.direction = (0, 0)
        self.last_direction = (0, 1)
        self.max_segments = 3
        self.color: tuple[int, int, int] = (0, 0, 255)
        dx, dy = -self.last_direction[0], -self.last_direction[1]
        self.segments = [(self.grid_x + dx * i, self.grid_y + dy * i) for i in range(self.max_segments)]
        self.grid_x, self.grid_y = self.segments[0]
        self.first_move_done = False
        pygame.display.set_caption("The Eel Escapade")

    def move(self) -> None:
        dx, dy = self.direction
        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        if new_x < 0 or new_x >= COLS or new_y < 0 or new_y >= ROWS:
            game_state.lives -= 1
            if game_state.lives <= 0:
                game_state.state = "gameover"
            else:
                self.direction = (0, 0)
            return

        if (new_x, new_y) in self.segments[1:]:
            game_state.lives -= 1
            if game_state.lives <= 0:
                game_state.state = "gameover"
            else:
                self.direction = (0, 0)
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

                if not self.first_move_done and (dx, dy) == (0, -1):
                    return

                if self.direction == (0, 0) or (dx, dy) != (-self.last_direction[0], -self.last_direction[1]):
                    self.direction = (dx, dy)
                    self.last_direction = (dx, dy)
                    self.first_move_done = True

    def display(self) -> None:
        for x, y in self.segments:
            screen_x = x * TILE_WIDTH
            screen_y = y * TILE_HEIGHT
            pygame.draw.rect(
                self.surface, self.color, (screen_x, screen_y, TILE_WIDTH, TILE_HEIGHT)
            )

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
        return (
            grid_x * TILE_WIDTH + TILE_WIDTH // 2,
            grid_y * TILE_HEIGHT + TILE_HEIGHT // 2,
        )

    def display(self):
        pygame.draw.circle(
            self.surface, (255, 0, 0), (int(self.pos[0]), int(self.pos[1])), 10
        )

    def check_collision(self, head_x, head_y) -> bool:
        dist = math.hypot(head_x - self.pos[0], head_y - self.pos[1])
        return dist < TILE_WIDTH // 2

def draw_bg(surface: pygame.Surface):
    for row in range(ROWS):
        for col in range(COLS):
            color = (113, 212, 217) if (row + col) % 2 == 0 else (67, 197, 204)
            pygame.draw.rect(
                surface,
                color,
                (col * TILE_WIDTH, row * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT),
            )

def main():
    global high_score
    pygame.init()
    fps = 6
    fps_clock = pygame.time.Clock()
    text_font = pygame.font.SysFont("Arial", 30)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_lives(lives, font, x, y, spacing=30, heart_color=(255, 0, 0)):
        for i in range(lives):
            heart = font.render("♥", True, heart_color)
            screen.blit(heart, (x + i * spacing, y))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def new_game():
        return Player(screen, COLS // 2, ROWS // 2), SeaUrchin(screen)

    p, food = new_game()
    game_state.state = "wait"
    game_state.lives = 3
    score = 0
    level = 1

    run = True
    cute_font = pygame.font.Font("Howdy Koala.ttf", 32)
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
                elif game_state.state == "gameover":
                    if event.key == pygame.K_r:
                        p, food = new_game()
                        game_state.state = "wait"
                        game_state.lives = 3
                        score = 0
                        p.max_segments = 3

        if game_state.state == "gameon":
            draw_bg(screen)
            if p.direction != (0, 0):
                prev_pos = p.grid_x, p.grid_y
                prev_segments = p.segments[:]
                prev_max_segments = p.max_segments
                p.move()
                if game_state.state == "gameon":  
                    head_x, head_y = p.get_head_pos()
                    if food.check_collision(head_x, head_y):
                        p.grow()
                        food.pos = food.generate_new_position()
                        p.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    score = len(p.segments) - 3
                    level = score // 10 + 1
                else:
                    
                    p.grid_x, p.grid_y = prev_pos
                    p.segments = prev_segments
                    p.max_segments = prev_max_segments

            p.display()
            food.display()
            if score > high_score:
                high_score = score
            draw_text(f"Score: {score}", text_font, (255, 255, 255), 10, 10)
            draw_text(f"Level: {level}", text_font, (255, 255, 255), 140, 10)
            draw_text(f"High Score: {high_score}", text_font, (255, 255, 255), 250, 10)
            draw_text("Lives:", text_font, (255, 255, 255), 10, 480)
            draw_lives(game_state.lives, text_font, 100, 480)
            fps = 6 + (level - 1)

        elif game_state.state == "wait":
            screen.fill((142, 212, 245))

            draw_text("Welcome to", cute_font, (232,100,170), WIDTH // 2 - 107, HEIGHT // 2 - 80)
            draw_text("The Eel Escapade!", cute_font, (2,172,191), WIDTH // 2 - 155, HEIGHT // 2 - 30)
            draw_text("Press SPACE to start", cute_font, (232, 100, 170), WIDTH // 2 - 180, HEIGHT // 2 + 20)

        elif game_state.state == "gameover":
            screen.fill((142, 212, 245))
            draw_text("Game Over", cute_font, (242, 34, 124), WIDTH // 2 - 90, HEIGHT // 2 - 70)
            draw_text("Press R to Restart", cute_font, (80, 80, 255), WIDTH // 2 - 160, HEIGHT // 2 - 10)

        pygame.display.flip()
        fps_clock.tick(fps)

    f = open("highscore.txt", "w")
    f.write(str(high_score))
    f.close()

    pygame.quit()

if __name__ == "__main__":
    main()