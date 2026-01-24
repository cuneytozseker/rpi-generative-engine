import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.paint()

# Brutalist Composition with Rectangles
ctx.set_source_rgb(0, 0, 0)  # Black

# Define grid parameters
grid_size = 40
num_cols = width // grid_size
num_rows = height // grid_size
rect_density = 0.7  # Probability of a rectangle appearing in a grid cell

# Iterate over the grid
for row in range(num_rows):
    for col in range(num_cols):
        # Calculate cell coordinates
        x = col * grid_size
        y = row * grid_size

        # Randomly determine if a rectangle should be drawn in this cell
        if random.random() < rect_density:
            # Randomly determine rectangle dimensions (with constraints)
            rect_width = random.randint(grid_size // 4, grid_size)
            rect_height = random.randint(grid_size // 4, grid_size)

            # Adjust position to keep the rectangle within the grid cell
            rect_x = x + random.randint(0, grid_size - rect_width) if (grid_size - rect_width) > 0 else x
            rect_y = y + random.randint(0, grid_size - rect_height) if (grid_size - rect_height) > 0 else y

            # Draw the rectangle
            ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
            ctx.fill()

# Introduce larger, dominant rectangles
num_dominant = 3
for _ in range(num_dominant):
    dom_width = random.randint(width // 4, width // 2)
    dom_height = random.randint(height // 4, height // 2)
    dom_x = random.randint(0, width - dom_width)
    dom_y = random.randint(0, height - dom_height)
    ctx.rectangle(dom_x, dom_y, dom_width, dom_height)
    ctx.fill()

# Add white outlines to some rectangles for contrast
ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.set_line_width(2)
outline_density = 0.1

for row in range(num_rows):
    for col in range(num_cols):
        # Calculate cell coordinates
        x = col * grid_size
        y = row * grid_size

        # Randomly determine if a rectangle should be drawn in this cell
        if random.random() < rect_density * outline_density:
            # Randomly determine rectangle dimensions (with constraints)
            rect_width = random.randint(grid_size // 4, grid_size)
            rect_height = random.randint(grid_size // 4, grid_size)

            # Adjust position to keep the rectangle within the grid cell
            rect_x = x + random.randint(0, grid_size - rect_width) if (grid_size - rect_width) > 0 else x
            rect_y = y + random.randint(0, grid_size - rect_height) if (grid_size - rect_height) > 0 else y

            # Draw the rectangle
            ctx.rectangle(rect_x, rect_y, rect_width, rect_height)
            ctx.stroke()
