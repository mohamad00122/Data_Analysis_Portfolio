import pygame
import random
import json

pygame.init()

# Game variables
white = (255, 255, 255)
black = (35, 35, 35)
red = (255, 87, 51)
green = (0, 200, 83)
blue = (64, 224, 208)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Grimoire')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont("comicsansms", 35)

def save_high_score(new_high):
    with open('high_score.json', 'w') as file:
        json.dump({"high_score": new_high}, file)

def load_high_score():
    try:
        with open('high_score.json', 'r') as file:
            return json.load(file)["high_score"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def display_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    mesg_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
    dis.blit(mesg, mesg_rect)

def gameLoop():
    game_over = False
    game_close = False
    game_pause = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    score = 0
    high_score = load_high_score()

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            message("High Score: " + str(high_score), green, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_SPACE:
                    game_pause = not game_pause

        while game_pause:
            dis.fill(blue)
            message("Paused. Press Space to resume or Q to quit", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_pause = False
                    elif event.key == pygame.K_q:
                        game_over = True
                        game_pause = False

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                game_close = True

        our_snake(snake_block, snake_List)
        display_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
