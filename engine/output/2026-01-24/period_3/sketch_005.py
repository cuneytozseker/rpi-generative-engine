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

# --- Generative Code: Brutalist Rectangles ---
ctx.set_source_rgb(1, 1, 1)  # White rectangles

# Grid parameters
grid_x = 10
grid_y = 10
cell_width = width / grid_x
cell_height = height / grid_y

# Randomness parameters
max_offset_x = cell_width * 0.2
max_offset_y = cell_height * 0.2
min_rect_size = 0.3
max_rect_size = 0.8

# Loop through grid
for i in range(grid_x):
    for j in range(grid_y):
        # Calculate cell center
        center_x = i * cell_width + cell_width / 2
        center_y = j * cell_height + cell_height / 2

        # Random offset
        offset_x = random.uniform(-max_offset_x, max_offset_x)
        offset_y = random.uniform(-max_offset_y, max_offset_y)

        # Random rectangle size (relative to cell)
        rect_width = cell_width * random.uniform(min_rect_size, max_rect_size)
        rect_height = cell_height * random.uniform(min_rect_size, max_rect_size)

        # Calculate rectangle top-left corner
        rect_x = center_x - rect_width / 2 + offset_x
        rect_y = center_y - rect_height / 2 + offset_y

        # Draw rectangle
        ctx.rectangle(rect_x, rect_y, rect_width, rect_height)

        # Randomly fill or stroke (brutalist variation)
        if random.random() < 0.7: # 70% fill, 30% stroke
            ctx.fill()
        else:
            ctx.set_line_width(random.uniform(2, 6))
            ctx.stroke()
