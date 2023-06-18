import numpy as np
import tensorflow as tf
from tensorflow.keras import layers

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.batch_size = 64
        self.memory = []  # Experience replay memory
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_decay = 0.995  # Exploration decay rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential()
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(lr=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self):
        minibatch = np.random.choice(len(self.memory), self.batch_size, replace=False)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def end_game(self, game_state):
        state = np.array([list(game_state.values())])  # Convert the game state to a numpy array
        action = self.act(state)
        self.remember(state, action, 0, state, True)  # Assuming no reward at the end of the game
        self.replay(self.batch_size)

    def dict2tensor(self, dictionary):
        return np.array([])

# Usage example
state_size = 10  # Define your own state size
action_size = 4  # Define your own action size

# Create an instance of the DQNAgent
agent = DQNAgent(state_size, action_size)

# Training loop
while True:
    # Initialize the game state
    game_state = initialize_game_state()  # Define your own game state initialization function
    done = False

    while not done:
        # Agent selects an action
        action = agent.act(game_state)

        # Apply the action and get the next state, reward, and done flag
        next_state, reward, done = apply_action(action)  # Define your own function

        # Remember the current state, action, reward, next state, and done flag
        agent.remember(game_state, action, reward, next_state, done)

        # Update the game state
        game_state = next_state

    # Perform experience replay and update the agent's Q-network
    agent.replay(agent.batch_size)

# After the training loop, when you want to make a move based on the learned Q-network:
def make_move(game_state):
    state = np.array([list(game_state.values())])  # Convert the game state to a numpy array
    action = agent.act(state)
    return action