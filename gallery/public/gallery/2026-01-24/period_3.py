import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # or your choice
ctx.paint()

# Concentric circles with systematic offset
center_x, center_y = width / 2, height / 2
num_circles = 20
max_radius = min(width, height) / 2 * 0.9  # Limit radius to fit within bounds
radius_increment = max_radius / num_circles
offset_increment = 5  # Adjust for visual effect

for i in range(num_circles):
    radius = radius_increment * (i + 1)
    offset_angle = math.radians(offset_increment * i) # Convert to radians

    x = center_x + math.cos(offset_angle) * (i*1.5) # Introduce x offset
    y = center_y + math.sin(offset_angle) * (i*1.5) # Introduce y offset

    ctx.set_source_rgb(1, 1, 1) # White
    ctx.set_line_width(2)
    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.stroke()
