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
num_lines = 60
line_length = 200
x_center, y_center = width / 2, height / 2
rotation_increment = 360 / num_lines
offset_increment = 10

ctx.set_line_width(2)

for i in range(num_lines):
    angle = math.radians(i * rotation_increment)
    offset = i * offset_increment
    x1 = x_center + offset
    y1 = y_center
    x2 = x1 + line_length * math.cos(angle)
    y2 = y1 + line_length * math.sin(angle)

    ctx.set_source_rgb(1, 1, 1)  # White lines
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
