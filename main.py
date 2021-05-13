#  ------------------ 1 -------------------- Initialize the module
import random
import pygame
import os

pygame.mixer.init()
pygame.init()

#  ------------------ 2 -------------------- Set the window various properties
screenWidth = 900
screenHeight = 600

white = (250, 250, 250)
red = (250, 0, 0)
yellow = (250, 250, 0)
green = (0, 200, 0)
black = (0, 0, 0)

gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Snake Run")

bgimg = pygame.image.load("bg.jpg")
bg = pygame.transform.scale(bgimg, (screenWidth, screenHeight)).convert_alpha()

clock = pygame.time.Clock()

fnt = pygame.font.SysFont(None, 40)


#  ------------------ 3 -------------------- Game specific variables
def textScreen(text, color, x, y):
    screen_text = fnt.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(yellow)
        gameWindow.blit(bg ,(0, 0))
        textScreen("Welcome to Snake Run!", white, screenWidth/2-150, screenHeight/2-50)
        textScreen("Press Space Bar to Play!", white, screenWidth/2-160, screenHeight/2)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit() 
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    gameLoop()

        pygame.display.update()
        clock.tick(30)

#  ------------------ 4 -------------------- Creating game loop
def gameLoop():
    snake_list = []
    snake_length = 1

    if not os.path.isfile('hiScore.txt'):
        hscore = 0
    else:
        with open('hiScore.txt', 'r') as f:
            hscore = int(f.read())

    exit_game = False
    game_over  = False

    snake_x = 450
    snake_y = 300
    snake_size = 25

    velocity_x = 0
    velocity_y = 0
    velocity_init = 5

    food_x = random.randint(50, screenWidth-80)
    food_y = random.randint(50, screenHeight-80)
    food_size = 25

    score = 0
    fps = 30

    while not exit_game:
        if game_over:
            with open('hiScore.txt', 'w') as f:
                f.write(str(hscore))

            gameWindow.fill(yellow)
            textScreen("Game Over!", black, 380, screenHeight/2-150)
            textScreen("Press Enter To Continue!", black, 320, screenHeight/2-100)
            textScreen("Press Escape To Exit!", black, 340, screenHeight/2-50)
            for e in pygame.event.get():
                # print(e)
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        welcome()
                    if e.key == pygame.K_ESCAPE:
                        exit_game = True

        else:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit_game = True

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RIGHT:
                        velocity_x = velocity_init
                        velocity_y = 0

                    if e.key == pygame.K_LEFT:
                        velocity_x = -velocity_init
                        velocity_y = 0

                    if e.key == pygame.K_UP:
                        velocity_y = -velocity_init
                        velocity_x = 0

                    if e.key == pygame.K_DOWN:
                        velocity_y = velocity_init
                        velocity_x = 0

                    if e.key == pygame.K_y:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x-food_x)<20 and abs(snake_y-food_y)<20 :
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()
                score += 10
                if score>hscore:
                    hscore = score
                food_x = random.randint(30, screenWidth-50)
                food_y = random.randint(30, screenHeight-50)
                snake_length += 2

            gameWindow.fill(white)
            textScreen("Score : "+str(score), black, 5, 5)
            textScreen("High Score : "+str(hscore), black, 650, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            
            if len(snake_list)>snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load('dead.mp3')
                pygame.mixer.music.play()

                
            if snake_x<0 or snake_x>screenWidth-20 or snake_y<0 or snake_y>screenHeight-20:
                game_over = True
                pygame.mixer.music.load('dead.mp3')
                pygame.mixer.music.play()

            # pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            plot_snake(gameWindow, black, snake_list, snake_size)
            
        pygame.display.update()
        clock.tick(fps)
        

    #  ------------------ 5 -------------------- Exit
    pygame.quit()
    quit()


#  ------------------ 6 -------------------- Call
welcome()


