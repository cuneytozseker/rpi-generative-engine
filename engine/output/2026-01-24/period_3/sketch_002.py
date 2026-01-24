import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # Black background
ctx.paint()

# Generative Code: Parametric Line Pattern with Rotation

num_lines = 50
line_length = 200
center_x, center_y = width / 2, height / 2
rotation_increment = 2 * math.pi / num_lines  # Full circle divided by num_lines
offset_increment = 5

ctx.set_line_width(1)
ctx.set_source_rgb(1, 1, 1) # White lines

for i in range(num_lines):
    angle = i * rotation_increment
    offset_x = math.cos(angle) * offset_increment * i
    offset_y = math.sin(angle) * offset_increment * i

    x1 = center_x + offset_x
    y1 = center_y + offset_y

    x2 = x1 + line_length * math.cos(angle)
    y2 = y1 + line_length * math.sin(angle)

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
