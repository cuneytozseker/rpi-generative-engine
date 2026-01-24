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

# Initial square
x, y = 100, 100
size = 600
num_iterations = 7

ctx.set_line_width(2)

for i in range(num_iterations):
    # Draw the square
    ctx.set_source_rgb(1, 1, 1) # White squares
    ctx.rectangle(x, y, size, size)
    ctx.stroke()

    # Calculate the new square dimensions and position using the golden ratio
    new_size = size / phi
    new_x = x + (size - new_size) / 2
    new_y = y + (size - new_size) / 2

    # Update variables for the next iteration
    x, y = new_x, new_y
    size = new_size
