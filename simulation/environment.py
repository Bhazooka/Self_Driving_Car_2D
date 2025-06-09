import os
import pygame
import math
from simulation_settings import WINDOW_SETTINGS, COLOUR_SETTINGS, FONT_SETTINGS


from simulation.draw_text import (
    draw_score, draw_timer, draw_speed, draw_sensor_values, draw_car_status
)

class Environment:
    def __init__(self, track_filename=None):
        self._init_screen_settings()
        self._init_colours()
        self._init_fonts()
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Simulation")
        self.TRACK_IMAGE = self._load_track_image(track_filename)

    def _load_track_image(self, track_filename):
        project_root = os.path.dirname(os.path.abspath(__file__))
        tracks_dir = os.path.join(project_root, "..", "tracks")
        if track_filename is not None:
            img_path = os.path.join(tracks_dir, track_filename)
        else:
            img_path = os.path.join(tracks_dir, "track_3.png")
        img_path = os.path.normpath(img_path)
        return pygame.transform.scale(
            pygame.image.load(img_path).convert(),
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        )

    def _init_screen_settings(self):
        self.SCREEN_WIDTH = WINDOW_SETTINGS["WIDTH"]
        self.SCREEN_HEIGHT = WINDOW_SETTINGS["HEIGHT"]

    def _init_colours(self):
        self.ROAD_COLOUR = COLOUR_SETTINGS["BLACK"]
        self.BACKGROUND_COLOUR = COLOUR_SETTINGS["WHITE"]
        self.CAR_COLOUR = COLOUR_SETTINGS["RED"]
        self.SENSOR_COLOUR = COLOUR_SETTINGS["GREEN"]
        self.START_COLOUR = COLOUR_SETTINGS["YELLOW"]
        self.CHECKPOINT_COLOUR = COLOUR_SETTINGS["GREY"]
        self.TEXT_COLOUR = COLOUR_SETTINGS["WHITE"]
        self.TEXTBOX_COLOUR = (72, 72, 72)

    def _init_fonts(self):
        pygame.init()
        pygame.font.init()
        self.FONT_BIG = pygame.font.Font(None, FONT_SETTINGS["BIG"])
        self.FONT_SMALL = pygame.font.Font(None, FONT_SETTINGS["SMALL"])

    def find_start_position(self):
        width, height = self.TRACK_IMAGE.get_width(), self.TRACK_IMAGE.get_height()
        for y in range(height):
            for x in range(width):
                if self.TRACK_IMAGE.get_at((x, y)) == self.START_COLOUR:
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            if self.TRACK_IMAGE.get_at((nx, ny)) == self.ROAD_COLOUR:
                                angle = math.degrees(math.atan2(-dy, dx))
                                return x, y, angle
        return None

    def draw_track(self):
        self.window.blit(self.TRACK_IMAGE, (0, 0))

    def clear_screen(self):
        rect = pygame.Rect(0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.window.fill(self.BACKGROUND_COLOUR, rect)

    def draw_text(self, car, remaining_time):
        draw_score(self.window, self.FONT_SMALL, self.TEXTBOX_COLOUR, self.TEXT_COLOUR, car.score)
        draw_timer(self.window, self.FONT_SMALL, self.TEXTBOX_COLOUR, self.TEXT_COLOUR, remaining_time, self.SCREEN_WIDTH)
        draw_speed(self.window, self.FONT_SMALL, self.TEXTBOX_COLOUR, self.TEXT_COLOUR, car.speed, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        draw_sensor_values(self.window, self.FONT_SMALL, self.TEXTBOX_COLOUR, self.TEXT_COLOUR, car.sensors, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        on_track = car.check_road_status(car.x, car.y) != "completely_off"
        draw_car_status(self.window, self.FONT_SMALL, self.TEXTBOX_COLOUR, self.TEXT_COLOUR, on_track, car.angle, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        font = pygame.font.SysFont(None, 24)
        controls = font.render("[E]:End Simulation | [R]:Restart Episode", True, (128,128,128))
        self.window.blit(controls, (10, self.SCREEN_HEIGHT - 30))
