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

# Golden Ratio
phi = (1 + math.sqrt(5)) / 2

# Initial square size
side = 600
x = (width - side) / 2
y = (height - side) / 2

# Number of iterations
iterations = 8

# Colors
color_bg = (0, 0, 0)
color_fg = (1, 1, 1)

ctx.set_line_width(2)


def draw_nested_squares(ctx, x, y, side, iterations, depth=0):
    if depth >= iterations:
        return

    # Current square
    ctx.set_source_rgb(*color_fg)
    ctx.rectangle(x, y, side, side)
    ctx.stroke()

    # Calculate inner square size and position based on golden ratio
    inner_side = side / phi
    inner_x = x + (side - inner_side) / 2
    inner_y = y + (side - inner_side) / 2

    # Recursive call
    draw_nested_squares(ctx, inner_x, inner_y, inner_side, iterations, depth + 1)

# Start drawing
draw_nested_squares(ctx, x, y, side, iterations)
