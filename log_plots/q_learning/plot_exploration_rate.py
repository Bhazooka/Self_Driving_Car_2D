import sys
import os

from visualization import Visualizer
from simulation_settings import QL_SETTINGS  # Use QL_SETTINGS, not QL_CONFIG

# Add the grandparent directory to the path (for config.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add the parent directory (for visualizer.py)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    grandparent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    log_file = os.path.join(grandparent_directory, "q_learning_logs", "q_table.txt")

    visualizer = Visualizer(log_file)
    target_epsilon = QL_SETTINGS["MIN_EXPLORATION_RATE"]
    visualizer.plot_exploration_rate_decay(target_epsilon, QL_SETTINGS["EXPLORATION_DECAY"])

if __name__ == "__main__":
    main()
