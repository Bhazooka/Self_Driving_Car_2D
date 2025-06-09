import math
import time
import pygame
from simulation.sensor import Sensor
from simulation.checkpoint import Checkpoint
from simulation_settings import CAR_SETTINGS

class Car:
    def __init__(self, environment):
        self.environment = environment
        self._initialize_starting_state()
        self._load_car_settings()
        self.image = self.make_car()
        self.sensors = self.make_sensors()
        self.reset()

    def _initialize_starting_state(self):
        start_info = self.environment.find_start_position()
        if not start_info:
            raise RuntimeError("No valid starting position found on the track.")
        self.initial_position = tuple(start_info[:2])
        self.initial_angle = self.normalize_angle(start_info[2])

    def _load_car_settings(self):
        settings = CAR_SETTINGS
        self.width = settings.get("WIDTH", 40)
        self.height = settings.get("HEIGHT", 20)
        self.max_speed = settings.get("MAX_SPEED", 10)
        self.max_speed_partially_off = settings.get("MAX_SPEED_PARTIALLY_OFF", 5)
        self.max_speed_completely_off = settings.get("MAX_SPEED_COMPLETELY_OFF", 2)
        self.acceleration = settings.get("ACCELERATION", 0.2)
        self.deceleration = settings.get("DESACCELERATION", 0.95)
        self.rotation_speed = settings.get("ROTATION_SPEED", 5)

    def reset(self):
        self.x, self.y = self.initial_position[0], self.initial_position[1]
        self.angle = self.initial_angle
        self.speed = 0
        self.score = 0
        self.collided = False
        self.last_checkpoint = None
        now = time.time()
        self.last_road_check_time = now
        self.last_speed_check_time = now

    def make_car(self):
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        colour = getattr(self.environment, "CAR_COLOUR", (100, 140, 200))
        surf.fill(colour)
        return surf

    def make_sensors(self):
        sensor_specs = [
                    (-135, 100),  # back-left
                    (-90, 100),   # left
                    (-45, 150),   # front-left
                    (0, 200),     # front
                    (45, 150),    # front-right
                    (90, 100),    # right
                    (135, 100),   # back-right
                    (180, 80),    # back
        ]
        return [Sensor(self, angle, length) for angle, length in sensor_specs]

    def draw(self, window):
        # Draw the circular sensor field first (so the car is on top)
        self.draw_sensor_radius(window, radius=120, color=(255, 0, 0, 60))  # 60 is alpha for transparency

        # Draw a dark red flash where any sensor detects a wall
        for sensor in self.sensors:
            if 0 < sensor.distance < sensor.length:  # Detected wall within range
                angle_total = self.angle + sensor.angle_offset
                rad = math.radians(angle_total)
                obs_x = int(self.x + abs(sensor.distance) * math.cos(rad))
                obs_y = int(self.y - abs(sensor.distance) * math.sin(rad))
                pygame.draw.circle(window, (120, 0, 0), (obs_x, obs_y), 5)  # Dark red, radius 10

        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        window.blit(rotated, rect.topleft)
        # Optionally, comment out the line sensors if you only want the circle:
        # for sensor in self.sensors:
        #     sensor.draw(window)

    def draw_sensor_radius(self, window, radius=120, color=(255, 0, 0, 60)):
        """
        Draw a semi-transparent circular sensor field around the car.
        :param window: The pygame surface to draw on.
        :param radius: The radius of the sensor field.
        :param color: RGBA tuple for the sensor color (red, semi-transparent).
        """
        # Create a transparent surface
        sensor_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(sensor_surface, color, (radius, radius), radius)
        # Blit the sensor surface centered on the car
        window.blit(sensor_surface, (self.x - radius, self.y - radius))

    def get_state(self):
        state = [int(self.speed)]
        state.extend(int(sensor.distance / 10) for sensor in self.sensors)
        return tuple(state)

    def normalize_angle(self, angle):
        """Normalize the angle to be between 0 and 359."""
        return angle % 360

    def update_angle(self, delta):
        """Update the car's angle."""
        self.angle = self.normalize_angle(self.angle + delta)

    def discretize_angle(self, angle):
        """Discretize the angle into 8 directions."""
        return int(angle // 45)

    def handle_manual_input(self):
        """Handle manual input for the car."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.accelerate()
        else:
            self.decelerate()
        
        if keys[pygame.K_LEFT]:
            self.rotate(self.rotation_speed)
        elif keys[pygame.K_RIGHT]:
            self.rotate(-self.rotation_speed)
        
        self.update()

    def handle_agent_action(self, action):
        """Handle agent's action for the car."""
        if action == 0:
            self.accelerate()
        elif action == 1:
            self.rotate(self.rotation_speed)
        elif action == 2:
            self.rotate(-self.rotation_speed)
        else:
            self.decelerate()
        
        self.update()

    def update(self):
        self.update_position()
        self.update_sensors()
        self.check_collision(check_type="TRACK")

    def accelerate(self):
        """Accelerate the car."""
        self.speed = min(self.speed + self.acceleration, self.max_speed)

    def decelerate(self):
        """Decelerate the car."""
        self.speed *= self.deceleration

    def rotate(self, rotation):
        """Rotate the car."""
        if self.max_speed != 0:
            self.update_angle(rotation * (self.speed / self.max_speed))

    def update_position(self):
        """Update the car's position based on its speed and angle."""
        rad_angle = math.radians(self.angle)
        new_x = self.x + self.speed * math.cos(rad_angle)
        new_y = self.y - self.speed * math.sin(rad_angle)
        
        road_status = self.check_road_status(new_x, new_y)
        self.adjust_speed_and_position(road_status, new_x, new_y)

    def adjust_speed_and_position(self, road_status, new_x, new_y):
        """Adjust the car's speed and position based on its road status."""
        if road_status == "on_road":
            self.max_speed = CAR_SETTINGS.get("MAX_SPEED", 10)
        elif road_status == "partially_off":
            self.max_speed = self.max_speed_partially_off
        else:
            self.max_speed = self.max_speed_completely_off

        self.speed = min(self.speed, self.max_speed)
        self.x, self.y = new_x, new_y

    def check_collision(self, check_type="TRACK"):
        """Check if the car has collided with the boundaries or left the track."""
        if check_type == "WINDOW":
            half_w, half_h = self.width / 2, self.height / 2
            self.collided = not (
                half_w < self.x < self.environment.SCREEN_WIDTH - half_w and
                half_h < self.y < self.environment.SCREEN_HEIGHT - half_h
            )
        elif check_type == "TRACK":
            self.collided = self.check_road_status(self.x, self.y) == "completely_off"

    def check_road_status(self, x, y):
        """Check the road status at the given position."""
        rotated_rect = self.get_rotated_vertices(pygame.Rect(x - self.width / 2, y - self.height / 2, self.width, self.height))
        on_road_count = sum(1 for vertex in rotated_rect if self.is_on_road(*vertex))
        
        if on_road_count == len(rotated_rect):
            return "on_road"
        elif on_road_count > 0:
            return "partially_off"
        return "completely_off"

    def get_rotated_vertices(self, rect):
        """Get the rotated vertices of the car's rectangle."""
        rad_angle = math.radians(self.angle)
        cx, cy = rect.center
        corners = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        return [(cx + (x - cx) * math.cos(rad_angle) - (y - cy) * math.sin(rad_angle),
                cy + (x - cx) * math.sin(rad_angle) + (y - cy) * math.cos(rad_angle))
                for x, y in corners]

    def is_on_road(self, x, y):
        """Check if the given position is on the road."""
        if 0 <= x < self.environment.SCREEN_WIDTH and 0 <= y < self.environment.SCREEN_HEIGHT:
            colour_at_position = self.environment.TRACK_IMAGE.get_at((int(x), int(y)))
            return colour_at_position in [self.environment.ROAD_COLOUR, 
                                          self.environment.CHECKPOINT_COLOUR, 
                                          self.environment.START_COLOUR]
        return False

    def update_sensors(self):
        """Update the car's sensors."""
        for sensor in self.sensors:
            sensor.update(self.environment)

    def update_score(self, delta):
        """Update the car's score."""
        self.score = round(self.score + delta, 1)

    def check_checkpoint(self, current_time, checkpoints):
        """Check if the car has reached a checkpoint."""
        radius = 2
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx * dx + dy * dy <= radius * radius:
                    check_x, check_y = int(self.x + dx), int(self.y + dy)
                    if self.is_valid_position(check_x, check_y):
                        colour_at_position = self.environment.TRACK_IMAGE.get_at((check_x, check_y))
                        if colour_at_position == self.environment.CHECKPOINT_COLOUR:
                            position = (check_x, check_y)
                            if position == self.last_checkpoint:
                                return 0
                            if position in checkpoints:
                                checkpoint = checkpoints[position]
                                if checkpoint.is_active(current_time):
                                    checkpoint.last_crossed = current_time
                                    self.last_checkpoint = position
                                    return 10
                            else:
                                checkpoints[position] = Checkpoint(position)
                                checkpoints[position].last_crossed = current_time
                                self.last_checkpoint = position
                                return 10
        return 0

    def is_valid_position(self, x, y):
        """Check if the given position is within the screen boundaries."""
        return 0 <= x < self.environment.SCREEN_WIDTH and 0 <= y < self.environment.SCREEN_HEIGHT

    def reward_road(self):
        """Calculate the reward based on the car's position on the road."""
        current_time = time.time()
        if current_time - self.last_road_check_time >= 0.25:
            road_status = self.check_road_status(self.x, self.y)
            self.last_road_check_time = current_time
            
            if road_status == "on_road":
                return 0.5
            return -0.5 if road_status == "partially_off" else -1
        return 0

    def reward_speed(self):
        """Calculate the reward based on the car's speed."""
        return round(self.speed / 6, 1)

    def reward_distance(self):
        """
        Reward the agent for maintaining distance from the track edges.
        Focuses on lateral sensors (indices 0, 1, 3, 4).
        """
        lateral_sensors = [self.sensors[i] for i in [0, 1, 3, 4]]
        min_distance = min(sensor.distance for sensor in lateral_sensors)
        reward = min_distance / 100
        return round(reward, 1)

    def calculate_reward(self):
        """Calculate the total reward for the car's current state."""
        total_reward = 0
        total_reward += round(self.reward_speed() * self.reward_distance(), 1)
        if self.collided:
            total_reward -= 25
        self.update_score(total_reward)
        return total_reward