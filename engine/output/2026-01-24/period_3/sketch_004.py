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

# Generative Code: Wave Interference

num_waves = 15
amplitude = 50
wavelength = 100
phase_shift_increment = 0.2
line_width = 2

ctx.set_line_width(line_width)
ctx.set_source_rgb(1, 1, 1)

for i in range(num_waves):
    phase_shift = i * phase_shift_increment
    for x in range(0, width):
        y = height / 2 + amplitude * math.sin(2 * math.pi * x / wavelength + phase_shift)
        if x == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

    # Invert color for every other wave for higher contrast
    if i % 2 == 0:
        ctx.set_source_rgb(1, 1, 1)
    else:
         ctx.set_source_rgb(0, 0, 0) # or another contrasting color
