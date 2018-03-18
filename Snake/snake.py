import pygame as pg
import sys
import random

pg.init()
screen = pg.display.set_mode((640, 640))
screen.fill((0,0,0))
pg.display.set_caption('Classic Snake')
clock = pg.time.Clock()
start_play = 'f'
killed = 'f'
scoreboard = 0


def random_generator():
    m = random.randrange(0, 640)
    while m % 15 != 0 and m!=0 and m!=639:
        m = random.randrange(0, 640)
    return m


def main_intro():
    pg.init()
    global start_play
    text = pg.font.Font('freesansbold.ttf', 28)
    img = '/home/dsp/PycharmProjects/Snake/assets/Mainscreen.png'
    image_load = pg.image.load(img)
    screen.blit(image_load,(200,125))
    start = pg.Rect((260,250),(100,36))
    pg.draw.rect(screen,(255,255,255),start)
    text_surface = text.render('Play',True,(0, 0, 0))
    play = text_surface.get_rect()
    play.center = (310,268)
    screen.blit(text_surface, play)
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN or event.type == pg.KEYDOWN:
            pos = pg.mouse.get_pos()
            if start.collidepoint(pos) or play.collidepoint(pos) or pg.K_ENTER:
                start_play = 't'

    pg.display.update()


def game():
    position = []
    global scoreboard
    previous_key = pg.K_0
    bodyx, bodyy = random_generator(), random_generator()
    food = pg.Rect((200, 140), (15, 15))
    food_counter, x = 0, 0
    vx, vy = 0, 0
    running = True
    while running:
        i = food_counter
        j = 0
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP and previous_key != pg.K_DOWN:
                    vx, vy = 0, -16
                    previous_key = pg.K_UP
                elif event.key == pg.K_DOWN and previous_key != pg.K_UP:
                    vx, vy = 0, 16
                    previous_key = pg.K_DOWN
                elif event.key == pg.K_RIGHT and previous_key != pg.K_LEFT:
                    vx, vy = 16, 0
                    previous_key = pg.K_RIGHT
                elif event.key == pg.K_LEFT and previous_key != pg.K_RIGHT:
                    vx, vy = -16, 0

                    previous_key = pg.K_LEFT

        bodyx = (bodyx+vx)
        bodyy = (bodyy+vy)

        if food_counter > x:
            x = food_counter
            position.insert(x, (position[x-1][0]+vx, position[x-1][1]+vy))
        else:
            if len(position) == 0:
                position.insert(0, (bodyx, bodyy))

        p = food_counter
        while p > 0:
            position[p] = position[p - 1]
            p -= 1

        del position[0]
        position.insert(0, (bodyx, bodyy))

        while i >= 0:
            pg.draw.rect(screen,(255,255,255),pg.Rect(position[j],(15,15)))
            j += 1
            i -= 1

        # This sees that food is within window
        u,v = random_generator(),random_generator()
        while u > 624 or u < 1:
            u = random_generator()

        while v > 624 or v < 1:
            v = random_generator()

        # Checks the collision
        if (pg.Rect(position[0], (15, 15))).colliderect(food):
            food = pg.Rect((u, v), (15, 15))
            food_counter += 1
            scoreboard += 10

        if bodyx >= 625 or bodyy >= 625 or bodyx <= 0 or bodyy <= 0:
            running = False

        a=1
        while a < len(position):
            if position[0] == position[a]:
                running = False
            a += 1

        clock.tick(15)
        pg.draw.rect(screen, (255, 0, 0), food)
        pg.display.update()
        screen.fill((0, 0, 0))


def game_over():
    pg.init()
    global start_play, killed, scoreboard
    over = pg.Rect((180, 200), (300, 300))
    pg.draw.rect(screen,(255, 255, 255), over)
    text = pg.font.Font('freesansbold.ttf', 28)

    # For Game Over
    game_over_text = text.render('Game Over', True, (0,0,0))
    end = game_over_text.get_rect()
    end.center = (330,250)
    screen.blit(game_over_text, end)

    # For Retry
    retry_text = text.render('Retry', True, (0, 0, 0))
    retry = retry_text.get_rect()
    retry.center = (225, 446)
    screen.blit(retry_text, retry)

    # For Cancel
    cancel_text = text.render('Cancel', True, (0, 0, 0))
    cancel = cancel_text.get_rect()
    cancel.center = (420, 438)
    screen.blit(cancel_text, cancel)

    # For Score
    score_text = text.render('Score : %d' %scoreboard, True, (255, 0, 0))
    score = score_text.get_rect()
    score.center = (316, 307)
    screen.blit(score_text, score)

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            scoreboard = 0
            if retry.collidepoint(pos):
                start_play = 't'
                killed = 'f'
            elif cancel.collidepoint(pos):
                start_play = 'f'
                killed = 'f'

    pg.display.update()


while True:
    pg.init()
    for main_event in pg.event.get():
        if main_event.type == pg.QUIT or (main_event.type == pg.KEYDOWN and main_event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit

    if start_play == 'f' and killed == 'f':
        main_intro()
    if start_play == 't':
        game()
        start_play = 'f'
        killed = 't'

    if killed == 't':
        game_over()

    screen.fill((0, 0, 0))

