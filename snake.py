import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game, font=("Arial", 14))
        self.start_button.pack()

        self.reset_button = tk.Button(root, text="Reset Game", command=self.reset_game, font=("Arial", 14))
        self.reset_button.pack()

        self.snake = []
        self.snake_direction = "Up"
        self.food = None
        self.running = False

        self.root.bind("<Up>", lambda _: self.change_direction("Up"))
        self.root.bind("<Down>", lambda _: self.change_direction("Down"))
        self.root.bind("<Left>", lambda _: self.change_direction("Left"))
        self.root.bind("<Right>", lambda _: self.change_direction("Right"))

    def start_game(self):
        self.reset_game()
        self.snake = [(200, 200), (200, 210), (200, 220)]
        self.snake_direction = "Up"
        self.running = True
        self.spawn_food()
        self.update_game()

    def reset_game(self):
        self.running = False
        self.canvas.delete("all")
        self.snake = []
        self.food = None
        self.canvas.create_text(200, 200, fill="white", font=("Arial", 24), text="Press Start to Play")

    def draw_snake(self):
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green", tags="snake")

    def spawn_food(self):
        if self.food is not None:
            self.canvas.delete("food")

        while True:
            food_x = random.randint(0, 39) * 10
            food_y = random.randint(0, 39) * 10
            if (food_x, food_y) not in self.snake:
                break

        self.food = (food_x, food_y)
        self.canvas.create_oval(food_x, food_y, food_x + 10, food_y + 10, fill="red", tags="food")

    def change_direction(self, direction):
        if not self.running:
            return

        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if direction != opposites.get(self.snake_direction):
            self.snake_direction = direction

    def update_game(self):
        if not self.running:
            return

        head_x, head_y = self.snake[0]

        if self.snake_direction == "Up":
            head_y -= 10
        elif self.snake_direction == "Down":
            head_y += 10
        elif self.snake_direction == "Left":
            head_x -= 10
        elif self.snake_direction == "Right":
            head_x += 10

        new_head = (head_x, head_y)

        if (new_head in self.snake or
            head_x < 0 or head_y < 0 or head_x >= 400 or head_y >= 400):
            self.running = False
            self.canvas.create_text(200, 200, fill="white", font=("Arial", 24), text="Game Over")
            return

        self.snake = [new_head] + self.snake

        if new_head == self.food:
            self.spawn_food()
        else:
            self.snake.pop()

        self.draw_snake()
        self.root.after(100, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
