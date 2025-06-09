import pygame
import pygame_menu
import os
import subprocess
import sys

from simulation_settings import SESSION_SETTINGS, QL_SETTINGS, CAR_SETTINGS

TRACKS_DIR = "tracks"
TRACKS = [f for f in os.listdir(TRACKS_DIR) if f.endswith('.png')]
selected_track = TRACKS[0] if TRACKS else None

def view_progress_graph():
    # Launch the plot_progress.py script in a new process
    python_exe = sys.executable
    script_path = os.path.join("log_plots", "plot_progress.py")
    subprocess.Popen([python_exe, script_path])

def set_episode_duration(value):
    SESSION_SETTINGS["EPISODE_DURATION"] = int(value)

def set_num_episodes(value):
    SESSION_SETTINGS["NUM_EPISODES"] = int(value)

def set_learning_rate(value):
    QL_SETTINGS["LEARNING_RATE"] = float(value)

def set_discount_factor(value):
    QL_SETTINGS["DISCOUNT_FACTOR"] = float(value)

def set_exploration_rate(value):
    QL_SETTINGS["EXPLORATION_RATE"] = float(value)

def set_exploration_decay(value):
    QL_SETTINGS["EXPLORATION_DECAY"] = float(value)

def set_min_exploration_rate(value):
    QL_SETTINGS["MIN_EXPLORATION_RATE"] = float(value)

def set_max_speed(value):
    CAR_SETTINGS["MAX_SPEED"] = float(value)

def set_acceleration(value):
    CAR_SETTINGS["ACCELERATION"] = float(value)

def set_deceleration(value):
    CAR_SETTINGS["DESACCELERATION"] = float(value)

def set_rotation_speed(value):
    CAR_SETTINGS["ROTATION_SPEED"] = float(value)

def set_manual_control(value):
    SESSION_SETTINGS["MANUAL_CONTROL"] = value

def set_track(selected, value):
    global selected_track
    selected_track = value

def settings_menu(menu, start_callback):
    menu.clear()
    menu.add.label('Settings', font_size=30)
    # Session settings
    menu.add.range_slider('Episode Duration', SESSION_SETTINGS["EPISODE_DURATION"], (5, 120), 1, onchange=set_episode_duration)
    menu.add.range_slider('Num Episodes', SESSION_SETTINGS["NUM_EPISODES"], (1, 500), 1, onchange=set_num_episodes)
    menu.add.toggle_switch('Manual Control', SESSION_SETTINGS["MANUAL_CONTROL"], onchange=set_manual_control, width=150)
    menu.add.vertical_margin(15)
    # Q-learning settings
    menu.add.label('Q-Learning Settings', font_size=24)
    menu.add.range_slider('Learning Rate', QL_SETTINGS["LEARNING_RATE"], (0.01, 1.0), 0.01, onchange=set_learning_rate)
    menu.add.range_slider('Discount Factor', QL_SETTINGS["DISCOUNT_FACTOR"], (0.5, 1.0), 0.01, onchange=set_discount_factor)
    menu.add.range_slider('Exploration Rate', QL_SETTINGS["EXPLORATION_RATE"], (0.0, 1.0), 0.01, onchange=set_exploration_rate)
    menu.add.range_slider('Exploration Decay', QL_SETTINGS["EXPLORATION_DECAY"], (0.90, 1.0), 0.0005, onchange=set_exploration_decay)
    menu.add.range_slider('Min Exploration Rate', QL_SETTINGS["MIN_EXPLORATION_RATE"], (0.0, 0.5), 0.01, onchange=set_min_exploration_rate)
    menu.add.vertical_margin(15)
    # Car settings
    menu.add.label('Car Settings', font_size=24)
    menu.add.range_slider('Max Speed', CAR_SETTINGS["MAX_SPEED"], (0.1, 5.0), 0.05, onchange=set_max_speed)
    menu.add.range_slider('Acceleration', CAR_SETTINGS["ACCELERATION"], (0.01, 1.0), 0.01, onchange=set_acceleration)
    menu.add.range_slider('Deceleration', CAR_SETTINGS["DESACCELERATION"], (0.80, 1.0), 0.01, onchange=set_deceleration)
    menu.add.range_slider('Rotation Speed', CAR_SETTINGS["ROTATION_SPEED"], (1, 20), 1, onchange=set_rotation_speed)
    menu.add.button('Back', lambda: main_menu(menu, start_callback))

def main_menu(menu, start_callback):
    menu.clear()
    menu.add.label('Self-Driving Car Simulator', font_size=40)
    menu.add.button('Start Simulation', lambda: start_callback(selected_track))
    menu.add.button('Settings', lambda: settings_menu(menu, start_callback))
    menu.add.selector('Select Track: ', [(t, t) for t in TRACKS], onchange=set_track)
    menu.add.button('View Progress Graph', view_progress_graph)
    menu.add.button('Quit', pygame_menu.events.EXIT)

def launch_menu(start_callback):
    pygame.init()
    surface = pygame.display.set_mode((600, 700))
    menu = pygame_menu.Menu('Main Menu', 600, 700, theme=pygame_menu.themes.THEME_DARK)
    main_menu(menu, start_callback)
    menu.mainloop(surface)