import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))

color = (255, 255, 255)

#left bar
score1 = 0
bar1X = 20
bar1Y = 250
bar1Y_change = 0
bar1Rect = pygame.Rect(bar1X, bar1Y, 20, 100)
def draw_bar(rect):
    pygame.draw.rect(screen, color, rect)

font = pygame.font.Font('freesansbold.ttf', 32)

#print scoreboard
def scoreboard():
    scoretext = font.render(str(score1) + ' '*19 + str(score2), True, (255, 255, 255))
    screen.blit(scoretext, (300, 20))

#print name of the winner
def print_winner(name):
    winnertext = font.render(name + ' wins!', True, (255, 255, 255))
    screen.blit(winnertext, (300, 80))

#right bar
score2 = 0
bar2X = 760
bar2Y = 250
bar2Y_change = 0
bar2Rect = pygame.Rect(bar2X, bar2Y, 20, 100)

#net
netX = 395
netY = 0
def draw_net():
    for i in range(6):
        netY = 100*(i) + 20
        netRect = pygame.Rect(netX, netY, 10, 60)
        pygame.draw.rect(screen, color, netRect)

#ball
kickoff_direction = 'right' #if a ball goes left or right at the start of a round
goal = False
ball_speed = 5 #speed in X axis
ballX = 395
ballY = 290
ballX_change = ball_speed
ballY_change = 0
ballRect = pygame.Rect(ballX, ballY, 20, 20)
def draw_ball(ball):
    pygame.draw.rect(screen, color, ball)

#freeze ball after someone wins
def ball_freeze():
    ballX = 100
    ballY = -100
    ballX_change = 0
    ballY_change = 0

#attributes to control if the opposite key is pressed when the other is released (so the bar doesn't stop abruptly)
w_down = False
s_down = False
UP_down = False
DOWN_down = False

score_freeze = False
win = False

running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #left bar controls
            if event.key == pygame.K_w:
                bar1Y_change = -ball_speed
                w_down = True
            if event.key == pygame.K_s:
                bar1Y_change = ball_speed
                s_down = True
            #right bar controls
            if event.key == pygame.K_UP:
                bar2Y_change = -ball_speed
                UP_down = True
            if event.key == pygame.K_DOWN:
                bar2Y_change = ball_speed
                DOWN_down = True
        if event.type == pygame.KEYUP:
            #left bar controls (check if the opposite key is pressed while the other is released)
            if event.key == pygame.K_w and s_down == True:
                w_down = False
            elif event.key == pygame.K_w:
                bar1Y_change = 0
                w_down = False
            if event.key == pygame.K_s and w_down == True:
                s_down = False
            elif event.key == pygame.K_s:
                bar1Y_change = 0
                s_down = False
            #right bar controls (check if the opposite key is pressed while the other is released)
            if event.key == pygame.K_UP and DOWN_down == True:
                UP_down = False
            elif event.key == pygame.K_UP:
                bar2Y_change = 0
                UP_down = False
            if event.key == pygame.K_DOWN and UP_down == True:
                DOWN_down = False
            elif event.key == pygame.K_DOWN:
                bar2Y_change = 0
                DOWN_down = False

            
    #draw bar1
    bar1Y += bar1Y_change
    bar1Rect = pygame.Rect(bar1X, bar1Y, 20, 100)
    draw_bar(bar1Rect)
    
    #draw bar2
    bar2Y += bar2Y_change
    bar2Rect = pygame.Rect(bar2X, bar2Y, 20, 100)
    draw_bar(bar2Rect)

    #bars edge detection
    if bar1Y<= 0 or bar1Y >= 500:
        bar1Y = bar1Y - bar1Y_change
        bar1Y_change = 0
    if bar2Y <= 0 or bar2Y >= 500:
        bar2Y = bar2Y - bar2Y_change
        bar2Y_change = 0

    #ball vs bar collision
    if bar1Rect.colliderect(ballRect):
        ballX_change = ball_speed
        bar1_middle = bar1Y + 50
        hit_position = ballY - bar1_middle #hit_position is how far from the middle of the bar the ball hits
        ballY_change = hit_position*0.05
    if bar2Rect.colliderect(ballRect):
        ballX_change = -ball_speed
        bar2_middle = bar2Y + 50
        hit_position = ballY - bar2_middle 
        ballY_change = hit_position*0.05

    #ball vs wall collision
    if ballY <= 0 or ballY >= 580:
        ballY_change = -ballY_change

    #check if goal
    if ballX >= 800 and score_freeze == False:
        score1 += 1
        score_freeze = True
    if ballX <= 0 and score_freeze == False:
        score2 += 1
        score_freeze = True


    #a little time delay after goal :)
    if ballX >= 1500 or ballX <= -700:
        goal = True
        score_freeze = False

    #reset for a new round
    if goal:
        ballY = random.randint(0, 580)
        ballX = 395
        ballY_change = random.randint(-2, 2)
        goal = False
        if kickoff_direction is 'left':
            ballX_change = ball_speed - 2
            kickoff_direction = 'right'
        else:
            ballX_change = -(ball_speed - 2)
            kickoff_direction = 'left'
    if not win:
        #draw ball
        ballX += ballX_change
        ballY += ballY_change
        ballRect = pygame.Rect(ballX, ballY, 20, 20)
        draw_ball(ballRect)

    #check if win
    if score1 == 1:
        print_winner('Player 1')
        ball_freeze()
        win = True

    if score2 == 1:
        print_winner('Player 2')
        ball_freeze()
        win = True

    scoreboard()
    draw_net()

    pygame.display.update()