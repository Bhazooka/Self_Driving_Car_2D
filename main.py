import os
import pygame
import subprocess
import sys
from simulation_settings import SESSION_SETTINGS
from simulation.car import Car
from simulation.environment import Environment
from q_learning_implementation.agent import QLearningAgent
from q_learning_logs.logger import Logger
from user_interface import launch_menu

def run_episode(environment, car, agent, manual_control):
    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    window_closed = False
    restart_episode = False
    end_simulation = False

    while True:
        clock.tick(240) # FPS
        environment.clear_screen()

        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, SESSION_SETTINGS["EPISODE_DURATION"] - elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                window_closed = True
                return car.score, window_closed, end_simulation, restart_episode
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # End simulation
                    end_simulation = True
                    return car.score, window_closed, end_simulation, restart_episode
                if event.key == pygame.K_r:  # Restart episode
                    restart_episode = True
                    return car.score, window_closed, end_simulation, restart_episode

        if time_left <= 0:
            break

        environment.draw_track()

        if manual_control:
            car.handle_manual_input()
            car.calculate_reward()
        else:
            state = car.get_state()
            action = agent.get_action(state, use_epsilon=SESSION_SETTINGS["TRAINING_MODE"])
            car.handle_agent_action(action)
            reward = car.calculate_reward()
            next_state = car.get_state()
            if SESSION_SETTINGS["TRAINING_MODE"]:
                agent.update_q_value(state, action, round(reward, 1), next_state)
                agent.decay_exploration()

        if car.collided:
            break

        car.draw(environment.window)
        environment.draw_text(car, time_left)
        pygame.display.flip()

    return car.score, window_closed, end_simulation, restart_episode


def start_simulation(selected_track):
    # You can use selected_track to load the correct track in your Environment class
    print(f"Starting simulation with track: {selected_track}")
    pygame.display.quit()  # Close the menu window before starting simulation
    pygame.display.init()
    environment = Environment(selected_track)  # Pass selected_track to Environment
    car = Car(environment)
    state_size, action_size = 9, 4
    agent = QLearningAgent(state_size, action_size)

    # Load Q-table based on mode
    q_loaded = agent.load_q_table()
    if SESSION_SETTINGS["TRAINING_MODE"]:
        if q_loaded:
            print(f"Training mode: Q-table loaded from {agent.q_table_path}")
        else:
            print("Training mode: No previous Q-table found. Starting fresh.")
    else:
        if q_loaded:
            print(f"Evaluation mode: Using saved Q-table from {agent.q_table_path}")
        else:
            print("Warning: No Q-table found for evaluation mode!")
            pygame.quit()
            return

    q_table_filename = os.path.basename(agent.q_table_path)
    log_filename = q_table_filename.replace(".json", ".txt")
    logger = Logger(log_filename)

    num_episodes = 1 if SESSION_SETTINGS["MANUAL_CONTROL"] else SESSION_SETTINGS["NUM_EPISODES"]

    episode = 0
    while episode < num_episodes:
        print(f"Starting episode {episode + 1}/{num_episodes}")
        car.reset()
        score, window_closed, end_simulation, restart_episode = run_episode(
            environment, car, agent, SESSION_SETTINGS["MANUAL_CONTROL"]
        )

        if window_closed:
            print("Window closed. Ending session.")
            break

        if end_simulation:
            print("Simulation ended by user. Displaying progress graph...")
            # Launch the plot_progress.py script in a new process
            python_exe = sys.executable
            script_path = os.path.join("log_plots", "plot_progress.py")
            subprocess.Popen([python_exe, script_path])
            break

        if restart_episode:
            print("Restarting episode by user request.")
            continue  # Do not increment episode, just restart

        if not SESSION_SETTINGS["MANUAL_CONTROL"] and SESSION_SETTINGS["TRAINING_MODE"]:
            agent.save_q_table()
            logger.log_score(score)

        mode = "Training" if SESSION_SETTINGS["TRAINING_MODE"] else "Evaluation"
        print(f"{mode} episode {episode + 1} completed. Score: {score}")

        episode += 1

    pygame.quit()


def main():
    launch_menu(start_simulation)

if __name__ == "__main__":
    main()