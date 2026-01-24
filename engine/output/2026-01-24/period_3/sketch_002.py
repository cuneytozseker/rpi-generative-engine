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

# Generative code: Parametric lines with rotation

num_lines = 50
line_length = 300
x_center, y_center = width / 2, height / 2
rotation_increment = 2 * math.pi / num_lines  # Full circle division
offset_x = 50
offset_y = 50

ctx.set_line_width(2)

for i in range(num_lines):
    angle = i * rotation_increment

    # Calculate start and end points of the line
    x1 = x_center + offset_x + line_length * math.cos(angle)
    y1 = y_center + offset_y + line_length * math.sin(angle)
    x2 = x_center - offset_x - line_length * math.cos(angle)
    y2 = y_center - offset_y - line_length * math.sin(angle)

    # Set color based on line index
    brightness = (i % 10) / 10 # Simple brightness variation
    ctx.set_source_rgb(brightness, brightness, brightness)

    # Draw the line
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

    offset_x += 0.1
    offset_y += 0.1

