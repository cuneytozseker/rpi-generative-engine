import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # or your choice
ctx.paint()

# Grid parameters
grid_size = 40
num_cols = width // grid_size
num_rows = height // grid_size

# Colors
white = (1, 1, 1)
black = (0, 0, 0)
gray = (0.5, 0.5, 0.5)

# Function to draw a random geometric shape within a grid cell
def draw_shape(x, y, size):
    shape_type = random.choice(['rect', 'circle', 'triangle'])
    color = random.choice([white, gray])  # Reduced to white and gray

    ctx.set_source_rgb(*color)

    if shape_type == 'rect':
        w = random.uniform(size * 0.2, size * 0.8)
        h = random.uniform(size * 0.2, size * 0.8)
        x_offset = random.uniform(0, size - w)
        y_offset = random.uniform(0, size - h)
        ctx.rectangle(x + x_offset, y + y_offset, w, h)
        ctx.fill()
    elif shape_type == 'circle':
        radius = random.uniform(size * 0.1, size * 0.4)
        ctx.arc(x + size/2, y + size/2, radius, 0, 2 * math.pi)
        ctx.fill()
    elif shape_type == 'triangle':
        x1 = x + random.uniform(0, size)
        y1 = y + random.uniform(0, size)
        x2 = x + random.uniform(0, size)
        y2 = y + random.uniform(0, size)
        x3 = x + random.uniform(0, size)
        y3 = y + random.uniform(0, size)

        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.line_to(x3, y3)
        ctx.close_path()
        ctx.fill()

# Iterate through the grid
for row in range(num_rows):
    for col in range(num_cols):
        x = col * grid_size
        y = row * grid_size

        # Add some probability to skip drawing in a cell for whitespace
        if random.random() > 0.2: # increase for more empty cells
            draw_shape(x, y, grid_size)
