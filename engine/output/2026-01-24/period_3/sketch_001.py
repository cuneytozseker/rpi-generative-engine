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

# Concentric circles with offset

center_x, center_y = width / 2, height / 2
num_circles = 20
max_radius = min(width, height) / 2 * 0.9
radius_increment = max_radius / num_circles
offset_increment = 5 # Fixed pixel offset

for i in range(num_circles):
    radius = radius_increment * (i + 1)
    offset_x = offset_increment * (i % 4 - 1.5)  # Cycle between -1.5, -0.5, 0.5, 1.5
    offset_y = offset_increment * ((i + 2) % 4 - 1.5)  # Shifted offset pattern

    x = center_x + offset_x
    y = center_y + offset_y
    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.set_line_width(2)

    # Alternate fill and stroke
    if i % 2 == 0:
        ctx.set_source_rgb(1, 1, 1)
        ctx.stroke()
    else:
        ctx.set_source_rgb(0.8, 0.8, 0.8) # Slightly darker fill
        ctx.fill()
