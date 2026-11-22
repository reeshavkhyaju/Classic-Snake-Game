
import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
BACKGROUND_COLOR = "green"
SPACE_SIZE = 20
SNAKE_COLOR = "red"
BODY_PARTS = 3
SPEED = 150
direction = "down"
score = 0

root = tk.Tk()
root.title("Snake Game")

score_label = tk.Label(
    root,
    text="Score: {}".format(score),
    font=("consolas", 20)
)
score_label.pack()

canvas = tk.Canvas(
    root,
    bg=BACKGROUND_COLOR,
    height=GAME_HEIGHT,
    width=GAME_WIDTH
)
canvas.pack()


class Food:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.canvas = canvas

        canvas.create_oval(
            x, y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill="orange",
            tag="food"
        )


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = []

        for i in range(BODY_PARTS):
            self.coordinates.append(
                [100 - i * SPACE_SIZE, 100]
            )

        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR
            )
            self.squares.append(square)


def next_turn(snake):
    global food, score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if check_collisions(snake):
        game_over()
        return

    if x == food.coordinates[0] and y == food.coordinates[1]:

        canvas.delete("food")

        score += 1
        score_label.config(text="Score: {}".format(score))

        food = Food(canvas)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    root.after(SPEED, next_turn, snake)





def game_over():
    canvas.delete("all")

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=("consolas", 40),
        text="GAME OVER",
        fill="red"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 50,
        font=("consolas", 20),
        text="Your Score: {}".format(score),
        fill="white"
    )

    play_again_button = tk.Button(
        root,
        font=("consolas", 16),
        text="Play Again",
        bg="lightblue",
        command=restart_game
    )

    canvas.create_window(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 100,
        window=play_again_button
    )


def restart_game():
    global score, direction, snake, food

    canvas.delete("all")

    score = 0
    direction = "down"

    score_label.config(text="Score: {}".format(score))

    snake = Snake(canvas)
    food = Food(canvas)

    next_turn(snake)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Wall collision
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Self collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


root.bind("<Left>", lambda event: change_direction("left"))
root.bind("<Right>", lambda event: change_direction("right"))
root.bind("<Up>", lambda event: change_direction("up"))
root.bind("<Down>", lambda event: change_direction("down"))

snake = Snake(canvas)
food = Food(canvas)

next_turn(snake)

root.mainloop()
