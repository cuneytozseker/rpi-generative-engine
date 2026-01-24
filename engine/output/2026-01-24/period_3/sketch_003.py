import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.95, 0.95, 0.95)  # Light grey background
ctx.paint()

# Grid parameters
grid_size = 80
grid_rows = height // grid_size
grid_cols = width // grid_size

# Color palette
black = (0.1, 0.1, 0.1)
red = (0.8, 0.2, 0.2)
blue = (0.2, 0.4, 0.8)
colors = [black, red, blue]  # Limited palette

# Modular letter components
def draw_module(ctx, x, y, size, module_type):
    ctx.set_line_width(size / 8)
    ctx.set_source_rgb(*random.choice(colors))

    if module_type == 0:  # Vertical line
        ctx.move_to(x + size / 2, y)
        ctx.line_to(x + size / 2, y + size)
        ctx.stroke()
    elif module_type == 1:  # Horizontal line
        ctx.move_to(x, y + size / 2)
        ctx.line_to(x + size, y + size / 2)
        ctx.stroke()
    elif module_type == 2:  # Diagonal line (top-left to bottom-right)
        ctx.move_to(x, y)
        ctx.line_to(x + size, y + size)
        ctx.stroke()
    elif module_type == 3: # Diagonal line (top-right to bottom-left)
        ctx.move_to(x + size, y)
        ctx.line_to(x, y + size)
        ctx.stroke()
    elif module_type == 4: # Circle segment (top left)
        ctx.arc(x + size/2, y + size/2, size/2, math.pi, 1.5*math.pi)
        ctx.stroke()
    elif module_type == 5: # Rectangle
         ctx.rectangle(x + size/4, y + size/4, size/2, size/2)
         ctx.fill()

# Generate the "type"
for row in range(grid_rows):
    for col in range(grid_cols):
        x = col * grid_size
        y = row * grid_size
        module_type = random.randint(0, 5)  # Random module
        draw_module(ctx, x, y, grid_size, module_type)
