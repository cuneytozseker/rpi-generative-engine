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

# Concentric Circles with Systematic Offset

center_x, center_y = width / 2, height / 2
num_circles = 30
max_radius = min(width, height) / 2 * 0.9  # Use 90% of available space
radius_increment = max_radius / num_circles

for i in range(num_circles):
    radius = radius_increment * (i + 1)
    offset_angle = (i * math.pi) / 10  # Progressive rotational offset
    offset_x = math.cos(offset_angle) * (radius * 0.1)  # Offset amount
    offset_y = math.sin(offset_angle) * (radius * 0.1)

    x = center_x + offset_x
    y = center_y + offset_y

    # Alternate between filled and stroked
    if i % 2 == 0:
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(x, y, radius, 0, 2 * math.pi)
        ctx.fill()
    else:
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(2)
        ctx.arc(x, y, radius, 0, 2 * math.pi)
        ctx.stroke()
