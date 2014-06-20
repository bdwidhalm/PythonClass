# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

BALL_COLOR = "Red"
PADDLE_COLOR = "Blue"
SCORE_COLOR = "Green"
LINE_COLOR = "White"

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0] # pixels per update (1/60 seconds)

paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0.0
paddle2_vel = 0.0
paddle_acc = 2

score1 = 0
score2 = 0

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horz_velocity = random.randrange(2, 4)
    vert_velocity = random.randrange(1, 3)
    if right:
        ball_vel = [horz_velocity, -vert_velocity] # pixels per update (1/60 seconds)
    else:
        ball_vel = [-horz_velocity, -vert_velocity] # pixels per update (1/60 seconds)

def increase_velocity():
    global ball_vel
    ball_vel[0] += ball_vel[0] * 0.1
    ball_vel[1] += ball_vel[1] * 0.1

# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    ball_init(True);

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos > HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos += paddle1_vel
    elif (paddle1_pos + HALF_PAD_HEIGHT) < HEIGHT and paddle1_vel > 0:
        paddle1_pos += paddle1_vel
    
    if paddle2_pos > HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos += paddle2_vel
    elif (paddle2_pos + HALF_PAD_HEIGHT) < HEIGHT and paddle2_vel > 0:
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, LINE_COLOR)
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, LINE_COLOR)
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, LINE_COLOR)
    
    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]], 1, PADDLE_COLOR, PADDLE_COLOR)
    canvas.draw_polygon([[(WIDTH - 1) - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [(WIDTH - 1) - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [(WIDTH - 1), paddle2_pos + HALF_PAD_HEIGHT], [(WIDTH - 1), paddle2_pos - HALF_PAD_HEIGHT]], 1, PADDLE_COLOR, PADDLE_COLOR)
     
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if abs(ball_pos[1] - paddle1_pos) <= HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            increase_velocity()
        else:
            score2 += 1
            ball_init(True)
    # right gutter
    if ball_pos[0] >= (WIDTH - 1) - BALL_RADIUS - PAD_WIDTH:
        if abs(ball_pos[1] - paddle2_pos) <= HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0]
            increase_velocity()
        else:
            score1 += 1
            ball_init(False)
    # collide and reflect off top side
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # collide and reflect off bottom side
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
            
    # draw ball and scores
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, BALL_COLOR, BALL_COLOR)
    canvas.draw_text(str(score1), [(WIDTH / 2) - 75, 50], 48, SCORE_COLOR)
    canvas.draw_text(str(score2), [(WIDTH / 2) + 50, 50], 48, SCORE_COLOR)
    

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= paddle_acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += paddle_acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += paddle_acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= paddle_acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel += paddle_acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel -= paddle_acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel -= paddle_acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel += paddle_acc

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game)


# start frame
frame.start()
new_game()
