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

# Concentric Circles with Offset

center_x = width / 2
center_y = height / 2
max_radius = min(width, height) / 2 * 0.9  # Scale down to stay within bounds
num_circles = 40
radius_step = max_radius / num_circles
offset_amplitude = 20  # Maximum offset amount
line_width = 1

ctx.set_line_width(line_width)

for i in range(num_circles):
    radius = radius_step * (i + 1)
    offset_x = math.sin(i * 0.2) * offset_amplitude  # Sinusoidal offset for x
    offset_y = math.cos(i * 0.3) * offset_amplitude  # Cosinusoidal offset for y

    x = center_x + offset_x
    y = center_y + offset_y

    if i % 2 == 0:
        ctx.set_source_rgb(1, 1, 1)
    else:
        ctx.set_source_rgb(0.3, 0.3, 0.3)  # Slightly darker for contrast

    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.stroke()
