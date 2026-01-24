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
x, y = 50, 50
size = 700
min_size = 5

# Iteration parameters
num_iterations = 12
scale_factor = 1 / phi
line_width_reduction = 0.8  # Reduce line width on each iteration

# Colors
base_color = (1, 1, 1)  # White
highlight_color = (0.2, 0.2, 0.2) # Dark gray

ctx.set_source_rgb(*base_color)
ctx.set_line_width(5)

for i in range(num_iterations):
    ctx.rectangle(x, y, size, size)
    ctx.stroke()

    # Calculate next square parameters based on golden ratio
    new_size = size * scale_factor
    new_x = x + (size - new_size) / 2
    new_y = y + (size - new_size) / 2

    # Check for early termination to avoid tiny squares
    if new_size < min_size:
        break

    # Update square parameters
    x, y, size = new_x, new_y, new_size

    #Reduce line width
    ctx.set_line_width(ctx.get_line_width() * line_width_reduction)

    #Alternate color for visual interest every 3 steps
    if i % 3 == 0:
        ctx.set_source_rgb(*highlight_color)
    else:
        ctx.set_source_rgb(*base_color)
