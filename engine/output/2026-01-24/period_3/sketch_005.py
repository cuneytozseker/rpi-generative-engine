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

# Generative Code: Brutalist Rectangles

grid_size = 50
rect_variation = 20 # max size variation in each direction
density = 0.7  # Probability of a rectangle appearing at each grid point

ctx.set_source_rgb(1, 1, 1) # White rectangles
ctx.set_line_width(2)

for x in range(0, width, grid_size):
    for y in range(0, height, grid_size):
        if random.random() < density:
            # Introduce some variation in size and position
            rect_width = grid_size + random.randint(-rect_variation, rect_variation)
            rect_height = grid_size + random.randint(-rect_variation, rect_variation)
            rect_x = x + random.randint(-rect_variation//2, rect_variation//2)
            rect_y = y + random.randint(-rect_variation//2, rect_variation//2)

            # Ensure rectangles stay within bounds
            rect_x = max(0, min(rect_x, width - rect_width))
            rect_y = max(0, min(rect_y, height - rect_height))

            ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
            
            if random.random() < 0.2:  # Sometimes fill, sometimes just stroke
              ctx.fill()
            else:
              ctx.stroke()
