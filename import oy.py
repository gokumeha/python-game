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
purple = (128, 0, 128)
gray = (128, 128, 128)
 
dis_width = 800  # Increased width for better UI
dis_height = 500  # Increased height for better UI
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Enhanced Two Player Snake Game')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 20)
input_font = pygame.font.SysFont("arial", 30)
title_font = pygame.font.SysFont("bahnschrift", 40)

# Game constants
GAME_TIME_LIMIT = 120  # 2 minutes in seconds
RESPAWN_DELAY = 3  # 3 seconds before respawn

def get_player_names():
    """Get names for both players"""
    player1_name = ""
    player2_name = ""
    getting_name1 = True
    getting_name2 = False
    
    while getting_name1 or getting_name2:
        dis.fill(blue)
        
        # Title
        title_text = title_font.render("Enter Player Names", True, white)
        dis.blit(title_text, [dis_width//2 - title_text.get_width()//2, 50])
        
        if getting_name1:
            # Player 1 name input
            prompt1 = input_font.render("Player 1 (WASD controls): " + player1_name + "_", True, yellow)
            dis.blit(prompt1, [50, 150])
            
            instruction1 = font_style.render("Press ENTER when done", True, white)
            dis.blit(instruction1, [50, 190])
        else:
            # Show completed Player 1 name
            completed1 = input_font.render("Player 1: " + player1_name, True, yellow)
            dis.blit(completed1, [50, 150])
        
        if getting_name2:
            # Player 2 name input
            prompt2 = input_font.render("Player 2 (IJKL controls): " + player2_name + "_", True, purple)
            dis.blit(prompt2, [50, 250])
            
            instruction2 = font_style.render("Press ENTER when done", True, white)
            dis.blit(instruction2, [50, 290])
        elif not getting_name1:
            # Show completed Player 2 name
            completed2 = input_font.render("Player 2: " + player2_name, True, purple)
            dis.blit(completed2, [50, 250])
        
        if not getting_name1 and not getting_name2:
            start_text = font_style.render("Press SPACE to start the game!", True, green)
            dis.blit(start_text, [dis_width//2 - start_text.get_width()//2, 350])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if getting_name1:
                    if event.key == pygame.K_RETURN and player1_name.strip():
                        getting_name1 = False
                        getting_name2 = True
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    elif event.unicode.isprintable() and len(player1_name) < 15:
                        player1_name += event.unicode
                
                elif getting_name2:
                    if event.key == pygame.K_RETURN and player2_name.strip():
                        getting_name2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    elif event.unicode.isprintable() and len(player2_name) < 15:
                        player2_name += event.unicode
                
                elif event.key == pygame.K_SPACE:
                    return player1_name.strip() or "Player 1", player2_name.strip() or "Player 2"
    
    return player1_name.strip() or "Player 1", player2_name.strip() or "Player 2"

def display_game_info(player1_name, player2_name, player1_points, player2_points, time_left):
    """Display scores, names, and time remaining"""
    # Player 1 info (left side)
    name1_text = score_font.render(f"{player1_name}: {player1_points}", True, yellow)
    dis.blit(name1_text, [10, 10])
    
    # Player 2 info (right side)
    name2_text = score_font.render(f"{player2_name}: {player2_points}", True, purple)
    dis.blit(name2_text, [dis_width - name2_text.get_width() - 10, 10])
    
    # Time remaining (center)
    minutes = int(time_left // 60)
    seconds = int(time_left % 60)
    time_text = score_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, white)
    dis.blit(time_text, [dis_width//2 - time_text.get_width()//2, 10])
    
    # Draw separator line
    pygame.draw.line(dis, white, (0, 40), (dis_width, 40), 2)

def display_respawn_countdown(player_name, countdown):
    """Display respawn countdown for dead player"""
    if countdown > 0:
        respawn_text = font_style.render(f"{player_name} respawning in {countdown}...", True, red)
        dis.blit(respawn_text, [dis_width//2 - respawn_text.get_width()//2, dis_height//2 + 50])

def get_spawn_position(player_num):
    """Get a safe spawn position for a player"""
    if player_num == 1:
        return dis_width // 4, dis_height // 2
    else:
        return 3 * dis_width // 4, dis_height // 2

def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def show_final_results(player1_name, player2_name, player1_points, player2_points):
    """Display final game results"""
    dis.fill(blue)
    
    # Title
    title_text = title_font.render("GAME OVER!", True, red)
    dis.blit(title_text, [dis_width//2 - title_text.get_width()//2, 100])
    
    # Final scores
    score1_text = input_font.render(f"{player1_name}: {player1_points} points", True, yellow)
    dis.blit(score1_text, [dis_width//2 - score1_text.get_width()//2, 180])
    
    score2_text = input_font.render(f"{player2_name}: {player2_points} points", True, purple)
    dis.blit(score2_text, [dis_width//2 - score2_text.get_width()//2, 220])
    
    # Winner announcement
    if player1_points > player2_points:
        winner_text = input_font.render(f"{player1_name} Wins!", True, green)
    elif player2_points > player1_points:
        winner_text = input_font.render(f"{player2_name} Wins!", True, green)
    else:
        winner_text = input_font.render("It's a Tie!", True, white)
    
    dis.blit(winner_text, [dis_width//2 - winner_text.get_width()//2, 280])
    
    # Play again prompt
    again_text = font_style.render("Press C to Play Again or Q to Quit", True, white)
    dis.blit(again_text, [dis_width//2 - again_text.get_width()//2, 350])
    
    pygame.display.update()

def gameLoop():
    # Get player names
    player1_name, player2_name = get_player_names()
    
    game_over = False
    game_close = False
    
    # Game timing
    start_time = time.time()
    
    # Player 1 variables
    x1, y1 = get_spawn_position(1)
    x1_change = 0
    y1_change = 0
    snake_List1 = []
    Length_of_snake1 = 1
    player1_alive = True
    player1_respawn_time = 0
    
    # Player 2 variables  
    x2, y2 = get_spawn_position(2)
    x2_change = 0
    y2_change = 0
    snake_List2 = []
    Length_of_snake2 = 1
    player2_alive = True
    player2_respawn_time = 0
    
    # Point system
    player1_points = 0
    player2_points = 0

    # Food position
    foodx = round(random.randrange(50, dis_width - snake_block - 50) / 10.0) * 10.0
    foody = round(random.randrange(50, dis_height - snake_block - 50) / 10.0) * 10.0

    while not game_over:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_left = max(0, GAME_TIME_LIMIT - elapsed_time)
        
        # Check if time is up
        if time_left <= 0:
            game_close = True

        while game_close == True:
            show_final_results(player1_name, player2_name, player1_points, player2_points)
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False

        # Handle respawn timing
        if not player1_alive and player1_respawn_time > 0:
            if current_time >= player1_respawn_time:
                player1_alive = True
                x1, y1 = get_spawn_position(1)
                x1_change = 0
                y1_change = 0
                snake_List1 = []
                Length_of_snake1 = 1
                player1_respawn_time = 0
        
        if not player2_alive and player2_respawn_time > 0:
            if current_time >= player2_respawn_time:
                player2_alive = True
                x2, y2 = get_spawn_position(2)
                x2_change = 0
                y2_change = 0
                snake_List2 = []
                Length_of_snake2 = 1
                player2_respawn_time = 0

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

        # Player movement and boundary checking
        if player1_alive:
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 50:  # Account for UI space
                player1_alive = False
                player1_respawn_time = current_time + RESPAWN_DELAY
                player2_points += 1
            else:
                x1 += x1_change
                y1 += y1_change
        
        if player2_alive:
            if x2 >= dis_width or x2 < 0 or y2 >= dis_height or y2 < 50:  # Account for UI space
                player2_alive = False
                player2_respawn_time = current_time + RESPAWN_DELAY
                player1_points += 1
            else:
                x2 += x2_change
                y2 += y2_change
        
        dis.fill(blue)
        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])
        
        # Update snake lists
        if player1_alive:
            snake_Head1 = [x1, y1]
            snake_List1.append(snake_Head1)
            if len(snake_List1) > Length_of_snake1:
                del snake_List1[0]

        if player2_alive:
            snake_Head2 = [x2, y2]
            snake_List2.append(snake_Head2)
            if len(snake_List2) > Length_of_snake2:
                del snake_List2[0]

        # Self collision check
        if player1_alive and len(snake_List1) > 1:
            for x in snake_List1[:-1]:
                if x == snake_Head1:
                    player1_alive = False
                    player1_respawn_time = current_time + RESPAWN_DELAY
                    player2_points += 1
                    
        if player2_alive and len(snake_List2) > 1:
            for x in snake_List2[:-1]:
                if x == snake_Head2:
                    player2_alive = False
                    player2_respawn_time = current_time + RESPAWN_DELAY
                    player1_points += 1

        # Player collision check
        if player1_alive and player2_alive:
            if snake_Head1 == snake_Head2:
                # Head-on collision - both die
                player1_alive = False
                player2_alive = False
                player1_respawn_time = current_time + RESPAWN_DELAY
                player2_respawn_time = current_time + RESPAWN_DELAY
            else:
                # Check if player 1 hits player 2's body
                for x in snake_List2[:-1]:
                    if snake_Head1 == x:
                        player1_alive = False
                        player1_respawn_time = current_time + RESPAWN_DELAY
                        player2_points += 1
                        break
                
                # Check if player 2 hits player 1's body
                for x in snake_List1[:-1]:
                    if snake_Head2 == x:
                        player2_alive = False
                        player2_respawn_time = current_time + RESPAWN_DELAY
                        player1_points += 1
                        break

        # Draw snakes
        if player1_alive:
            our_snake(snake_block, snake_List1, black)
        if player2_alive:
            our_snake(snake_block, snake_List2, red)
        
        # Food collision
        if player1_alive and x1 == foodx and y1 == foody:
            foodx = round(random.randrange(50, dis_width - snake_block - 50) / 10.0) * 10.0
            foody = round(random.randrange(50, dis_height - snake_block - 50) / 10.0) * 10.0
            Length_of_snake1 += 2
            
        if player2_alive and x2 == foodx and y2 == foody:
            foodx = round(random.randrange(50, dis_width - snake_block - 50) / 10.0) * 10.0
            foody = round(random.randrange(50, dis_height - snake_block - 50) / 10.0) * 10.0
            Length_of_snake2 += 2

        # Display UI
        display_game_info(player1_name, player2_name, player1_points, player2_points, time_left)
        
        # Display respawn countdowns
        if not player1_alive and player1_respawn_time > 0:
            countdown = max(0, int(player1_respawn_time - current_time))
            if countdown > 0:
                display_respawn_countdown(player1_name, countdown)
        
        if not player2_alive and player2_respawn_time > 0:
            countdown = max(0, int(player2_respawn_time - current_time))
            if countdown > 0:
                display_respawn_countdown(player2_name, countdown)

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()