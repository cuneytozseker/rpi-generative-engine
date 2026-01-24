import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(1, 1, 1)  # White background
ctx.paint()

# Grid parameters
grid_size = 8
cell_width = width / grid_size
cell_height = height / grid_size
margin = 5 # small margin

# Color palette
black = (0, 0, 0)
gray = (0.8, 0.8, 0.8)
red = (0.9, 0.1, 0.1)

colors = [black, gray, red]

# Random seed for consistency
random.seed(42)

# Draw grid and shapes
for row in range(grid_size):
    for col in range(grid_size):
        x1 = col * cell_width + margin
        y1 = row * cell_height + margin
        x2 = (col + 1) * cell_width - margin
        y2 = (row + 1) * cell_height - margin

        cell_x = col * cell_width
        cell_y = row * cell_height
        cell_w = cell_width
        cell_h = cell_height


        # Randomly choose a shape
        shape_type = random.randint(0, 3)

        ctx.set_source_rgb(*random.choice(colors))

        if shape_type == 0:  # Rectangle
            ctx.rectangle(x1, y1, x2 - x1, y2 - y1)
            ctx.fill()
        elif shape_type == 1:  # Circle
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = min(x2 - x1, y2 - y1) / 2
            ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
            ctx.fill()
        elif shape_type == 2:  # Diagonal Line
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.set_line_width(random.uniform(3, 8))
            ctx.stroke()
        elif shape_type == 3: # Empty circle outline
             center_x = (x1 + x2) / 2
             center_y = (y1 + y2) / 2
             radius = min(x2 - x1, y2 - y1) / 2
             ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
             ctx.set_source_rgb(0,0,0)
             ctx.set_line_width(random.uniform(2, 6))
             ctx.stroke()
