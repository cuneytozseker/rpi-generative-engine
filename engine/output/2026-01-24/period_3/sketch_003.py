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

# --- Modular Typography System ---

# Grid parameters
grid_size = 40
x_count = width // grid_size
y_count = height // grid_size

# Define basic module shapes (lines, rectangles)
def draw_module(ctx, x, y, module_type):
    ctx.set_line_width(2)
    ctx.set_source_rgb(1, 1, 1)  # White lines

    if module_type == 0:  # Horizontal line
        ctx.move_to(x, y + grid_size / 2)
        ctx.line_to(x + grid_size, y + grid_size / 2)
        ctx.stroke()
    elif module_type == 1:  # Vertical line
        ctx.move_to(x + grid_size / 2, y)
        ctx.line_to(x + grid_size / 2, y + grid_size)
        ctx.stroke()
    elif module_type == 2:  # Diagonal line (top-left to bottom-right)
        ctx.move_to(x, y)
        ctx.line_to(x + grid_size, y + grid_size)
        ctx.stroke()
    elif module_type == 3:  # Diagonal line (top-right to bottom-left)
        ctx.move_to(x + grid_size, y)
        ctx.line_to(x, y + grid_size)
        ctx.stroke()
    elif module_type == 4:  # Small rectangle
        rect_size = grid_size / 3
        ctx.rectangle(x + grid_size / 3, y + grid_size / 3, rect_size, rect_size)
        ctx.fill()
    else: # Empty module
        pass

# "Typeface" definition (example: 'A', 'B', etc. using module patterns)
# Here, we're creating a systematic, randomized pattern

for i in range(x_count):
    for j in range(y_count):
        x = i * grid_size
        y = j * grid_size
        module_type = random.randint(0, 5) # Generate random module type
        draw_module(ctx, x, y, module_type)
