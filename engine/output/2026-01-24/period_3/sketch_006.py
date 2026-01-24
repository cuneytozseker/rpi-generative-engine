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

# Initial square parameters
x, y = 100, 100
size = 600
depth = 7 # Number of nested squares

# Color scheme
color1 = (1, 1, 1)  # White
color2 = (0.2, 0.2, 0.2) # Dark Gray

# Recursive function to draw nested squares
def draw_nested_squares(ctx, x, y, size, depth):
    if depth <= 0:
        return

    # Alternate colors
    if depth % 2 == 0:
        ctx.set_source_rgb(*color1)
    else:
        ctx.set_source_rgb(*color2)
    
    ctx.rectangle(x, y, size, size)
    ctx.fill()

    # Calculate new size and position using golden ratio
    new_size = size / phi
    new_x = x + (size - new_size) / 2
    new_y = y + (size - new_size) / 2

    # Recursive call
    draw_nested_squares(ctx, new_x, new_y, new_size, depth - 1)

# Draw the nested squares
draw_nested_squares(ctx, x, y, size, depth)
