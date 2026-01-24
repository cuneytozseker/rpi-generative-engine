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

# Generative Code
num_lines = 36
line_length = 300
x_center, y_center = width / 2, height / 2
rotation_increment = 360 / num_lines
line_width = 3

ctx.set_line_width(line_width)

for i in range(num_lines):
    angle = math.radians(i * rotation_increment)
    x1 = x_center + line_length * math.cos(angle)
    y1 = y_center + line_length * math.sin(angle)
    x2 = x_center - line_length * math.cos(angle)
    y2 = y_center - line_length * math.sin(angle)

    # Alternate colors for visual interest
    if i % 2 == 0:
        ctx.set_source_rgb(1, 1, 1) # White
    else:
        ctx.set_source_rgb(0.8, 0.8, 0.8)  # Light Gray

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
