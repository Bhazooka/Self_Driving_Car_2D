import pygame

# Try to use a modern, readable font
def get_font(size, bold=False):
    try:
        return pygame.font.SysFont("segoeui", size, bold=bold)
    except:
        return pygame.font.Font(None, size)

def draw_shadowed_text(window, text, font, pos, text_colour, shadow_colour=(0,0,0), shadow_offset=(2,2)):
    # Draw shadow
    shadow = font.render(text, True, shadow_colour)
    window.blit(shadow, (pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]))
    # Draw main text
    surf = font.render(text, True, text_colour)
    window.blit(surf, pos)

def draw_score(window, font_big, textbox_colour, text_colour, car_score):
    font = get_font(font_big.get_height(), bold=True)
    text = f"Score: {car_score}"
    rect = font.render(text, True, text_colour).get_rect(topleft=(20, 20))
    pygame.draw.rect(window, textbox_colour, rect.inflate(18, 18).move(-9, -9), border_radius=8)
    draw_shadowed_text(window, text, font, rect.topleft, text_colour)

def draw_timer(window, font_big, textbox_colour, text_colour, remaining_time, screen_width):
    font = get_font(font_big.get_height(), bold=True)
    text = f"Time: {remaining_time:.1f}"
    rect = font.render(text, True, text_colour).get_rect(topright=(screen_width - 20, 20))
    # pygame.draw.rect(window, textbox_colour, rect.inflate(18, 18).move(-9, -9), border_radius=8)
    # draw_shadowed_text(window, text, font, rect.topleft, text_colour)

def draw_speed(window, font_big, textbox_colour, text_colour, car_speed, screen_width, screen_height):
    font = get_font(font_big.get_height(), bold=True)
    text = f"Speed: {car_speed:.1f}"
    rect = font.render(text, True, text_colour).get_rect(bottomright=(screen_width - 20, screen_height - 20))
    pygame.draw.rect(window, textbox_colour, rect.inflate(18, 18).move(-9, -9), border_radius=8)
    draw_shadowed_text(window, text, font, rect.topleft, text_colour)

def draw_sensor_values(window, font_small, textbox_colour, text_colour, car_sensors, screen_width, screen_height):
    font = get_font(font_small.get_height())
    base_x = screen_width - 20
    base_y = screen_height - 80
    for idx, sensor in enumerate(reversed(car_sensors)):
        label = f"Sensor {len(car_sensors) - idx}: {sensor.distance:.1f}"
        surf = font.render(label, True, text_colour)
        rect = surf.get_rect(bottomright=(base_x, base_y - idx * 28))
        pygame.draw.rect(window, textbox_colour, rect.inflate(14, 14).move(-7, -7), border_radius=6)
        draw_shadowed_text(window, label, font, rect.topleft, text_colour)

def draw_car_status(window, font_small, textbox_colour, text_colour, is_on_track, car_angle, screen_width, screen_height):
    font = get_font(font_small.get_height())
    base_x = screen_width - 20
    base_y = screen_height - 250
    status = None #"On Track: Yes" if is_on_track else "On Track: No"
    angle = None # f"Angle: {car_angle:.1f}°"
    status_surf = font.render(status, True, text_colour)
    status_rect = status_surf.get_rect(bottomright=(base_x, base_y))
    pygame.draw.rect(window, textbox_colour, status_rect.inflate(14, 14).move(-7, -7), border_radius=6)
    draw_shadowed_text(window, status, font, status_rect.topleft, text_colour)

    angle_surf = font.render(angle, True, text_colour)
    angle_rect = angle_surf.get_rect(bottomright=(base_x, base_y + 30))
    pygame.draw.rect(window, textbox_colour, angle_rect.inflate(14, 14).move(-7, -7), border_radius=6)
    draw_shadowed_text(window, angle, font, angle_rect.topleft, text_colour)