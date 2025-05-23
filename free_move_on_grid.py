import sys
import pygame
import pygame.locals
from pygame.event import Event
import math


class Player:
    def __init__(self, surface: pygame.Surface, x: float, y: float) -> None:
        self.surface = surface
        self.vx = self.vy = self.ax = self.ay = 0.0
        self.max_segments = 30
        self.segment_spacing = 2
        self.segments = [(x - i * self.segment_spacing, y) for i in range(self.max_segments)]
        self.x, self.y = self.segments[0]

    def move(self) -> None:
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95

    
        self.segments[0] = (self.x, self.y)

    
        for i in range(1, len(self.segments)):
            prev_x, prev_y = self.segments[i - 1]
            curr_x, curr_y = self.segments[i]

            dx = prev_x - curr_x
            dy = prev_y - curr_y
            dist = math.hypot(dx, dy)

            if dist == 0:
                continue  
        
            t = self.segment_spacing / dist
            new_x = prev_x - dx * t
            new_y = prev_y - dy * t
            self.segments[i] = (new_x, new_y)

    def handle_keyboard(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.ay = -0.7
            elif event.key == pygame.K_DOWN:
                self.ay = 0.7
            elif event.key == pygame.K_RIGHT:
                self.ax = 0.7
            elif event.key == pygame.K_LEFT:
                self.ax = -0.7
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.ay = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.ax = 0

    def display(self) -> None:
        for sx, sy in self.segments:
            pygame.draw.circle(self.surface, (0, 0, 255), (int(sx), int(sy)), 16)

            

WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS


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
    fps = 60
    fps_clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    p = Player(screen, WIDTH / 2, HEIGHT / 2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                p.handle_keyboard(event)

        draw_bg(screen)
        p.move()
        p.display()

        pygame.display.flip()
        fps_clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
import sys
import pygame
import pygame.locals
from pygame.event import Event
import math


class Player:
    def __init__(self, surface: pygame.Surface, x: float, y: float) -> None:
        self.surface = surface
        self.vx = self.vy = self.ax = self.ay = 0.0
        self.max_segments = 30
        self.segment_spacing = 2
        self.segments = [(x - i * self.segment_spacing, y) for i in range(self.max_segments)]
        self.x, self.y = self.segments[0]

    def move(self) -> None:
        self.vx += self.ax
        self.vy += self.ay
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95
        self.vy *= 0.95

    
        self.segments[0] = (self.x, self.y)

    
        for i in range(1, len(self.segments)):
            prev_x, prev_y = self.segments[i - 1]
            curr_x, curr_y = self.segments[i]

            dx = prev_x - curr_x
            dy = prev_y - curr_y
            dist = math.hypot(dx, dy)

            if dist == 0:
                continue  
        
            t = self.segment_spacing / dist
            new_x = prev_x - dx * t
            new_y = prev_y - dy * t
            self.segments[i] = (new_x, new_y)

    def handle_keyboard(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.ay = -0.7
            elif event.key == pygame.K_DOWN:
                self.ay = 0.7
            elif event.key == pygame.K_RIGHT:
                self.ax = 0.7
            elif event.key == pygame.K_LEFT:
                self.ax = -0.7
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.ay = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.ax = 0

    def display(self) -> None:
        for sx, sy in self.segments:
            pygame.draw.circle(self.surface, (0, 0, 255), (int(sx), int(sy)), 16)

            

WIDTH, HEIGHT = 512, 512
ROWS, COLS = 16, 16
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS


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
    fps = 60
    fps_clock = pygame.time.Clock()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    p = Player(screen, WIDTH / 2, HEIGHT / 2)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            else:
                p.handle_keyboard(event)

        draw_bg(screen)
        p.move()
        p.display()

        pygame.display.flip()
        fps_clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()

