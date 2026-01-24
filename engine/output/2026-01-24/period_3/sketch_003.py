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
grid_size = 20
num_cols = width // grid_size
num_rows = height // grid_size

# Module definitions (simple line-based)
def module_a(ctx, x, y, size):
    ctx.move_to(x, y)
    ctx.line_to(x + size, y + size)
    ctx.stroke()

def module_b(ctx, x, y, size):
    ctx.move_to(x + size, y)
    ctx.line_to(x, y + size)
    ctx.stroke()

def module_c(ctx, x, y, size):
    ctx.move_to(x, y)
    ctx.line_to(x + size, y)
    ctx.stroke()

def module_d(ctx, x, y, size):
    ctx.move_to(x, y)
    ctx.line_to(x, y + size)
    ctx.stroke()

modules = [module_a, module_b, module_c, module_d]

# Color definitions
white = (1, 1, 1)

# Drawing loop
ctx.set_source_rgb(*white)
ctx.set_line_width(2)

for row in range(num_rows):
    for col in range(num_cols):
        x = col * grid_size
        y = row * grid_size

        # Randomly choose a module to draw
        module = random.choice(modules)
        module(ctx, x, y, grid_size)
