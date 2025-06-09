import os

class Logger:
    def __init__(self, log_file="training_log.txt"):    # default file=training_log.txt if the user doesn't provide one
        self.log_directory = "q_learning_logs"  # Use q_learning_logs as the log directory
        self.log_file = os.path.join(self.log_directory, log_file)  # Full path to the log file

        # Ensure the q_learning_logs directory exists
        os.makedirs(self.log_directory, exist_ok=True)

    def get_last_score(self):
        try:
            with open(self.log_file, "r") as log_file:
                lines = log_file.readlines()
                if lines:
                    last_line = lines[-1]  # Get the last line
                    last_score = float(last_line.strip())  # Convert the score to float
                    return last_score
        except FileNotFoundError:
            return 0.0  # If the file doesn't exist, return 0.0
        return 0.0  # If the file is empty, return 0.0

    def log_score(self, score):
        with open(self.log_file, "a") as log_file:
            log_file.write(f"{score}\n")  # Write the score followed by a newline