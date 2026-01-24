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

# Grid parameters
grid_size = 20
grid_rows = height // grid_size
grid_cols = width // grid_size

# Rectangle parameters
max_rect_size = grid_size * 4
min_rect_size = grid_size

# Color palette
white = (1, 1, 1)
gray = (0.5, 0.5, 0.5)

ctx.set_line_width(1)

for row in range(grid_rows):
    for col in range(grid_cols):
        # Chance to draw rectangle
        if random.random() < 0.3:  # density of rectangles
            x = col * grid_size
            y = row * grid_size

            # Random width and height
            rect_width = random.randint(min_rect_size, max_rect_size)
            rect_height = random.randint(min_rect_size, max_rect_size)

            # Adjust for grid boundaries
            if x + rect_width > width:
                rect_width = width - x
            if y + rect_height > height:
                rect_height = height - y

            # Color selection
            if random.random() < 0.7:
                ctx.set_source_rgb(*white)
            else:
                ctx.set_source_rgb(*gray)

            # Draw rectangle
            ctx.rectangle(x, y, rect_width, rect_height)
            ctx.fill()

        # Chance to draw outline
        elif random.random() < 0.1:
            x = col * grid_size
            y = row * grid_size

            # Random width and height (smaller outlines)
            rect_width = random.randint(grid_size, grid_size * 2)
            rect_height = random.randint(grid_size, grid_size * 2)

             # Adjust for grid boundaries
            if x + rect_width > width:
                rect_width = width - x
            if y + rect_height > height:
                rect_height = height - y

            ctx.set_source_rgb(*white)  # White outlines
            ctx.rectangle(x, y, rect_width, rect_height)
            ctx.stroke()
