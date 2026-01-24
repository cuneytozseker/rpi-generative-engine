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
max_radius = min(width, height) / 2 * 0.9  # 90% of the possible radius
radius_increment = max_radius / num_circles
offset_angle_increment = 2 * math.pi / num_circles  # Full circle divided equally

for i in range(num_circles):
    radius = radius_increment * (i + 1)
    offset_angle = offset_angle_increment * i

    x = center_x + radius * math.cos(offset_angle) - center_x
    y = center_y + radius * math.sin(offset_angle) - center_y

    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)

    gray_value = (i / num_circles) * 0.7 + 0.3 # Gray values from 0.3 to 1.0
    ctx.set_source_rgb(gray_value, gray_value, gray_value)
    ctx.set_line_width(2)
    ctx.stroke()
