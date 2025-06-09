import os
from visualization import Visualizer

def main():
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_file = os.path.join(parent_directory, "q_learning_logs", "q_table.txt")

    visualizer = Visualizer(log_file)
    visualizer.read_log()
    visualizer.plot_progress()

if __name__ == "__main__":
    main()