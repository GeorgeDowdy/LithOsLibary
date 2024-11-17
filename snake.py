import tkinter as tk
import random

# Create the main window
root = tk.Tk()
root.title("Snake Game")

# Game configuration
window_width = 600
window_height = 400
cell_size = 20  # Size of each cell in the grid
snake_color = "green"
food_color = "red"
bg_color = "black"

# Create a canvas to display the game
canvas = tk.Canvas(root, width=window_width, height=window_height, bg=bg_color)
canvas.pack()

# Initial snake position and direction
snake = [(100, 100), (80, 100), (60, 100)]  # List of (x, y) tuples representing the snake's body
snake_direction = "Right"  # Initial direction
food_position = (200, 200)  # Starting position of the food

# Function to create a square at a given (x, y) position
def create_square(position, color):
    x, y = position
    return canvas.create_rectangle(x, y, x + cell_size, y + cell_size, fill=color, outline=color)

# Draw the snake and food
snake_squares = [create_square(part, snake_color) for part in snake]
food_square = create_square(food_position, food_color)

# Function to place food randomly on the canvas
def place_food():
    global food_position, food_square
    canvas.delete(food_square)
    x = random.randint(0, (window_width // cell_size) - 1) * cell_size
    y = random.randint(0, (window_height // cell_size) - 1) * cell_size
    food_position = (x, y)
    food_square = create_square(food_position, food_color)

# Function to change the snake's direction
def change_direction(new_direction):
    global snake_direction
    if (new_direction == "Left" and snake_direction != "Right") or \
       (new_direction == "Right" and snake_direction != "Left") or \
       (new_direction == "Up" and snake_direction != "Down") or \
       (new_direction == "Down" and snake_direction != "Up"):
        snake_direction = new_direction

# Function to move the snake
def move_snake():
    global snake, snake_squares

    # Calculate new head position based on direction
    head_x, head_y = snake[0]
    if snake_direction == "Right":
        new_head = (head_x + cell_size, head_y)
    elif snake_direction == "Left":
        new_head = (head_x - cell_size, head_y)
    elif snake_direction == "Up":
        new_head = (head_x, head_y - cell_size)
    elif snake_direction == "Down":
        new_head = (head_x, head_y + cell_size)

    # Check if the snake hits the walls
    if new_head[0] < 0 or new_head[0] >= window_width or new_head[1] < 0 or new_head[1] >= window_height:
        game_over()
        return

    # Check if the snake hits itself
    if new_head in snake:
        game_over()
        return

    # Add the new head to the snake's body
    snake = [new_head] + snake

    # Check if the snake has eaten food
    if new_head == food_position:
        place_food()  # Generate new food
    else:
        # Remove the tail if no food is eaten
        tail = snake.pop()
        canvas.delete(snake_squares[-1])
        del snake_squares[-1]

    # Add the new head's square to the canvas
    snake_squares = [create_square(new_head, snake_color)] + snake_squares

    # Keep the snake moving
    root.after(100, move_snake)

# Function to handle game over
def game_over():
    canvas.create_text(window_width // 2, window_height // 2, text="Game Over", fill="white", font=("Arial", 30))
    root.after_cancel(move_snake)

# Bind the arrow keys to control the snake
root.bind("<Left>", lambda event: change_direction("Left"))
root.bind("<Right>", lambda event: change_direction("Right"))
root.bind("<Up>", lambda event: change_direction("Up"))
root.bind("<Down>", lambda event: change_direction("Down"))

# Start the game
place_food()
move_snake()

# Start the Tkinter event loop
root.mainloop()
