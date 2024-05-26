import pygame
import sys 
import random

pygame.init()

SW, SH = 800, 800

BLOCK_SIZE = 40
FONT = pygame.font.Font("font.ttf", BLOCK_SIZE*2)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Snake!")
clock = pygame.time.Clock()

# Load images
snake_head_img = pygame.image.load('assets/snake_head.png')
snake_body_img = pygame.image.load('assets/snake_body.png')
apple_img = pygame.image.load('assets/apple.png')

class Snake:
    def __init__(self):
        self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        global apple
        
        for square in self.body:
            if self.head.colliderect(square):
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):
                self.dead = True
        
        if self.dead:
            self.__init__()
            apple = Apple()
        
        self.body.append(self.head.copy())
        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE
        self.body = self.body[-(len(self.body) - 1):]  # Maintain the length of the snake

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW) / BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH) / BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
    
    def update(self):
        screen.blit(apple_img, (self.x, self.y))

def drawGrid():
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, "#3c3c3b", rect, 1)

snake = Snake()
apple = Apple()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.ydir = 1
                snake.xdir = 0
            elif event.key == pygame.K_UP and snake.ydir == 0:
                snake.ydir = -1
                snake.xdir = 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.ydir = 0
                snake.xdir = -1

    snake.update()
    
    screen.fill('black')
    drawGrid()

    apple.update()

    score = FONT.render(f"{len(snake.body) + 1}", True, "white")
    score_rect = score.get_rect(center=(SW / 2, SH / 20))
    screen.blit(score, score_rect)

    # Draw snake head with image
    screen.blit(snake_head_img, (snake.head.x, snake.head.y))

    # Draw snake body
    for square in snake.body:
        screen.blit(snake_body_img, (square.x, square.y))

    if snake.head.x == apple.x and snake.head.y == apple.y:
        snake.body.append(pygame.Rect(snake.body[-1].x, snake.body[-1].y, BLOCK_SIZE, BLOCK_SIZE))
        apple = Apple()

    pygame.display.update()
    clock.tick(5)
