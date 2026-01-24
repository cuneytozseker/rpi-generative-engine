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

# Wave parameters
num_waves = 10
amplitude = 50
wavelength_min = 50
wavelength_max = 200
phase_shift_x = 0
phase_shift_y = 0

# Drawing waves
ctx.set_source_rgb(1, 1, 1)  # White lines
ctx.set_line_width(2)

for i in range(num_waves):
    wavelength = random.uniform(wavelength_min, wavelength_max)
    phase_shift_x = random.uniform(0, 2*math.pi) # Introduce some variety in the phases.
    phase_shift_y = random.uniform(0, 2*math.pi)

    # Horizontal Waves
    ctx.move_to(0, i * (height / num_waves))
    for x in range(width):
        y = i * (height / num_waves) + amplitude * math.sin(2 * math.pi * x / wavelength + phase_shift_x)
        ctx.line_to(x, y)
    ctx.stroke()

    # Vertical Waves - more subtle
    ctx.move_to(i * (width/num_waves), 0)
    for y in range(height):
        x = i*(width/num_waves) + amplitude * 0.5 * math.sin(2 * math.pi * y/wavelength + phase_shift_y)  # Lower amplitude
        ctx.line_to(x, y)
    ctx.stroke()
