import tkinter as tk
import random

# Game configuration
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DOT_SIZE = 20
PLAYER_SPEED = 10
TIME_LIMIT = 10000  # 10 seconds in milliseconds
COUNTDOWN_INTERVAL = 100  # Update every 100 milliseconds (0.1 second)
WIN_SCORE = 30  # Winning condition: collecting 30 dots

# Create the main window
root = tk.Tk()
root.title("Dot Collector Game with Timer")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black")
canvas.pack()

# Create the player (a blue square)
player = canvas.create_rectangle(50, 50, 50 + DOT_SIZE, 50 + DOT_SIZE, fill="blue")

# Create a dot (a red square)
dot = canvas.create_rectangle(100, 100, 100 + DOT_SIZE, 100 + DOT_SIZE, fill="red")

# Player position and score
player_x, player_y = 50, 50
score = 0
time_left = TIME_LIMIT

# Create labels for score and timer
score_label = tk.Label(root, text=f"Score: {score}", font=("Arial", 16), bg="black", fg="white")
score_label.pack()

timer_label = tk.Label(root, text=f"Time Left: {time_left // 1000}", font=("Arial", 16), bg="black", fg="white")
timer_label.pack()

# Function to move the player
def move_player(dx, dy):
    global player_x, player_y
    player_x += dx
    player_y += dy

    # Boundary control: prevent the player from going off-screen
    player_x = max(0, min(WINDOW_WIDTH - DOT_SIZE, player_x))
    player_y = max(0, min(WINDOW_HEIGHT - DOT_SIZE, player_y))

    # Move the player on the canvas
    canvas.coords(player, player_x, player_y, player_x + DOT_SIZE, player_y + DOT_SIZE)

    # Check for collision with the dot
    if (player_x < canvas.coords(dot)[0] + DOT_SIZE and
        player_x + DOT_SIZE > canvas.coords(dot)[0] and
        player_y < canvas.coords(dot)[1] + DOT_SIZE and
        player_y + DOT_SIZE > canvas.coords(dot)[1]):
        collect_dot()

# Function to move the player using WASD keys
def handle_keypress(event):
    if event.keysym == "w":  # Move up
        move_player(0, -PLAYER_SPEED)
    elif event.keysym == "s":  # Move down
        move_player(0, PLAYER_SPEED)
    elif event.keysym == "a":  # Move left
        move_player(-PLAYER_SPEED, 0)
    elif event.keysym == "d":  # Move right
        move_player(PLAYER_SPEED, 0)

# Function to collect the dot and reset the timer
def collect_dot():
    global score, time_left
    # Move the dot to a new random position
    new_x = random.randint(0, WINDOW_WIDTH - DOT_SIZE)
    new_y = random.randint(0, WINDOW_HEIGHT - DOT_SIZE)
    canvas.coords(dot, new_x, new_y, new_x + DOT_SIZE, new_y + DOT_SIZE)

    # Increase the score
    score += 1
    score_label.config(text=f"Score: {score}")

    # Reset the timer
    time_left = TIME_LIMIT
    timer_label.config(text=f"Time Left: {time_left // 1000}")

    # Check if the player has won
    if score >= WIN_SCORE:
        you_win()

# Function to update the countdown timer
def update_timer():
    global time_left
    time_left -= COUNTDOWN_INTERVAL

    # Update the timer display
    timer_label.config(text=f"Time Left: {time_left // 1000}")

    # Check if time has run out
    if time_left <= 0:
        game_over()
    else:
        # Continue updating the timer every 100 milliseconds (0.1 seconds)
        root.after(COUNTDOWN_INTERVAL, update_timer)

# Function to end the game when the timer runs out
def game_over():
    canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="Game Over", fill="white", font=("Arial", 32))
    root.unbind("<KeyPress>")  # Stop player movement
    show_replay_exit_buttons()

# Function to handle winning condition
def you_win():
    canvas.config(bg="gold")  # Change background color to gold
    canvas.create_text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, text="You Win!", fill="white", font=("Arial", 32))
    root.unbind("<KeyPress>")  # Stop player movement
    show_replay_exit_buttons()

# Function to show Replay and Exit buttons after game ends
def show_replay_exit_buttons():
    replay_button = tk.Button(root, text="Replay", command=replay_game, font=("Arial", 16), width=10)
    replay_button.pack(pady=10)
    
    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 16), width=10)
    exit_button.pack(pady=10)

# Function to reset the game
def replay_game():
    global score, time_left, player_x, player_y
    # Reset score, timer, and player position
    score = 0
    time_left = TIME_LIMIT
    player_x, player_y = 50, 50

    # Reset player and dot position
    canvas.coords(player, player_x, player_y, player_x + DOT_SIZE, player_y + DOT_SIZE)
    collect_dot()

    # Reset the canvas and labels
    canvas.config(bg="black")
    score_label.config(text=f"Score: {score}")
    timer_label.config(text=f"Time Left: {time_left // 1000}")

    # Bind the keys again and start the timer
    root.bind("<KeyPress>", handle_keypress)
    root.after(COUNTDOWN_INTERVAL, update_timer)

    # Remove the buttons
    for widget in root.pack_slaves():
        if isinstance(widget, tk.Button):
            widget.destroy()

# Ensure that keypress binding happens at the start of the game
root.bind("<KeyPress>", handle_keypress)

# Start the timer countdown after initializing everything
root.after(COUNTDOWN_INTERVAL, update_timer)

# Start the game loop
root.mainloop()
