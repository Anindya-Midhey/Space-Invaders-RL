import random
import pickle
from collections import defaultdict


class QAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.3):
        # Q-table: state -> [Q0, Q1, Q2, Q3]
        self.q = defaultdict(lambda: [0, 0, 0, 0])
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon   # 🔴 keep > 0 for movement

    def choose_action(self, state):
        """
        Actions:
        0 = do nothing
        1 = move left
        2 = move right
        3 = shoot
        """

        # 🔥 Exploration (guarantees movement)
        if random.random() < self.epsilon:
            return random.choice([1, 2, 3])  # avoid 'do nothing'

        # Exploitation
        q_values = self.q[state]
        best_action = max(range(4), key=lambda a: q_values[a])

        # 🚨 If best action is 'do nothing', force action
        if best_action == 0:
            return random.choice([1, 2, 3])

        return best_action

    def learn(self, state, action, reward, next_state, done):
        best_next = max(self.q[next_state])
        target = reward if done else reward + self.gamma * best_next
        self.q[state][action] += self.alpha * (target - self.q[state][action])

    def save(self, path="q_table.pkl"):
        with open(path, "wb") as f:
            pickle.dump(dict(self.q), f)

    def load(self, path="q_table.pkl"):
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                self.q = defaultdict(lambda: [0, 0, 0, 0], data)
        except FileNotFoundError:
            print("⚠️ Q-table not found. Starting fresh.")
