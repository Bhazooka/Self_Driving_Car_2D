import pygame
import math
from simulation_settings import COLOUR_SETTINGS

class Sensor:
    def __init__(self, car, angle_offset, length):
        self.car = car
        self.end_x = 0  
        self.end_y = 0  
        self.angle_offset = angle_offset
        self.length = length
        self.distance = 0  # distance to the first obstacle
        self.is_on_road = False  

    def draw(self, window):
        # Draw the sensor line from the car to the sensor's endpoint
        pygame.draw.line(
            window,
            COLOUR_SETTINGS["GREEN"],
            (self.car.x, self.car.y),
            (self.end_x, self.end_y),
            2
        )
        # Draw the detected obstacle if any
        if self.distance != 0:
            angle_total = self.car.angle + self.angle_offset
            rad = math.radians(angle_total)
            obs_x = int(self.car.x + abs(self.distance) * math.cos(rad))
            obs_y = int(self.car.y - abs(self.distance) * math.sin(rad))
            obs_colour = COLOUR_SETTINGS["GREEN"]
            pygame.draw.circle(window, obs_colour, (obs_x, obs_y), 5)


    def make_sensor_distance(self, environment):
        angle_total = self.car.angle + self.angle_offset
        rad = math.radians(angle_total)
        found = False
        result = self.length if self.is_on_road else 0

        # Loop through the range of the sensor's length to check for obstacles
        for step in range(int(self.length)):
            px = int(self.car.x + step * math.cos(rad))
            py = int(self.car.y - step * math.sin(rad))

            # Ensure the check is within the environment's boundaries
            if not (0 <= px < environment.SCREEN_WIDTH and 0 <= py < environment.SCREEN_HEIGHT):
                continue
            pixel_colour = environment.TRACK_IMAGE.get_at((px, py))

            # If the car is on the road, detect the first non-road object
            if self.is_on_road:
                if pixel_colour not in (environment.ROAD_COLOUR, environment.CHECKPOINT_COLOUR, environment.START_COLOUR):
                    result = step
                    found = True
                    break
            # If the car is off-road, detect the distance to the road
            else:
                if pixel_colour in (environment.ROAD_COLOUR, environment.CHECKPOINT_COLOUR, environment.START_COLOUR):
                    result = -step
                    found = True
                    break
        return result

    def update(self, environment):
        # Calculate the sensor's direction in radians
        angle_total = self.car.angle + self.angle_offset
        rad = math.radians(angle_total)
        # Compute endpoint
        self.end_x = self.car.x + self.length * math.cos(rad)
        self.end_y = self.car.y - self.length * math.sin(rad)
        # Determine if the car is on the road
        self.is_on_road = self.car.is_on_road(self.car.x, self.car.y)
        # Update the measured distance
        self.distance = self.make_sensor_distance(environment)
