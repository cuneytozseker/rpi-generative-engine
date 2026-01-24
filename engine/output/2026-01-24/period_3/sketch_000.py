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

# Swiss Grid & Geometric Shapes
grid_size = 40
cols = width // grid_size
rows = height // grid_size

ctx.set_line_width(2)

for row in range(rows):
    for col in range(cols):
        x = col * grid_size
        y = row * grid_size

        # Random shape selection
        shape_type = random.choice(['rect', 'circle', 'triangle', 'line'])

        if shape_type == 'rect':
            w = random.randint(grid_size // 2, grid_size)
            h = random.randint(grid_size // 2, grid_size)
            x_offset = random.randint(0, grid_size - w)
            y_offset = random.randint(0, grid_size - h)

            ctx.set_source_rgb(1, 1, 1)
            ctx.rectangle(x + x_offset, y + y_offset, w, h)
            ctx.fill()

        elif shape_type == 'circle':
            radius = random.randint(grid_size // 4, grid_size // 2)
            ctx.set_source_rgb(1, 0, 0) #red circles
            ctx.arc(x + grid_size // 2, y + grid_size // 2, radius, 0, 2 * math.pi)
            ctx.fill()

        elif shape_type == 'triangle':
            x1 = x + random.randint(0, grid_size)
            y1 = y + random.randint(0, grid_size)
            x2 = x + random.randint(0, grid_size)
            y2 = y + random.randint(0, grid_size)
            x3 = x + random.randint(0, grid_size)
            y3 = y + random.randint(0, grid_size)

            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.line_to(x3, y3)
            ctx.close_path()
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()

        elif shape_type == 'line':
            x1 = x + random.randint(0, grid_size)
            y1 = y + random.randint(0, grid_size)
            x2 = x + random.randint(0, grid_size)
            y2 = y + random.randint(0, grid_size)

            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.set_source_rgb(1, 1, 1)
            ctx.stroke()
