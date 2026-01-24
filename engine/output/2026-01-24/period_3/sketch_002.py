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
num_lines = 100
line_length = 200
x_center = width / 2
y_center = height / 2
angle_increment = 2 * math.pi / num_lines

ctx.set_line_width(2)

for i in range(num_lines):
    angle = i * angle_increment
    x1 = x_center + line_length * math.cos(angle)
    y1 = y_center + line_length * math.sin(angle)
    x2 = x_center - line_length * math.cos(angle)
    y2 = y_center - line_length * math.sin(angle)

    # Vary color based on line index
    color_value = (i % 50) / 50  # Cycle through greyscale
    ctx.set_source_rgb(color_value, color_value, color_value)

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
