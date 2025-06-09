import sys
import os
import json
import numpy as np
import random
from collections import defaultdict
import ast
from simulation_settings import QL_SETTINGS



class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # The number of possible states
        self.action_size = action_size  # The number of possible actions
        self.q_table = defaultdict(self._default_q_values)  # Initialize Q-table with default values for unseen states
        self.q_table_path = os.path.join("q_learning_implementation", "q_tables", QL_SETTINGS["Q_TABLE_FILENAME"])
        self.learning_rate = QL_SETTINGS["LEARNING_RATE"]  # Alpha
        self.discount_factor = QL_SETTINGS["DISCOUNT_FACTOR"]  # Gamma
        self.exploration_rate = QL_SETTINGS["EXPLORATION_RATE"]  # Epsilon
        self.exploration_decay = QL_SETTINGS["EXPLORATION_DECAY"]  # Epsilon decay
        self.min_exploration_rate = QL_SETTINGS["MIN_EXPLORATION_RATE"]  # Minimum epsilon

    def load_q_table(self):
        """
        Load the Q-table from a JSON file. 
        Returns True if successful, False if the file does not exist.
        """
        if not os.path.exists(self.q_table_path):
            return False
        with open(self.q_table_path, "r") as f:
            data = json.load(f)
            self.q_table = defaultdict(self._default_q_values)
            for state_str, actions_list in data.items():
                state = ast.literal_eval(state_str)
                self.q_table[state] = np.array(actions_list)
        return True

    def save_q_table(self):
        """Save the Q-table to a JSON file."""
        serializable_q_table = {str(state): actions.tolist() for state, actions in self.q_table.items()}
        with open(self.q_table_path, "w") as f:
            json.dump(serializable_q_table, f)

    def _default_q_values(self):
        return np.zeros(self.action_size)

# Get an action based on the current state using epsilon-greedy strategy.
    def get_action(self, state, use_epsilon=True):
        """Choose an action based on the current state using epsilon-greedy strategy."""
        if len(state) != self.state_size:
            print(f"Warning: State has {len(state)} variables, but state_size is {self.state_size}")
    
        # Use epsilon-greedy only when use_epsilon is True (learning mode)
        if use_epsilon and random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        else:
            return np.argmax(self.q_table[state])

    def update_q_value(self, state, action, reward, next_state):
        """
        Bellman Equation update for Q-learning:
        Q[state][action] = Q[state][action] + alpha * (reward + gamma * max(Q[next_state]) - Q[state][action])
        """
        alpha = self.learning_rate
        gamma = self.discount_factor
        Q = self.q_table
        max_next_q = np.max(Q[next_state])
        Q[state][action] = Q[state][action] + alpha * (reward + gamma * max_next_q - Q[state][action])

    def decay_exploration(self):
        """decay exploration rate (epsilon) over time"""
        self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
