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

# Golden Ratio
phi = (1 + math.sqrt(5)) / 2

# Starting square
x, y = 100, 100
size = 600
ctx.set_line_width(2)

# Number of iterations
iterations = 7

def draw_nested_squares(ctx, x, y, size, iterations):
    if iterations == 0:
        return

    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(x, y, size, size)
    ctx.stroke()

    new_size = size / phi
    new_x = x + (size - new_size) / 2
    new_y = y + (size - new_size) / 2

    draw_nested_squares(ctx, new_x, new_y, new_size, iterations - 1)

draw_nested_squares(ctx, x, y, size, iterations)
