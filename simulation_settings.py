
CAR_SETTINGS = {
    "WIDTH": 25,
    "HEIGHT": 10,
    "MAX_SPEED": 1.5,  # Maximum speed on the track
    "MAX_SPEED_PARTIALLY_OFF": 0.2,  # Max speed when partially off the track
    "MAX_SPEED_COMPLETELY_OFF": 0.1,  # Max speed when completely off the track
    "ACCELERATION": 0.2,
    "DESACCELERATION": 0.95,  # Natural deceleration
    "ROTATION_SPEED": 5,  # Rotation speed
    "COLLISION_TYPE": "TRACK" # "WINDOW" or "TRACK"
}

QL_SETTINGS = {
    "LEARNING_RATE": 0.5,  # Alpha: learning rate for Q-learning updates
    "DISCOUNT_FACTOR": 0.95,  # Gamma: how much to discount future rewards
    "EXPLORATION_RATE": 1.0,  # Epsilon: initial exploration rate
    "EXPLORATION_DECAY": 0.995,  # How fast to decay epsilon over episodes
    "MIN_EXPLORATION_RATE": 0.1,  # Minimum exploration rate (to always explore a little)
    "Q_TABLE_FILENAME": "q_table.json"  # Agent 'knowledge' filename
}

SESSION_SETTINGS = {
    "TRAINING_MODE": True,    # Toggle between training and evaluation modes
    "NUM_EPISODES": 50,       # Number of episodes to run
    "EPISODE_DURATION": 10,   # Duration of each episode in seconds
    "MANUAL_CONTROL": False   # Enable manual control with arrow keys
}

WINDOW_SETTINGS = {
    "WIDTH": 900,
    "HEIGHT": 600,
}

COLOUR_SETTINGS = {
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "RED": (255, 0, 0),
    "GREY": (128, 128, 128),
    "YELLOW": (255, 255, 0),
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
}

# Font settings
FONT_SETTINGS = {
    "BIG": 36,  # Font size for larger text
    "MEDIUM": 24,  # Font size for medium text
    "SMALL": 20  # Font size for smaller text
}
