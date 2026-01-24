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

# Golden ratio
phi = (1 + math.sqrt(5)) / 2

# Initial square
x, y = 100, 100
side = 600
ctx.set_line_width(2)

def draw_nested_squares(ctx, x, y, side, depth):
    if depth == 0:
        return

    # Draw the current square
    ctx.set_source_rgb(1, 1, 1) # White lines
    ctx.rectangle(x, y, side, side)
    ctx.stroke()

    # Calculate the dimensions and position of the next square
    new_side = side / phi
    new_x = x + (side - new_side) / 2
    new_y = y + (side - new_side) / 2

    # Recursively draw the next square
    draw_nested_squares(ctx, new_x, new_y, new_side, depth - 1)


# Draw the nested squares
draw_nested_squares(ctx, x, y, side, 10)  # Depth controls number of squares
