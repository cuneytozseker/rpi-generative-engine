import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.paint()

# Generative Code
num_lines = 60
line_length = 250
center_x, center_y = width / 2, height / 2
angle_increment = 2 * math.pi / num_lines
rotation_increment = 0.01  # Gradual rotation

for i in range(num_lines):
    angle = i * angle_increment
    rotation = i * rotation_increment # Apply incremental rotation
    x1 = center_x + math.cos(angle + rotation) * 50 #Small offset
    y1 = center_y + math.sin(angle + rotation) * 50
    x2 = x1 + math.cos(angle + rotation) * line_length
    y2 = y1 + math.sin(angle + rotation) * line_length

    # Alternate line colors and thicknesses based on line number
    if i % 2 == 0:
      ctx.set_source_rgb(0.1, 0.1, 0.1)
      ctx.set_line_width(1.5)
    else:
      ctx.set_source_rgb(0.25, 0.25, 0.25)
      ctx.set_line_width(0.75)

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
