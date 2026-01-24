import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)
ctx.paint()

# Wave interference pattern
num_waves = 20
amplitude = 50
wavelength = 80
phase_shift_x = 0  # Varying phase shift for interesting effects
phase_shift_y = 0
wave_speed_x = 0.1  # Speed of wave movement
wave_speed_y = 0.1

ctx.set_line_width(2)

for i in range(num_waves):
    ctx.set_source_rgb(1, 1, 1)  # White lines
    ctx.move_to(0, height / num_waves * i)

    for x in range(width):
        y1 = amplitude * math.sin(2 * math.pi * x / wavelength + phase_shift_x + i * wave_speed_x) + height / num_waves * i
        y2 = amplitude * math.sin(2 * math.pi * x / wavelength + phase_shift_y + i * wave_speed_y) + height / num_waves * i

        # Average the two waves to create interference
        y = (y1 + y2) / 2
        ctx.line_to(x, y)

    ctx.stroke()
