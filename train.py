import pygame
import matplotlib.pyplot as plt
from game import Game
from q_agent import QAgent

# ───────── CONFIG ─────────
EPISODES = 1000
MAX_STEPS = 1000

# ───────── INIT (HEADLESS) ─────────
pygame.init()

# IMPORTANT: render=False disables game window
game = Game(750, 700, 50, render=False)
agent = QAgent()

episode_rewards = []

# ───────── TRAINING LOOP ─────────
for ep in range(EPISODES):
    state = game.get_discrete_state()
    total_reward = 0
    done = False
    step_count = 0

    while not done and step_count < MAX_STEPS:
        action = agent.choose_action(state)

        next_state, reward, done = game.step(action)

        agent.learn(state, action, reward, next_state, done)

        total_reward += reward
        state = next_state
        step_count += 1

    # Epsilon decay
    agent.epsilon = max(0.05, agent.epsilon * 0.995)

    episode_rewards.append(total_reward)

    game.reset()

    print(
        f"Episode {ep+1:4d} | "
        f"Reward {total_reward:7.2f} | "
        f"Steps {step_count:4d} | "
        f"Epsilon {agent.epsilon:.3f}"
    )

# ───────── SAVE TRAINED AGENT ─────────
agent.save("q_table.pkl")

# ───────── PLOT AFTER TRAINING ─────────
plt.figure(figsize=(8, 5))
plt.plot(episode_rewards)
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Q-Learning: Reward vs Episode")
plt.grid(True)
plt.savefig("rewards.png")
plt.show()

pygame.quit()
