import pygame
from game import Game
from q_agent import QAgent

pygame.init()

# Create game environment WITH rendering
game = Game(750, 700, 50, render=True)

# Load trained agent (pure exploitation)
agent = QAgent(epsilon=0.0)
agent.load("q_table.pkl")

clock = pygame.time.Clock()
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current discrete state
    state = game.get_discrete_state()

    # Agent selects best action (greedy)
    action = agent.choose_action(state)

    # Step environment (render happens inside game.step)
    _, _, done = game.step(action)

    # Reset game after terminal state
    if done:
        pygame.time.delay(2000)
        game.reset()

    clock.tick(80)

pygame.quit()
