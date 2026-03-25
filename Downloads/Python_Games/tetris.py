import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colors
BLACK = (0, 0, 0)
COLORS = [
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0)
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

# Grid
grid = [[0 for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = WIDTH // BLOCK_SIZE // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x],
                                 (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def valid_move(piece, dx, dy):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + dx
                new_y = piece.y + y + dy
                if new_x < 0 or new_x >= WIDTH//BLOCK_SIZE or new_y >= HEIGHT//BLOCK_SIZE:
                    return False
                if new_y >= 0 and grid[new_y][new_x]:
                    return False
    return True

def place_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[piece.y + y][piece.x + x] = piece.color

def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < HEIGHT // BLOCK_SIZE:
        grid.insert(0, [0 for _ in range(WIDTH // BLOCK_SIZE)])

clock = pygame.time.Clock()
piece = Piece()
running = True

fall_time = 0

while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    if fall_time > 500:
        if valid_move(piece, 0, 1):
            piece.y += 1
        else:
            place_piece(piece)
            clear_lines()
            piece = Piece()
        fall_time = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_move(piece, -1, 0):
                piece.x -= 1
            if event.key == pygame.K_RIGHT and valid_move(piece, 1, 0):
                piece.x += 1
            if event.key == pygame.K_DOWN and valid_move(piece, 0, 1):
                piece.y += 1
            if event.key == pygame.K_UP:
                piece.rotate()

    # Draw piece
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, piece.color,
                                 ((piece.x+x)*BLOCK_SIZE, (piece.y+y)*BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE))

    draw_grid()
    pygame.display.update()

pygame.quit()