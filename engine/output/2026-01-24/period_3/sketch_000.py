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
num_cols = width // grid_size
num_rows = height // grid_size

ctx.set_line_width(2)

for row in range(num_rows):
    for col in range(num_cols):
        x = col * grid_size
        y = row * grid_size

        # Randomly choose a shape and color
        shape_type = random.choice(['rectangle', 'circle', 'triangle'])
        color_r = random.uniform(0.9, 1)
        color_g = random.uniform(0.9, 1)
        color_b = random.uniform(0.9, 1)
        ctx.set_source_rgb(color_r, color_g, color_b)


        if shape_type == 'rectangle':
            rect_width = random.uniform(grid_size/2, grid_size)
            rect_height = random.uniform(grid_size/2, grid_size)
            ctx.rectangle(x + (grid_size - rect_width)/2, y + (grid_size - rect_height)/2, rect_width, rect_height)
            if random.random() < 0.5:
                ctx.fill()
            else:
                ctx.stroke()


        elif shape_type == 'circle':
            radius = random.uniform(grid_size/4, grid_size/2)
            ctx.arc(x + grid_size/2, y + grid_size/2, radius, 0, 2 * math.pi)
            if random.random() < 0.5:
                ctx.fill()
            else:
                ctx.stroke()

        elif shape_type == 'triangle':
            x1 = x + grid_size / 2
            y1 = y
            x2 = x
            y2 = y + grid_size
            x3 = x + grid_size
            y3 = y + grid_size
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.line_to(x3, y3)
            ctx.close_path()
            if random.random() < 0.5:
                ctx.fill()
            else:
                ctx.stroke()
