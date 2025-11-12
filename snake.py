import tkinter as tk
from tkinter import font as tkfont
import random
import json
import os
from datetime import datetime
from enum import Enum

class GameMode(Enum):
    CLASSIC = "Classic"
    SPEED = "Speed Mode"
    OBSTACLES = "Obstacles"
    TIME_ATTACK = "Time Attack"
    ZEN = "Zen Mode"

class PowerUpType(Enum):
    SPEED_BOOST = "speed_boost"
    SLOW_DOWN = "slow_down"
    SCORE_MULTIPLIER = "score_multiplier"
    INVINCIBLE = "invincible"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 Snake Game - Ultimate Edition")
        self.root.configure(bg='#0a0e27')

        # Game constants
        self.GRID_SIZE = 20
        self.CELL_SIZE = 25
        self.CANVAS_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.CANVAS_HEIGHT = self.GRID_SIZE * self.CELL_SIZE

        # Color scheme - glassmorphism/liquid glass
        self.COLORS = {
            'bg_dark': '#0a0e27',
            'bg_gradient_1': '#1a1f3a',
            'bg_gradient_2': '#2d3561',
            'glass_bg': '#ffffff',
            'glass_border': '#4facfe',
            'glass_border_2': '#00f2fe',
            'snake_head': '#4facfe',
            'snake_body': '#00f2fe',
            'snake_gradient': ['#4facfe', '#00f2fe', '#43e97b', '#38f9d7'],
            'food': '#ff006e',
            'food_glow': '#ff4d94',
            'obstacle': '#8b5cf6',
            'powerup_speed': '#fbbf24',
            'powerup_slow': '#60a5fa',
            'powerup_score': '#34d399',
            'powerup_invincible': '#f472b6',
            'text_primary': '#ffffff',
            'text_secondary': '#94a3b8',
            'button_gradient_1': '#667eea',
            'button_gradient_2': '#764ba2',
        }

        # Game state
        self.current_screen = "menu"  # menu, game, game_over
        self.game_mode = GameMode.CLASSIC
        self.snake = []
        self.snake_direction = "Right"
        self.next_direction = "Right"
        self.food = None
        self.obstacles = []
        self.powerups = []
        self.active_powerup = None
        self.powerup_timer = 0
        self.running = False
        self.paused = False
        self.score = 0
        self.high_scores = self.load_high_scores()
        self.game_speed = 150
        self.base_speed = 150
        self.time_remaining = 0
        self.start_time = 0
        self.moves_count = 0
        self.food_eaten = 0
        self.score_multiplier = 1

        # Animation state
        self.particle_effects = []
        self.animation_frame = 0

        # Setup UI
        self.setup_fonts()
        self.create_ui()
        self.show_menu()

        # Key bindings
        self.root.bind("<Up>", lambda e: self.queue_direction("Up"))
        self.root.bind("<Down>", lambda e: self.queue_direction("Down"))
        self.root.bind("<Left>", lambda e: self.queue_direction("Left"))
        self.root.bind("<Right>", lambda e: self.queue_direction("Right"))
        self.root.bind("<w>", lambda e: self.queue_direction("Up"))
        self.root.bind("<s>", lambda e: self.queue_direction("Down"))
        self.root.bind("<a>", lambda e: self.queue_direction("Left"))
        self.root.bind("<d>", lambda e: self.queue_direction("Right"))
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Escape>", lambda e: self.show_menu())

    def setup_fonts(self):
        """Setup custom fonts for the game"""
        self.fonts = {
            'title': tkfont.Font(family='Helvetica', size=48, weight='bold'),
            'subtitle': tkfont.Font(family='Helvetica', size=24, weight='bold'),
            'button': tkfont.Font(family='Helvetica', size=16, weight='bold'),
            'score': tkfont.Font(family='Helvetica', size=20, weight='bold'),
            'small': tkfont.Font(family='Helvetica', size=12),
            'tiny': tkfont.Font(family='Helvetica', size=10),
        }

    def create_ui(self):
        """Create the main UI container"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.COLORS['bg_dark'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Canvas for game and menus
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.CANVAS_WIDTH + 300,  # Extra space for sidebar
            height=self.CANVAS_HEIGHT,
            bg=self.COLORS['bg_dark'],
            highlightthickness=0
        )
        self.canvas.pack()

    def create_glass_panel(self, x, y, width, height, alpha=0.15):
        """Create a glassmorphism panel effect"""
        # Background with slight transparency effect
        self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=self.COLORS['bg_gradient_1'],
            outline=self.COLORS['glass_border'],
            width=2,
            tags="glass_panel"
        )
        # Inner glow effect
        self.canvas.create_rectangle(
            x + 2, y + 2, x + width - 2, y + height - 2,
            fill='',
            outline=self.COLORS['glass_border_2'],
            width=1,
            tags="glass_panel"
        )

    def create_gradient_rect(self, x, y, width, height, colors, tags=""):
        """Create a gradient rectangle effect"""
        steps = len(colors) - 1
        for i in range(steps):
            y1 = y + (height * i // steps)
            y2 = y + (height * (i + 1) // steps)
            self.canvas.create_rectangle(
                x, y1, x + width, y2,
                fill=colors[i],
                outline=colors[i],
                tags=tags
            )

    def create_button(self, x, y, width, height, text, command, tags="button"):
        """Create a glassmorphism button"""
        # Button background
        btn_id = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=self.COLORS['bg_gradient_2'],
            outline=self.COLORS['glass_border'],
            width=2,
            tags=tags
        )

        # Button text
        text_id = self.canvas.create_text(
            x + width // 2, y + height // 2,
            text=text,
            fill=self.COLORS['text_primary'],
            font=self.fonts['button'],
            tags=tags
        )

        # Bind click event
        self.canvas.tag_bind(btn_id, '<Button-1>', lambda e: command())
        self.canvas.tag_bind(text_id, '<Button-1>', lambda e: command())

        # Hover effects
        def on_enter(e):
            self.canvas.itemconfig(btn_id, fill=self.COLORS['button_gradient_1'])

        def on_leave(e):
            self.canvas.itemconfig(btn_id, fill=self.COLORS['bg_gradient_2'])

        self.canvas.tag_bind(btn_id, '<Enter>', on_enter)
        self.canvas.tag_bind(btn_id, '<Leave>', on_leave)
        self.canvas.tag_bind(text_id, '<Enter>', on_enter)
        self.canvas.tag_bind(text_id, '<Leave>', on_leave)

        return btn_id, text_id

    def show_menu(self):
        """Display the main menu with glassmorphism design"""
        self.current_screen = "menu"
        self.running = False
        self.paused = False
        self.canvas.delete("all")

        # Background gradient
        for i in range(self.CANVAS_HEIGHT):
            color_ratio = i / self.CANVAS_HEIGHT
            r = int(10 + (29 - 10) * color_ratio)
            g = int(14 + (53 - 14) * color_ratio)
            b = int(39 + (97 - 39) * color_ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(
                0, i, self.CANVAS_WIDTH + 300, i,
                fill=color,
                tags="background"
            )

        # Main glass panel
        panel_width = 400
        panel_height = 500
        panel_x = (self.CANVAS_WIDTH + 300 - panel_width) // 2
        panel_y = 50
        self.create_glass_panel(panel_x, panel_y, panel_width, panel_height)

        # Title with glow effect
        self.canvas.create_text(
            panel_x + panel_width // 2, panel_y + 60,
            text="🐍 SNAKE",
            fill=self.COLORS['glass_border'],
            font=self.fonts['title'],
            tags="menu"
        )
        self.canvas.create_text(
            panel_x + panel_width // 2, panel_y + 100,
            text="ULTIMATE EDITION",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            tags="menu"
        )

        # Game mode selection
        self.canvas.create_text(
            panel_x + panel_width // 2, panel_y + 140,
            text="SELECT GAME MODE",
            fill=self.COLORS['text_primary'],
            font=self.fonts['button'],
            tags="menu"
        )

        # Mode buttons
        modes = [
            (GameMode.CLASSIC, "🎮 Classic", "Traditional snake game"),
            (GameMode.SPEED, "⚡ Speed Mode", "Increases speed over time"),
            (GameMode.OBSTACLES, "🧱 Obstacles", "Avoid random obstacles"),
            (GameMode.TIME_ATTACK, "⏱️ Time Attack", "2 minutes challenge"),
            (GameMode.ZEN, "🌊 Zen Mode", "No walls, relaxing gameplay"),
        ]

        y_offset = panel_y + 180
        for mode, title, desc in modes:
            btn_y = y_offset
            self.create_button(
                panel_x + 50, btn_y, panel_width - 100, 45,
                title,
                lambda m=mode: self.start_game(m),
                tags="menu"
            )
            self.canvas.create_text(
                panel_x + panel_width // 2, btn_y + 60,
                text=desc,
                fill=self.COLORS['text_secondary'],
                font=self.fonts['tiny'],
                tags="menu"
            )
            y_offset += 75

        # High scores button
        self.create_button(
            panel_x + 50, panel_y + 460,
            panel_width - 100, 35,
            "🏆 High Scores",
            self.show_high_scores,
            tags="menu"
        )

        # Controls info
        controls_y = panel_y + panel_height + 20
        self.canvas.create_text(
            panel_x + panel_width // 2, controls_y,
            text="Controls: Arrow Keys or WASD | Space: Pause | ESC: Menu",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['tiny'],
            tags="menu"
        )

    def show_high_scores(self):
        """Display high scores screen"""
        self.canvas.delete("all")

        # Background
        for i in range(self.CANVAS_HEIGHT):
            color_ratio = i / self.CANVAS_HEIGHT
            r = int(10 + (29 - 10) * color_ratio)
            g = int(14 + (53 - 14) * color_ratio)
            b = int(39 + (97 - 39) * color_ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(
                0, i, self.CANVAS_WIDTH + 300, i,
                fill=color,
                tags="scores"
            )

        # Panel
        panel_width = 500
        panel_height = 450
        panel_x = (self.CANVAS_WIDTH + 300 - panel_width) // 2
        panel_y = 30
        self.create_glass_panel(panel_x, panel_y, panel_width, panel_height)

        # Title
        self.canvas.create_text(
            panel_x + panel_width // 2, panel_y + 40,
            text="🏆 HIGH SCORES",
            fill=self.COLORS['glass_border'],
            font=self.fonts['subtitle'],
            tags="scores"
        )

        # Display scores for each mode
        y_offset = panel_y + 80
        for mode in GameMode:
            mode_scores = self.high_scores.get(mode.value, [])

            self.canvas.create_text(
                panel_x + 30, y_offset,
                text=mode.value,
                fill=self.COLORS['text_primary'],
                font=self.fonts['button'],
                anchor="w",
                tags="scores"
            )

            y_offset += 30

            if mode_scores:
                for i, score_data in enumerate(mode_scores[:3], 1):
                    score_text = f"{i}. Score: {score_data['score']} | Food: {score_data['food']}"
                    self.canvas.create_text(
                        panel_x + 50, y_offset,
                        text=score_text,
                        fill=self.COLORS['text_secondary'],
                        font=self.fonts['small'],
                        anchor="w",
                        tags="scores"
                    )
                    y_offset += 25
            else:
                self.canvas.create_text(
                    panel_x + 50, y_offset,
                    text="No scores yet!",
                    fill=self.COLORS['text_secondary'],
                    font=self.fonts['small'],
                    anchor="w",
                    tags="scores"
                )
                y_offset += 25

            y_offset += 15

        # Back button
        self.create_button(
            panel_x + 150, panel_y + panel_height - 50,
            200, 40,
            "⬅️ Back to Menu",
            self.show_menu,
            tags="scores"
        )

    def start_game(self, mode):
        """Start a new game with the selected mode"""
        self.game_mode = mode
        self.current_screen = "game"
        self.running = True
        self.paused = False
        self.score = 0
        self.moves_count = 0
        self.food_eaten = 0
        self.score_multiplier = 1
        self.obstacles = []
        self.powerups = []
        self.active_powerup = None
        self.powerup_timer = 0

        # Initialize snake in the center
        center_x = self.GRID_SIZE // 2
        center_y = self.GRID_SIZE // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.snake_direction = "Right"
        self.next_direction = "Right"

        # Set game speed based on mode
        if mode == GameMode.SPEED:
            self.game_speed = 150
            self.base_speed = 150
        elif mode == GameMode.ZEN:
            self.game_speed = 120
            self.base_speed = 120
        else:
            self.game_speed = 100
            self.base_speed = 100

        # Time attack mode
        if mode == GameMode.TIME_ATTACK:
            self.time_remaining = 120  # 2 minutes
            self.start_time = datetime.now()

        # Generate obstacles for obstacles mode
        if mode == GameMode.OBSTACLES:
            self.generate_obstacles()

        self.spawn_food()
        self.update_game()
        self.draw_game()

    def generate_obstacles(self):
        """Generate random obstacles for obstacles mode"""
        self.obstacles = []
        num_obstacles = random.randint(8, 15)

        for _ in range(num_obstacles):
            while True:
                x = random.randint(2, self.GRID_SIZE - 3)
                y = random.randint(2, self.GRID_SIZE - 3)
                if (x, y) not in self.snake and (x, y) not in self.obstacles:
                    self.obstacles.append((x, y))
                    break

    def spawn_food(self):
        """Spawn food at a random location"""
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            if (x, y) not in self.snake and (x, y) not in self.obstacles:
                self.food = (x, y)
                break

        # Occasionally spawn powerups
        if random.random() < 0.15 and len(self.powerups) < 2:
            self.spawn_powerup()

    def spawn_powerup(self):
        """Spawn a random powerup"""
        while True:
            x = random.randint(0, self.GRID_SIZE - 1)
            y = random.randint(0, self.GRID_SIZE - 1)
            if ((x, y) not in self.snake and (x, y) not in self.obstacles
                and (x, y) != self.food and (x, y) not in [p[0] for p in self.powerups]):
                powerup_type = random.choice(list(PowerUpType))
                self.powerups.append(((x, y), powerup_type))
                break

    def queue_direction(self, direction):
        """Queue the next direction change"""
        if not self.running or self.paused:
            return

        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if direction != opposites.get(self.snake_direction):
            self.next_direction = direction

    def toggle_pause(self):
        """Toggle pause state"""
        if self.running and self.current_screen == "game":
            self.paused = not self.paused
            if self.paused:
                self.draw_pause_menu()
            else:
                self.update_game()

    def draw_pause_menu(self):
        """Draw pause menu overlay"""
        # Semi-transparent overlay
        overlay_width = 300
        overlay_height = 200
        x = (self.CANVAS_WIDTH - overlay_width) // 2
        y = (self.CANVAS_HEIGHT - overlay_height) // 2

        self.canvas.create_rectangle(
            x, y, x + overlay_width, y + overlay_height,
            fill=self.COLORS['bg_dark'],
            outline=self.COLORS['glass_border'],
            width=3,
            tags="pause"
        )

        self.canvas.create_text(
            x + overlay_width // 2, y + 50,
            text="⏸️ PAUSED",
            fill=self.COLORS['text_primary'],
            font=self.fonts['subtitle'],
            tags="pause"
        )

        self.canvas.create_text(
            x + overlay_width // 2, y + 100,
            text="Press SPACE to resume",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            tags="pause"
        )

        self.canvas.create_text(
            x + overlay_width // 2, y + 130,
            text="Press ESC for menu",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            tags="pause"
        )

    def update_game(self):
        """Main game loop"""
        if not self.running or self.paused:
            return

        # Update direction
        self.snake_direction = self.next_direction
        self.moves_count += 1

        # Calculate new head position
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Up":
            head_y -= 1
        elif self.snake_direction == "Down":
            head_y += 1
        elif self.snake_direction == "Left":
            head_x -= 1
        elif self.snake_direction == "Right":
            head_x += 1

        # Zen mode - wrap around edges
        if self.game_mode == GameMode.ZEN:
            head_x = head_x % self.GRID_SIZE
            head_y = head_y % self.GRID_SIZE

        new_head = (head_x, head_y)

        # Check collisions
        if self.game_mode != GameMode.ZEN:
            # Wall collision
            if (head_x < 0 or head_y < 0 or
                head_x >= self.GRID_SIZE or head_y >= self.GRID_SIZE):
                if self.active_powerup != PowerUpType.INVINCIBLE:
                    self.game_over()
                    return

        # Self collision
        if new_head in self.snake[1:]:
            if self.active_powerup != PowerUpType.INVINCIBLE:
                self.game_over()
                return

        # Obstacle collision
        if new_head in self.obstacles:
            if self.active_powerup != PowerUpType.INVINCIBLE:
                self.game_over()
                return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food collision
        ate_food = False
        if new_head == self.food:
            ate_food = True
            self.food_eaten += 1
            self.score += 10 * self.score_multiplier
            self.spawn_food()
            self.create_particle_effect(new_head, self.COLORS['food'])

            # Speed mode - increase speed
            if self.game_mode == GameMode.SPEED:
                self.game_speed = max(50, self.game_speed - 3)

        if not ate_food:
            self.snake.pop()

        # Check powerup collision
        for i, (pos, powerup_type) in enumerate(self.powerups):
            if new_head == pos:
                self.activate_powerup(powerup_type)
                self.powerups.pop(i)
                self.create_particle_effect(new_head, self.COLORS['powerup_score'])
                break

        # Update powerup timer
        if self.active_powerup:
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.deactivate_powerup()

        # Remove old powerups
        self.powerups = [p for p in self.powerups if random.random() > 0.01]

        # Update time for time attack
        if self.game_mode == GameMode.TIME_ATTACK:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.time_remaining = max(0, 120 - int(elapsed))
            if self.time_remaining <= 0:
                self.game_over()
                return

        # Update animation frame
        self.animation_frame = (self.animation_frame + 1) % 360

        # Continue game loop
        self.draw_game()
        self.root.after(self.game_speed, self.update_game)

    def activate_powerup(self, powerup_type):
        """Activate a powerup"""
        self.active_powerup = powerup_type
        self.powerup_timer = 100  # ~10 seconds depending on speed

        if powerup_type == PowerUpType.SPEED_BOOST:
            self.game_speed = max(30, self.game_speed // 2)
        elif powerup_type == PowerUpType.SLOW_DOWN:
            self.game_speed = min(300, self.game_speed * 2)
        elif powerup_type == PowerUpType.SCORE_MULTIPLIER:
            self.score_multiplier = 2

    def deactivate_powerup(self):
        """Deactivate current powerup"""
        if self.active_powerup == PowerUpType.SPEED_BOOST:
            self.game_speed = self.base_speed
        elif self.active_powerup == PowerUpType.SLOW_DOWN:
            self.game_speed = self.base_speed
        elif self.active_powerup == PowerUpType.SCORE_MULTIPLIER:
            self.score_multiplier = 1

        self.active_powerup = None
        self.powerup_timer = 0

    def create_particle_effect(self, position, color):
        """Create particle effect at position"""
        for _ in range(8):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 5)
            self.particle_effects.append({
                'x': position[0],
                'y': position[1],
                'dx': speed * random.choice([-1, 1]),
                'dy': speed * random.choice([-1, 1]),
                'life': 20,
                'color': color
            })

    def draw_game(self):
        """Draw the complete game state"""
        self.canvas.delete("all")

        # Draw game area background
        self.canvas.create_rectangle(
            0, 0, self.CANVAS_WIDTH, self.CANVAS_HEIGHT,
            fill=self.COLORS['bg_dark'],
            outline=''
        )

        # Draw grid
        for i in range(self.GRID_SIZE + 1):
            # Vertical lines
            self.canvas.create_line(
                i * self.CELL_SIZE, 0,
                i * self.CELL_SIZE, self.CANVAS_HEIGHT,
                fill=self.COLORS['bg_gradient_1'],
                width=1
            )
            # Horizontal lines
            self.canvas.create_line(
                0, i * self.CELL_SIZE,
                self.CANVAS_WIDTH, i * self.CELL_SIZE,
                fill=self.COLORS['bg_gradient_1'],
                width=1
            )

        # Draw obstacles
        for x, y in self.obstacles:
            px, py = x * self.CELL_SIZE, y * self.CELL_SIZE
            self.canvas.create_rectangle(
                px + 2, py + 2, px + self.CELL_SIZE - 2, py + self.CELL_SIZE - 2,
                fill=self.COLORS['obstacle'],
                outline=self.COLORS['glass_border'],
                width=2
            )

        # Draw food with glow effect
        if self.food:
            fx, fy = self.food
            px, py = fx * self.CELL_SIZE, fy * self.CELL_SIZE

            # Glow effect
            glow_size = 5 + abs((self.animation_frame % 60) - 30) // 10
            self.canvas.create_oval(
                px - glow_size, py - glow_size,
                px + self.CELL_SIZE + glow_size, py + self.CELL_SIZE + glow_size,
                fill='', outline=self.COLORS['food_glow'], width=2
            )

            # Food
            self.canvas.create_oval(
                px + 3, py + 3, px + self.CELL_SIZE - 3, py + self.CELL_SIZE - 3,
                fill=self.COLORS['food'],
                outline=self.COLORS['food_glow'],
                width=2
            )

        # Draw powerups
        for (x, y), powerup_type in self.powerups:
            px, py = x * self.CELL_SIZE, y * self.CELL_SIZE

            color_map = {
                PowerUpType.SPEED_BOOST: self.COLORS['powerup_speed'],
                PowerUpType.SLOW_DOWN: self.COLORS['powerup_slow'],
                PowerUpType.SCORE_MULTIPLIER: self.COLORS['powerup_score'],
                PowerUpType.INVINCIBLE: self.COLORS['powerup_invincible'],
            }

            symbol_map = {
                PowerUpType.SPEED_BOOST: "⚡",
                PowerUpType.SLOW_DOWN: "🐌",
                PowerUpType.SCORE_MULTIPLIER: "✨",
                PowerUpType.INVINCIBLE: "🛡️",
            }

            color = color_map.get(powerup_type, self.COLORS['powerup_score'])
            self.canvas.create_rectangle(
                px + 2, py + 2, px + self.CELL_SIZE - 2, py + self.CELL_SIZE - 2,
                fill=color,
                outline=self.COLORS['glass_border'],
                width=2
            )
            self.canvas.create_text(
                px + self.CELL_SIZE // 2, py + self.CELL_SIZE // 2,
                text=symbol_map.get(powerup_type, "?"),
                fill=self.COLORS['text_primary'],
                font=self.fonts['small']
            )

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            px, py = x * self.CELL_SIZE, y * self.CELL_SIZE

            if i == 0:  # Head
                # Head with gradient
                self.canvas.create_rectangle(
                    px + 1, py + 1, px + self.CELL_SIZE - 1, py + self.CELL_SIZE - 1,
                    fill=self.COLORS['snake_head'],
                    outline=self.COLORS['glass_border'],
                    width=2
                )
                # Eyes
                eye_offset = 6
                if self.snake_direction == "Right":
                    eye1 = (px + self.CELL_SIZE - 8, py + eye_offset)
                    eye2 = (px + self.CELL_SIZE - 8, py + self.CELL_SIZE - eye_offset)
                elif self.snake_direction == "Left":
                    eye1 = (px + 8, py + eye_offset)
                    eye2 = (px + 8, py + self.CELL_SIZE - eye_offset)
                elif self.snake_direction == "Up":
                    eye1 = (px + eye_offset, py + 8)
                    eye2 = (px + self.CELL_SIZE - eye_offset, py + 8)
                else:  # Down
                    eye1 = (px + eye_offset, py + self.CELL_SIZE - 8)
                    eye2 = (px + self.CELL_SIZE - eye_offset, py + self.CELL_SIZE - 8)

                for eye_x, eye_y in [eye1, eye2]:
                    self.canvas.create_oval(
                        eye_x - 2, eye_y - 2, eye_x + 2, eye_y + 2,
                        fill='white'
                    )
            else:  # Body
                # Calculate color gradient
                color_idx = min(i % len(self.COLORS['snake_gradient']),
                               len(self.COLORS['snake_gradient']) - 1)
                color = self.COLORS['snake_gradient'][color_idx]

                self.canvas.create_rectangle(
                    px + 2, py + 2, px + self.CELL_SIZE - 2, py + self.CELL_SIZE - 2,
                    fill=color,
                    outline=self.COLORS['glass_border_2'],
                    width=1
                )

        # Draw particle effects
        active_particles = []
        for particle in self.particle_effects:
            if particle['life'] > 0:
                px = (particle['x'] + particle['dx'] / 10) * self.CELL_SIZE
                py = (particle['y'] + particle['dy'] / 10) * self.CELL_SIZE
                size = particle['life'] // 4
                self.canvas.create_oval(
                    px - size, py - size, px + size, py + size,
                    fill=particle['color'],
                    outline=''
                )
                particle['life'] -= 1
                active_particles.append(particle)
        self.particle_effects = active_particles

        # Draw sidebar
        self.draw_sidebar()

    def draw_sidebar(self):
        """Draw the sidebar with game stats"""
        sidebar_x = self.CANVAS_WIDTH + 10
        sidebar_width = 280

        # Stats panel
        panel_y = 10
        self.create_glass_panel(sidebar_x, panel_y, sidebar_width, 180)

        # Game mode
        self.canvas.create_text(
            sidebar_x + sidebar_width // 2, panel_y + 20,
            text=self.game_mode.value,
            fill=self.COLORS['glass_border'],
            font=self.fonts['button']
        )

        # Score
        self.canvas.create_text(
            sidebar_x + 20, panel_y + 50,
            text="Score:",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            anchor="w"
        )
        self.canvas.create_text(
            sidebar_x + sidebar_width - 20, panel_y + 50,
            text=str(self.score),
            fill=self.COLORS['text_primary'],
            font=self.fonts['score'],
            anchor="e"
        )

        # Length
        self.canvas.create_text(
            sidebar_x + 20, panel_y + 80,
            text="Length:",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            anchor="w"
        )
        self.canvas.create_text(
            sidebar_x + sidebar_width - 20, panel_y + 80,
            text=str(len(self.snake)),
            fill=self.COLORS['text_primary'],
            font=self.fonts['score'],
            anchor="e"
        )

        # Food eaten
        self.canvas.create_text(
            sidebar_x + 20, panel_y + 110,
            text="Food:",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small'],
            anchor="w"
        )
        self.canvas.create_text(
            sidebar_x + sidebar_width - 20, panel_y + 110,
            text=str(self.food_eaten),
            fill=self.COLORS['text_primary'],
            font=self.fonts['score'],
            anchor="e"
        )

        # Time (for time attack)
        if self.game_mode == GameMode.TIME_ATTACK:
            self.canvas.create_text(
                sidebar_x + 20, panel_y + 140,
                text="Time:",
                fill=self.COLORS['text_secondary'],
                font=self.fonts['small'],
                anchor="w"
            )
            time_color = self.COLORS['food'] if self.time_remaining < 30 else self.COLORS['text_primary']
            self.canvas.create_text(
                sidebar_x + sidebar_width - 20, panel_y + 140,
                text=f"{self.time_remaining}s",
                fill=time_color,
                font=self.fonts['score'],
                anchor="e"
            )

        # Active powerup
        if self.active_powerup:
            powerup_y = 200
            self.create_glass_panel(sidebar_x, powerup_y, sidebar_width, 80)

            self.canvas.create_text(
                sidebar_x + sidebar_width // 2, powerup_y + 15,
                text="Active Powerup",
                fill=self.COLORS['text_secondary'],
                font=self.fonts['tiny']
            )

            powerup_names = {
                PowerUpType.SPEED_BOOST: "⚡ Speed Boost",
                PowerUpType.SLOW_DOWN: "🐌 Slow Down",
                PowerUpType.SCORE_MULTIPLIER: "✨ Score x2",
                PowerUpType.INVINCIBLE: "🛡️ Invincible",
            }

            self.canvas.create_text(
                sidebar_x + sidebar_width // 2, powerup_y + 40,
                text=powerup_names.get(self.active_powerup, "Unknown"),
                fill=self.COLORS['text_primary'],
                font=self.fonts['button']
            )

            # Timer bar
            bar_width = sidebar_width - 40
            bar_progress = (self.powerup_timer / 100) * bar_width
            self.canvas.create_rectangle(
                sidebar_x + 20, powerup_y + 60,
                sidebar_x + 20 + bar_width, powerup_y + 70,
                fill=self.COLORS['bg_gradient_1'],
                outline=self.COLORS['glass_border']
            )
            self.canvas.create_rectangle(
                sidebar_x + 20, powerup_y + 60,
                sidebar_x + 20 + bar_progress, powerup_y + 70,
                fill=self.COLORS['powerup_score'],
                outline=''
            )

        # High score panel
        high_score_y = 290 if self.active_powerup else 210
        self.create_glass_panel(sidebar_x, high_score_y, sidebar_width, 100)

        self.canvas.create_text(
            sidebar_x + sidebar_width // 2, high_score_y + 15,
            text="🏆 High Score",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['tiny']
        )

        mode_high_scores = self.high_scores.get(self.game_mode.value, [])
        if mode_high_scores:
            best = mode_high_scores[0]
            self.canvas.create_text(
                sidebar_x + sidebar_width // 2, high_score_y + 45,
                text=str(best['score']),
                fill=self.COLORS['glass_border'],
                font=self.fonts['subtitle']
            )
            self.canvas.create_text(
                sidebar_x + sidebar_width // 2, high_score_y + 75,
                text=f"Length: {best['length']} | Food: {best['food']}",
                fill=self.COLORS['text_secondary'],
                font=self.fonts['tiny']
            )
        else:
            self.canvas.create_text(
                sidebar_x + sidebar_width // 2, high_score_y + 50,
                text="No high score yet!",
                fill=self.COLORS['text_secondary'],
                font=self.fonts['small']
            )

        # Controls reminder
        controls_y = high_score_y + 110
        self.canvas.create_text(
            sidebar_x + sidebar_width // 2, controls_y,
            text="SPACE - Pause",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['tiny']
        )
        self.canvas.create_text(
            sidebar_x + sidebar_width // 2, controls_y + 15,
            text="ESC - Menu",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['tiny']
        )

    def game_over(self):
        """Handle game over"""
        self.running = False
        self.save_score()
        self.show_game_over()

    def save_score(self):
        """Save the current score if it's a high score"""
        mode_key = self.game_mode.value
        if mode_key not in self.high_scores:
            self.high_scores[mode_key] = []

        score_data = {
            'score': self.score,
            'length': len(self.snake),
            'food': self.food_eaten,
            'moves': self.moves_count,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.high_scores[mode_key].append(score_data)
        self.high_scores[mode_key].sort(key=lambda x: x['score'], reverse=True)
        self.high_scores[mode_key] = self.high_scores[mode_key][:10]  # Keep top 10

        # Save to file
        try:
            with open('high_scores.json', 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def load_high_scores(self):
        """Load high scores from file"""
        if os.path.exists('high_scores.json'):
            try:
                with open('high_scores.json', 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading high scores: {e}")
        return {}

    def show_game_over(self):
        """Display game over screen"""
        self.current_screen = "game_over"
        self.canvas.delete("all")

        # Background
        for i in range(self.CANVAS_HEIGHT):
            color_ratio = i / self.CANVAS_HEIGHT
            r = int(10 + (29 - 10) * color_ratio)
            g = int(14 + (53 - 14) * color_ratio)
            b = int(39 + (97 - 39) * color_ratio)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(
                0, i, self.CANVAS_WIDTH + 300, i,
                fill=color
            )

        # Panel
        panel_width = 450
        panel_height = 400
        panel_x = (self.CANVAS_WIDTH + 300 - panel_width) // 2
        panel_y = 50
        self.create_glass_panel(panel_x, panel_y, panel_width, panel_height)

        # Title
        self.canvas.create_text(
            panel_x + panel_width // 2, panel_y + 50,
            text="GAME OVER",
            fill=self.COLORS['food'],
            font=self.fonts['title']
        )

        # Stats
        stats_y = panel_y + 120

        self.canvas.create_text(
            panel_x + panel_width // 2, stats_y,
            text=f"Final Score: {self.score}",
            fill=self.COLORS['text_primary'],
            font=self.fonts['subtitle']
        )

        self.canvas.create_text(
            panel_x + panel_width // 2, stats_y + 50,
            text=f"Length: {len(self.snake)} | Food Eaten: {self.food_eaten}",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['button']
        )

        self.canvas.create_text(
            panel_x + panel_width // 2, stats_y + 85,
            text=f"Total Moves: {self.moves_count}",
            fill=self.COLORS['text_secondary'],
            font=self.fonts['small']
        )

        # Check if new high score
        mode_scores = self.high_scores.get(self.game_mode.value, [])
        if mode_scores and self.score >= mode_scores[0]['score']:
            self.canvas.create_text(
                panel_x + panel_width // 2, stats_y + 120,
                text="🏆 NEW HIGH SCORE! 🏆",
                fill=self.COLORS['glass_border'],
                font=self.fonts['button']
            )

        # Buttons
        button_y = panel_y + 300
        self.create_button(
            panel_x + 50, button_y,
            panel_width - 100, 40,
            "🔄 Play Again",
            lambda: self.start_game(self.game_mode),
            tags="game_over"
        )

        self.create_button(
            panel_x + 50, button_y + 60,
            panel_width - 100, 40,
            "⬅️ Back to Menu",
            self.show_menu,
            tags="game_over"
        )

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    game = SnakeGame(root)
    root.mainloop()
