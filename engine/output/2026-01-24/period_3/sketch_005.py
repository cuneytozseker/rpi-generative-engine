import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.95, 0.95, 0.95)  # Light gray background
ctx.paint()

# Generative code: Brutalist Rectangles

# Grid parameters
grid_size = 40
num_rects_x = width // grid_size
num_rects_y = height // grid_size

ctx.set_line_width(1)

for i in range(num_rects_x):
    for j in range(num_rects_y):
        x = i * grid_size
        y = j * grid_size

        # Random variations in rectangle size and position
        width_variation = random.uniform(0.2, 0.8)  # Rectangle width percentage
        height_variation = random.uniform(0.2, 0.8) # Rectangle height percentage
        x_offset = random.uniform(-grid_size * 0.1, grid_size * 0.1)  # Slight position shift
        y_offset = random.uniform(-grid_size * 0.1, grid_size * 0.1)

        rect_width = grid_size * width_variation
        rect_height = grid_size * height_variation

        rect_x = x + x_offset + (grid_size - rect_width) / 2  # Centering within grid cell
        rect_y = y + y_offset + (grid_size - rect_height) / 2

        # Probability of rectangle being filled/stroked
        if random.random() < 0.8:  # 80% probability
            ctx.set_source_rgb(0, 0, 0)  # Black
            ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
            if random.random() < 0.7:
                 ctx.fill()
            else:
                ctx.stroke()
