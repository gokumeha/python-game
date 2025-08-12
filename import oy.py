import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)  # Color for player 2 snake
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Two Player Snake Game by ZeN')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 25)
 
 
def display_scores(score1, score2):
    # Player 1 score (left side)
    score1_text = score_font.render("Player 1: " + str(score1), True, yellow)
    dis.blit(score1_text, [10, 10])
    
    # Player 2 score (right side)
    score2_text = score_font.render("Player 2: " + str(score2), True, purple)
    dis.blit(score2_text, [dis_width - 150, 10])
    
    # Draw a line separator below scores
    pygame.draw.line(dis, white, (0, 40), (dis_width, 40), 2)
 
 
def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 
 
def gameLoop():
    game_over = False
    game_close = False
 
    # Player 1 (WASD controls)
    x1 = dis_width / 4
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_List1 = []
    Length_of_snake1 = 1
    player1_alive = True
    
    # Player 2 (Arrow key controls)
    x2 = 3 * dis_width / 4
    y2 = dis_height / 2
    x2_change = 0
    y2_change = 0
    snake_List2 = []
    Length_of_snake2 = 1
    player2_alive = True
    
    # Point system
    player1_points = 0
    player2_points = 0
 
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
 
    while not game_over:
 
        while game_close == True:
            dis.fill(blue)
            message("Game Over! Press C-Play Again or Q-Quit", red)
            display_scores(player1_points, player2_points)
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
                # Player 1 controls (WASD) - only if alive
                if player1_alive:
                    if event.key == pygame.K_a:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_d:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_w:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s:
                        y1_change = snake_block
                        x1_change = 0
                
                # Player 2 controls (IJKL keys) - only if alive
                if player2_alive:
                    if event.key == pygame.K_j:
                        x2_change = -snake_block
                        y2_change = 0
                    elif event.key == pygame.K_l:
                        x2_change = snake_block
                        y2_change = 0
                    elif event.key == pygame.K_i:
                        y2_change = -snake_block
                        x2_change = 0
                    elif event.key == pygame.K_k:
                        y2_change = snake_block
                        x2_change = 0
 
        # Player 1 boundary and movement - only if alive
        if player1_alive:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                player1_alive = False
                player2_points += 1  # Give point to player 2
            else:
                x1 += x1_change
                y1 += y1_change
        
        # Player 2 boundary and movement - only if alive
        if player2_alive:
            if x2 >= dis_width or x2 < 0 or y2 >= dis_height or y2 < 0:
                player2_alive = False
                player1_points += 1  # Give point to player 1
            else:
                x2 += x2_change
                y2 += y2_change
        
        # Check if both players are dead
        if not player1_alive and not player2_alive:
            game_close = True
        
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        
        # Player 1 snake - only if alive
        if player1_alive:
            snake_Head1 = []
            snake_Head1.append(x1)
            snake_Head1.append(y1)
            snake_List1.append(snake_Head1)
            if len(snake_List1) > Length_of_snake1:
                del snake_List1[0]
 
        # Player 2 snake - only if alive
        if player2_alive:
            snake_Head2 = []
            snake_Head2.append(x2)
            snake_Head2.append(y2)
            snake_List2.append(snake_Head2)
            if len(snake_List2) > Length_of_snake2:
                del snake_List2[0]
 
        # Check collision with self for both players - only if alive
        if player1_alive:
            for x in snake_List1[:-1]:
                if x == snake_Head1:
                    player1_alive = False
                    player2_points += 1  # Give point to player 2
                    
        if player2_alive:
            for x in snake_List2[:-1]:
                if x == snake_Head2:
                    player2_alive = False
                    player1_points += 1  # Give point to player 1
        
        # Check collision between players - only if both are alive
        if player1_alive and player2_alive:
            for x in snake_List1:
                if x == snake_Head2:
                    player2_alive = False
                    player1_points += 1  # Give point to player 1
                    
            for x in snake_List2:
                if x == snake_Head1:
                    player1_alive = False
                    player2_points += 1  # Give point to player 2
 
        # Draw both snakes - only if alive
        if player1_alive:
            our_snake(snake_block, snake_List1, black)
        if player2_alive:
            our_snake(snake_block, snake_List2, purple)
        
        # Display scores (points instead of snake length)
        display_scores(player1_points, player2_points)
 
        pygame.display.update()
 
        # Check food collision for both players - only if alive
        if player1_alive and x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake1 += 2
            
        if player2_alive and x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake2 += 2
 
        clock.tick(snake_speed)
    print("YOU LOSE")
    pygame.quit()
    quit()
 
 
gameLoop()
