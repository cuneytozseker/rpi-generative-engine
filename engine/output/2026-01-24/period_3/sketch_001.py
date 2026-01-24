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

# Concentric circles with systematic offset
center_x, center_y = width / 2, height / 2
num_circles = 50
max_radius = min(width, height) / 2 * 0.9
radius_step = max_radius / num_circles
offset_factor = 0.1 # Adjust for visual balance

for i in range(num_circles):
    radius = radius_step * (i + 1)
    offset = radius * offset_factor

    # Alternate offset direction
    if i % 2 == 0:
        x = center_x + offset
        y = center_y + offset
    else:
        x = center_x - offset
        y = center_y - offset

    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.set_line_width(2)
    ctx.set_source_rgb(1, 1, 1)  # White lines
    ctx.stroke()
