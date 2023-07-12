import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from collections import deque
import random


# Define the DQN class
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95  # Discount factor
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Exploration decay rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.learning_rate = 0.001
        self.model = self.build_model()

    def build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation="relu"))
        model.add(layers.Dense(24, activation="relu"))
        model.add(layers.Dense(self.action_size, activation="linear"))
        model.compile(
            loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate)
        )
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        else:
            return np.argmax(self.model.predict(state)[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward

            if not done:
                target = reward + self.gamma * np.amax(
                    self.model.predict(next_state)[0]
                )

            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, env, num_episodes, batch_size):
        for episode in range(num_episodes):
            state = env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            total_reward = 0

            while not done:
                action = self.act(state)
                next_state, reward, done, _ = env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])

                self.remember(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward

                if done:
                    print(f"Episode: {episode + 1}, Total Reward: {total_reward}")

                if len(self.memory) > batch_size:
                    self.replay(batch_size)


# Example usage
env = GymEnvironment()  # Replace with your own environment

state_size = env.observation_space.shape[0]
action_size = env.action_space.n

agent = DQNAgent(state_size, action_size)
agent.train(env, num_episodes=100, batch_size=32)
