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
grid_size = 40
cols = width // grid_size
rows = height // grid_size

# Color palette
white = (1, 1, 1)
gray = (0.5, 0.5, 0.5)
black = (0, 0, 0)

# Function to draw shapes in grid cells
def draw_shape(ctx, x, y, size):
    shape_type = random.choice(["rect", "circle", "triangle", "line"])

    if shape_type == "rect":
        w = random.uniform(0.2, 1) * size
        h = random.uniform(0.2, 1) * size
        x_offset = random.uniform(0, size - w)
        y_offset = random.uniform(0, size - h)
        ctx.rectangle(x + x_offset, y + y_offset, w, h)

    elif shape_type == "circle":
        radius = random.uniform(0.1, 0.5) * size
        ctx.arc(x + size / 2, y + size / 2, radius, 0, 2 * math.pi)

    elif shape_type == "triangle":
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
    
    elif shape_type == "line":
        x1 = x + random.uniform(0, size)
        y1 = y + random.uniform(0, size)
        x2 = x + random.uniform(0, size)
        y2 = y + random.uniform(0, size)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)

    return random.choice([white, gray, black])

# Draw the grid with shapes
for row in range(rows):
    for col in range(cols):
        x = col * grid_size
        y = row * grid_size
        
        if random.random() < 0.8: # probability for drawing something
            color = draw_shape(ctx, x, y, grid_size)
            ctx.set_source_rgb(*color)
            
            if random.random() < 0.5:
                 ctx.fill()
            else:
                ctx.set_line_width(random.uniform(1,3))
                ctx.stroke()

        else:
            pass #leave cell blank sometimes

