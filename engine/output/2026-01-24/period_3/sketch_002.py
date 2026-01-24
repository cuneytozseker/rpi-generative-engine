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
num_lines = 40
line_length = 300
x_center, y_center = width / 2, height / 2
rotation_increment = 360 / num_lines
line_width = 2

ctx.set_line_width(line_width)

for i in range(num_lines):
    angle = math.radians(i * rotation_increment)
    x1 = x_center + line_length * math.cos(angle)
    y1 = y_center + line_length * math.sin(angle)
    x2 = x_center - line_length * math.cos(angle)
    y2 = y_center - line_length * math.sin(angle)

    # Vary color slightly based on index for subtle effect
    color_intensity = 0.5 + 0.5 * math.sin(i * 0.2) # Oscillate between 0.5 and 1.0
    ctx.set_source_rgb(color_intensity, color_intensity, color_intensity)

    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

