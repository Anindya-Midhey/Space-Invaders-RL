# 👾 Space Invaders AI using Reinforcement Learning (Q-Learning)

## 📌 Project Overview

This project implements an **AI-powered Space Invaders game** using **Reinforcement Learning (Q-Learning)** and **Pygame**.

The AI agent learns how to play the classic **Space Invaders** game by interacting with the environment, receiving rewards, and improving its strategy over time using a **Q-table based learning approach**.

The project supports:

- 🎮 Manual gameplay
- 🤖 AI-based gameplay using a trained Q-Learning agent
- 📈 Reward visualization during training
- 💾 Saving and loading trained Q-table
- 🛸 Dynamic enemy spawning and shooting system

---

## 🎯 Objective

The main objective of this project is to:

- Build a **Space Invaders environment** using Pygame
- Train an AI agent using **Q-Learning**
- Learn optimal actions through reward maximization
- Evaluate agent performance after training
- Visualize learning progress using reward plots

---

## 🧠 Reinforcement Learning Approach

This project uses **Q-Learning**, a model-free Reinforcement Learning algorithm.

The agent learns by:

### State Representation
The environment state consists of:

- Spaceship position
- Closest alien X position
- Closest alien Y position
- Remaining lives

### Actions

The agent can perform **4 actions**:

| Action | Description |
|--------|-------------|
| 0 | Do nothing |
| 1 | Move Left |
| 2 | Move Right |
| 3 | Shoot |

### Reward System

The AI agent receives rewards based on gameplay:

✅ Destroying aliens → Positive reward

✅ Winning the game → Large positive reward

❌ Losing lives → Negative reward

❌ Collision with enemies → Penalty

❌ Idle survival → Small living penalty

---

## 🎮 Game Features

- Classic **Space Invaders gameplay**
- Alien movement and attack system
- Laser shooting mechanics
- Obstacle blocks for protection
- UFO enemy spawning
- Score and high score tracking
- Game over and win condition
- AI gameplay after training
- Manual gameplay support

---

## 📁 Project Structure

```text
Space-Invaders-RL/
│── main.py                 # Manual game mode
│── train.py                # Train RL agent
│── test.py                 # Test trained AI
│── game.py                 # Game environment
│── q_agent.py              # Q-learning implementation
│── spaceship.py            # Spaceship mechanics
│── alien.py                # Alien and UFO logic
│── laser.py                # Laser mechanics
│── obstarcle.py            # Defensive obstacles
│── q_table.pkl             # Saved trained model
│── rewards.png             # Training reward graph
│── highscore.txt           # Stores high score
│── README.md
│── requirements.txt
│
├── Graphics/
│   ├── alien_1.png
│   ├── alien_2.png
│   ├── alien_3.png
│   ├── spaceship.png
│   └── ufo.png
│
└── Font/
    └── monogram.ttf
```

---

## ⚙️ Technologies Used

- Python
- Pygame
- Matplotlib
- Reinforcement Learning (Q-Learning)
- Pickle Serialization

---

## 🚀 Installation & Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/Anindya-Midhey/Space-Invaders-RL.git
```

### Step 2: Move to Project Directory

```bash
cd Space-Invaders-RL
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### 1️⃣ Play the Game Manually

Run:

```bash
python main.py
```

Controls:

| Key | Action |
|-----|--------|
| ← | Move Left |
| → | Move Right |
| Space | Shoot |

---

### 2️⃣ Train the AI Agent

Run:

```bash
python train.py
```

This will:

- Train the Q-Learning agent
- Save the trained model as:

```text
q_table.pkl
```

- Generate reward visualization:

```text
rewards.png
```

---

### 3️⃣ Test the Trained AI

Run:

```bash
python test.py
```

The trained AI agent will automatically play the game.

---

## 📈 Training Details

Training Configuration:

- **Episodes:** 1000
- **Maximum Steps per Episode:** 1000
- **Learning Rate (α):** 0.1
- **Discount Factor (γ):** 0.99
- **Initial Epsilon:** 0.3
- **Epsilon Decay:** 0.995
- **Minimum Epsilon:** 0.05

---

## 📊 Reward Visualization

During training, rewards per episode are plotted to evaluate learning performance.

Example:

- `rewards.png`

This graph shows how the AI agent improves over training episodes.

---

## 🔥 Key Highlights

✅ Custom-built Space Invaders game engine

✅ Q-Learning based AI agent

✅ Reward shaping strategy

✅ Dynamic enemy movement

✅ Headless training mode for faster RL training

✅ Save and reload trained model

✅ Manual and AI gameplay support

---

## 🔮 Future Improvements

- Deep Q-Network (DQN) implementation
- Better state representation
- Smarter reward engineering
- Difficulty scaling
- Multiple enemy types
- Model performance analytics dashboard

---

## 👨‍💻 Author

**Anindya Midhey**

---

## ⭐ If you found this project useful, consider giving it a star!
