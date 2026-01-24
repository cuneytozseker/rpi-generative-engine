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

# Grid parameters
grid_size = 40
rows = width // grid_size
cols = height // grid_size

# Color palette
black = (0, 0, 0)
red = (0.8, 0.2, 0.2)
blue = (0.2, 0.2, 0.8)

# Function to draw a random shape in a grid cell
def draw_shape(x, y):
    shape_type = random.choice(['rectangle', 'circle', 'triangle'])
    ctx.set_line_width(2)

    if shape_type == 'rectangle':
        w = random.uniform(grid_size * 0.2, grid_size * 0.8)
        h = random.uniform(grid_size * 0.2, grid_size * 0.8)
        rx = x + (grid_size - w) / 2
        ry = y + (grid_size - h) / 2
        if random.random() < 0.6:
            ctx.set_source_rgb(*black)
            ctx.rectangle(rx, ry, w, h)
            ctx.fill()
        else:
            ctx.set_source_rgb(*black)
            ctx.rectangle(rx, ry, w, h)
            ctx.stroke()

    elif shape_type == 'circle':
        radius = random.uniform(grid_size * 0.1, grid_size * 0.4)
        cx = x + grid_size / 2
        cy = y + grid_size / 2
        if random.random() < 0.6:
            ctx.set_source_rgb(*red)
            ctx.arc(cx, cy, radius, 0, 2 * math.pi)
            ctx.fill()
        else:
            ctx.set_source_rgb(*red)
            ctx.arc(cx, cy, radius, 0, 2 * math.pi)
            ctx.stroke()

    elif shape_type == 'triangle':
        s = random.uniform(grid_size * 0.3, grid_size * 0.7)
        x1 = x + grid_size / 2
        y1 = y + (grid_size - s * math.sqrt(3)/2) / 2
        x2 = x + (grid_size - s) / 2
        y2 = y + (grid_size + s * math.sqrt(3)/2) / 2
        x3 = x + (grid_size + s) / 2
        y3 = y + (grid_size + s * math.sqrt(3)/2) / 2
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.line_to(x3, y3)
        ctx.close_path()
        if random.random() < 0.6:
            ctx.set_source_rgb(*blue)
            ctx.fill()
        else:
            ctx.set_source_rgb(*blue)
            ctx.stroke()

# Iterate through the grid
for i in range(rows):
    for j in range(cols):
        x = i * grid_size
        y = j * grid_size
        if random.random() < 0.7:  # Probability of drawing a shape in a cell
            draw_shape(x, y)
