# 🐍 Snake Game - Ultimate Edition

A modern, feature-rich snake game with stunning glassmorphism UI design, multiple game modes, power-ups, and comprehensive scoring system.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🎨 **Glassmorphism/Liquid Glass UI**
- Modern translucent panels with gradient borders
- Smooth animations and particle effects
- Beautiful color gradients throughout the interface
- Hover effects on interactive elements
- Professional dark theme with cyan/purple accents

### 🎮 **5 Unique Game Modes**

1. **🎮 Classic Mode** - Traditional snake gameplay with progressive difficulty
2. **⚡ Speed Mode** - Snake accelerates as you collect food (for adrenaline junkies!)
3. **🧱 Obstacles Mode** - Navigate around random obstacles on the board
4. **⏱️ Time Attack** - Score as much as possible in 2 minutes
5. **🌊 Zen Mode** - Relaxing gameplay with no walls (wrap-around edges)

### 💎 **Power-Ups System**
Collect special power-ups that randomly appear on the board:
- **⚡ Speed Boost** - Temporarily increases snake speed
- **🐌 Slow Down** - Slows down the snake for better control
- **✨ Score Multiplier** - Doubles your points for a limited time
- **🛡️ Invincible** - Temporary immunity from collisions

### 🏆 **Advanced Scoring System**
- Real-time score tracking
- High score persistence (saved to JSON file)
- Separate leaderboards for each game mode
- Top 10 scores saved per mode
- Detailed statistics: score, length, food eaten, moves, timestamp

### 🎯 **Game Features**
- Snake eyes that follow the direction of movement
- Animated food with pulsing glow effect
- Particle effects when eating food or collecting power-ups
- Pause functionality (SPACE key)
- Smooth grid-based movement
- Input buffering to prevent missed commands
- Real-time sidebar with game statistics
- Professional game over screen with detailed stats

### 🖥️ **User Interface**
- Main menu with all game modes
- High scores screen showing top players
- In-game sidebar with live statistics
- Pause menu overlay
- Game over screen with "New High Score" celebration
- Responsive button hover effects
- Visual feedback for all interactions

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

### Installing Tkinter
If Tkinter is not installed on your system:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
Tkinter comes pre-installed with Python on macOS.

**Windows:**
Tkinter comes pre-installed with Python on Windows.

### Running the Game
```bash
python3 snake.py
```

Or simply:
```bash
python snake.py
```

## 🎮 How to Play

### Controls
- **Arrow Keys** or **WASD** - Control snake direction
- **SPACE** - Pause/Resume game
- **ESC** - Return to main menu

### Objective
- Guide the snake to eat food (red circles)
- Grow longer with each food item
- Avoid hitting walls (except in Zen mode)
- Avoid hitting yourself
- Collect power-ups for special abilities
- Achieve the highest score possible!

### Scoring
- **Food**: 10 points (20 with score multiplier)
- **Length**: Longer snake = bragging rights
- **Survival**: Stay alive as long as possible

## 🎨 Game Modes Explained

### Classic Mode
The traditional snake experience with balanced difficulty. Perfect for players of all skill levels.

### Speed Mode
For experienced players seeking a challenge! The snake moves faster with each food item collected. How long can you survive at maximum speed?

### Obstacles Mode
Random obstacles are placed on the board at the start. Navigate carefully around them while growing your snake. Requires strategic planning!

### Time Attack
Race against the clock! You have exactly 2 minutes to score as many points as possible. Fast-paced and intense.

### Zen Mode
Relaxing gameplay with no walls - the snake wraps around to the opposite side of the screen. Perfect for casual play and racking up massive scores.

## 💾 High Scores

High scores are automatically saved to `high_scores.json` in the same directory as the game. Each game mode has its own separate leaderboard with the top 10 scores.

Saved information includes:
- Final score
- Snake length
- Food eaten
- Total moves
- Date and time of achievement

## 🛠️ Technical Details

### Architecture
- **Object-Oriented Design**: Clean, maintainable code structure
- **Enum Classes**: Type-safe game modes and power-ups
- **Persistent Storage**: JSON-based high score system
- **Event-Driven**: Responsive to user input
- **Animation System**: Smooth particle effects and visual feedback

### Code Features
- Input buffering to prevent direction change glitches
- Collision detection for walls, self, obstacles, and items
- Proper game state management (menu, game, game_over, paused)
- Modular design with separation of concerns
- Comprehensive error handling

### Customization
The game uses a centralized color system. To customize the look:
1. Open `snake.py`
2. Locate the `COLORS` dictionary in the `__init__` method
3. Modify the hex color values to your preference
4. Save and run!

## 🐛 Bug Fixes from Original

This ultimate edition fixes all bugs from the original version:
- ✅ Added proper score tracking
- ✅ Fixed input direction buffering
- ✅ Added pause functionality
- ✅ Improved collision detection
- ✅ Added game state management
- ✅ Fixed game loop timing issues
- ✅ Added proper game over handling

## 🎯 Future Enhancements

Potential features for future versions:
- Sound effects and background music
- Online leaderboards
- Multiplayer mode
- Custom snake skins
- More power-up types
- Achievement system
- Difficulty settings within each mode
- Mobile touch controls

## 📝 License

This project is open source and available under the MIT License.

## 🙌 Credits

Developed with ❤️ using Python and Tkinter

## 🎮 Screenshots

### Main Menu
Beautiful glassmorphism design with all game modes clearly displayed.

### In-Game
- Clean grid-based gameplay
- Live statistics sidebar
- Animated food with glow effects
- Colorful snake with gradient body
- Power-ups with distinct visual styles

### High Scores
Dedicated screen showing top performers for each game mode.

### Game Over
Professional game over screen with complete statistics and quick restart option.

---

## 🚀 Quick Start Guide

1. **Install Python 3.6+** if you haven't already
2. **Ensure Tkinter is installed** (see Installation section)
3. **Download or clone** this repository
4. **Navigate** to the game directory
5. **Run** `python3 snake.py`
6. **Select** your preferred game mode
7. **Play** and enjoy!

---

## 💡 Tips & Tricks

1. **Plan Ahead**: In Classic and Obstacles mode, always think 2-3 moves ahead
2. **Speed Mode**: Grab the Slow Down power-up when things get too fast
3. **Time Attack**: Focus on efficiency - don't chase every food item
4. **Zen Mode**: Use the wrap-around feature strategically to escape tight spots
5. **Power-Ups**: The Invincible shield can save you in dangerous situations
6. **Obstacles**: In Obstacles mode, keep to the edges early on

---

**Ready to play? Launch the game and become the ultimate snake master!** 🏆
