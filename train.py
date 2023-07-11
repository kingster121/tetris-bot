import random
import time

from game import Tetris


class TetrisQLearning:
    def __init__(self, epsilon=0.1, alpha=0.5, gamma=0.9):
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.q_table = {}  # Q-table to store Q-values

    def update_q_table(self, state, action, reward, next_state):
        max_q_value = max(self.q_table.get(next_state, {}).values(), default=0)
        current_q_value = self.q_table.get(state, {}).get(action, 0)
        updated_q_value = (1 - self.alpha) * current_q_value + self.alpha * (
            reward + self.gamma * max_q_value
        )
        self.q_table.setdefault(state, {})[action] = updated_q_value

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)  # Randomly select an action
        else:
            return max(self.q_table.get(state, {}).items(), key=lambda x: x[1])[0]

    def train(self, num_episodes):
        for episode in range(num_episodes):
            tetris.reset()
            state = tetris.observation()
            done = False
            total_reward = 0
            start_time = time.time()

            while not done:
                action = self.select_action(state)
                print(action)
                tetris.perform_action(action)

                prev_reward = total_reward
                total_reward = tetris.reward()
                reward = total_reward - prev_reward

                next_state = tetris.observation()

                self.update_q_table(state, action, reward, next_state)

                state = next_state
                elapsed_time = time.time() - start_time
                if elapsed_time >= 60:
                    print("Done")
                    done = True

            print(f"Episode: {episode+1}, Total Reward: {total_reward}")

        print("Training completed.")


# Create an instance of Tetris game environment
tetris = Tetris()

# Create an instance of Q-learning agent
agent = TetrisQLearning()

# Start the game
time.sleep(10)
tetris.start()

# Train the agent
print("prior")
agent.train(num_episodes=1000)
print("after")

# Once training is completed, you can use the learned Q-values to play the game
while True:
    state = tetris.observation()
    action = agent.select_action(state)
    tetris.perform_action(action)
    time.sleep(0.1)  # Adjust the delay as per your game's speed
