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

# Modular Typography System

# Grid parameters
grid_size = 40
num_cols = width // grid_size
num_rows = height // grid_size

# Module definitions (basic shapes)
def draw_square(ctx, x, y, size):
    ctx.rectangle(x, y, size, size)
    ctx.fill()

def draw_circle_segment(ctx, x, y, radius, angle1, angle2):
    ctx.arc(x, y, radius, angle1, angle2)
    ctx.line_to(x, y)  # Close the path
    ctx.fill()

# Color palette
color_white = (1, 1, 1)
color_grey = (0.5, 0.5, 0.5)

# Random seed for reproducibility
random.seed(42)

# Generate "letters" based on grid positions
for row in range(num_rows):
    for col in range(num_cols):
        x = col * grid_size
        y = row * grid_size

        # Randomly select a module or a combination of modules
        module_choice = random.randint(0, 5)

        ctx.set_source_rgb(*color_white)

        if module_choice == 0:
            # Square
            draw_square(ctx, x, y, grid_size)
        elif module_choice == 1:
            # Quarter circle - top left
            draw_circle_segment(ctx, x + grid_size, y + grid_size, grid_size, math.pi, 1.5 * math.pi)
        elif module_choice == 2:
            # Quarter circle - top right
            draw_circle_segment(ctx, x, y + grid_size, grid_size, 1.5 * math.pi, 0)
        elif module_choice == 3:
            # Quarter circle - bottom left
            draw_circle_segment(ctx, x + grid_size, y, grid_size, math.pi / 2 * 3, math.pi * 2)
        elif module_choice == 4:
            # Quarter circle - bottom right
            draw_circle_segment(ctx, x, y, grid_size, 0, math.pi / 2)
        else:
            # Combination of two quarter circles (forming an "S" shape)
            ctx.set_source_rgb(*color_white)
            draw_circle_segment(ctx, x + grid_size, y + grid_size, grid_size/2, math.pi, 1.5 * math.pi)
            draw_circle_segment(ctx, x, y, grid_size/2, 0, math.pi / 2)
