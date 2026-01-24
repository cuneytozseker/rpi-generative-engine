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

# Golden Ratio
phi = (1 + math.sqrt(5)) / 2

# Initial square
size = width * 0.6
x = (width - size) / 2
y = (height - size) / 2

# Number of iterations
iterations = 7

# Function to draw nested squares
def draw_nested_squares(ctx, x, y, size, iterations):
    if iterations == 0:
        return

    ctx.set_source_rgb(1, 1, 1)  # White lines
    ctx.set_line_width(2)
    ctx.rectangle(x, y, size, size)
    ctx.stroke()

    new_size = size / phi
    new_x = x + (size - new_size) / 2
    new_y = y + (size - new_size) / 2

    draw_nested_squares(ctx, new_x, new_y, new_size, iterations - 1)

# Draw the nested squares
draw_nested_squares(ctx, x, y, size, iterations)
