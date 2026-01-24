import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # Black background
ctx.paint()

# Generative Code: Wave Interference

num_waves = 20
amplitude = 50
wavelength_range = (50, 150)
phase_shift_increment = 0.1
line_width = 2

ctx.set_line_width(line_width)

for i in range(num_waves):
    wavelength = random.uniform(wavelength_range[0], wavelength_range[1])
    phase_shift = i * phase_shift_increment
    ctx.set_source_rgb(1, 1, 1)  # White lines

    for x in range(width):
        y = height / 2 + amplitude * math.sin(2 * math.pi * x / wavelength + phase_shift)
        if x == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

    ctx.stroke()

    # Shift the center to create a displacement effect
    vertical_shift = i * 5  # Control the amount of displacement
    ctx.translate(0, vertical_shift)  # Apply the shift temporarily

    # reset to original position
    ctx.translate(0, -vertical_shift)
