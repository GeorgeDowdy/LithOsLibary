import tkinter as tk

# Window settings
WIDTH, HEIGHT = 800, 400

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 20

# Ball settings
BALL_SIZE = 20
BALL_SPEED_X, BALL_SPEED_Y = 3, 3

# Game window
root = tk.Tk()
root.title("Pong with Tkinter")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Left paddle
left_paddle = canvas.create_rectangle(30, HEIGHT//2 - PADDLE_HEIGHT//2, 30 + PADDLE_WIDTH, HEIGHT//2 + PADDLE_HEIGHT//2, fill="white")

# Right paddle
right_paddle = canvas.create_rectangle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, WIDTH - 30, HEIGHT//2 + PADDLE_HEIGHT//2, fill="white")

# Ball
ball = canvas.create_oval(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2, fill="white")

# Ball movement variables
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

# Paddle movement variables
left_paddle_dy, right_paddle_dy = 0, 0

# Functions for paddle movement
def move_left_paddle(event):
    global left_paddle_dy
    if event.keysym == "w":
        left_paddle_dy = -PADDLE_SPEED
    elif event.keysym == "s":
        left_paddle_dy = PADDLE_SPEED

def stop_left_paddle(event):
    global left_paddle_dy
    left_paddle_dy = 0

def move_right_paddle(event):
    global right_paddle_dy
    if event.keysym == "Up":
        right_paddle_dy = -PADDLE_SPEED
    elif event.keysym == "Down":
        right_paddle_dy = PADDLE_SPEED

def stop_right_paddle(event):
    global right_paddle_dy
    right_paddle_dy = 0

# Ball and paddle movement update function
def update():
    global ball_dx, ball_dy

    # Move paddles
    canvas.move(left_paddle, 0, left_paddle_dy)
    canvas.move(right_paddle, 0, right_paddle_dy)

    # Ensure paddles stay within bounds
    if canvas.coords(left_paddle)[1] <= 0:
        canvas.coords(left_paddle, 30, 0, 30 + PADDLE_WIDTH, PADDLE_HEIGHT)
    elif canvas.coords(left_paddle)[3] >= HEIGHT:
        canvas.coords(left_paddle, 30, HEIGHT - PADDLE_HEIGHT, 30 + PADDLE_WIDTH, HEIGHT)

    if canvas.coords(right_paddle)[1] <= 0:
        canvas.coords(right_paddle, WIDTH - 30 - PADDLE_WIDTH, 0, WIDTH - 30, PADDLE_HEIGHT)
    elif canvas.coords(right_paddle)[3] >= HEIGHT:
        canvas.coords(right_paddle, WIDTH - 30 - PADDLE_WIDTH, HEIGHT - PADDLE_HEIGHT, WIDTH - 30, HEIGHT)

    # Move ball
    canvas.move(ball, ball_dx, ball_dy)
    ball_coords = canvas.coords(ball)

    # Ball collision with top and bottom walls
    if ball_coords[1] <= 0 or ball_coords[3] >= HEIGHT:
        ball_dy *= -1

    # Ball collision with paddles
    if (canvas.coords(left_paddle)[2] >= ball_coords[0] and canvas.coords(left_paddle)[1] < ball_coords[3] and canvas.coords(left_paddle)[3] > ball_coords[1]) or \
       (canvas.coords(right_paddle)[0] <= ball_coords[2] and canvas.coords(right_paddle)[1] < ball_coords[3] and canvas.coords(right_paddle)[3] > ball_coords[1]):
        ball_dx *= -1

    # Ball goes out of bounds (reset position)
    if ball_coords[0] <= 0 or ball_coords[2] >= WIDTH:
        canvas.coords(ball, WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, WIDTH//2 + BALL_SIZE//2, HEIGHT//2 + BALL_SIZE//2)
        ball_dx *= -1

    # Schedule the next frame
    root.after(20, update)

# Bind paddle movement to keys
root.bind("<KeyPress-w>", move_left_paddle)
root.bind("<KeyPress-s>", move_left_paddle)
root.bind("<KeyRelease-w>", stop_left_paddle)
root.bind("<KeyRelease-s>", stop_left_paddle)

root.bind("<KeyPress-Up>", move_right_paddle)
root.bind("<KeyPress-Down>", move_right_paddle)
root.bind("<KeyRelease-Up>", stop_right_paddle)
root.bind("<KeyRelease-Down>", stop_right_paddle)

# Start the game loop
update()
root.mainloop()
 