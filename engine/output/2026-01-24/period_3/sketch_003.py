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

# Typography module parameters
module_size = grid_size * 2  # Each module spans 2x2 grid cells
stroke_width = 3

# Function to draw a modular 'H'
def draw_h(x, y):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(stroke_width)

    # Vertical lines
    ctx.move_to(x + grid_size / 2, y + grid_size / 4)
    ctx.line_to(x + grid_size / 2, y + module_size - grid_size / 4)
    ctx.stroke()

    ctx.move_to(x + module_size - grid_size / 2, y + grid_size / 4)
    ctx.line_to(x + module_size - grid_size / 2, y + module_size - grid_size / 4)
    ctx.stroke()

    # Horizontal line
    ctx.move_to(x + grid_size / 2, y + module_size / 2)
    ctx.line_to(x + module_size - grid_size / 2, y + module_size / 2)
    ctx.stroke()

# Function to draw a modular 'O'
def draw_o(x, y):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(stroke_width)

    ctx.arc(x + module_size / 2, y + module_size / 2, module_size / 2 - stroke_width / 2, 0, 2 * math.pi)
    ctx.stroke()

# Function to draw a modular 'I'
def draw_i(x, y):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(stroke_width)

    ctx.move_to(x + module_size / 2, y + grid_size / 4)
    ctx.line_to(x + module_size / 2, y + module_size - grid_size / 4)
    ctx.stroke()

# Function to draw a modular '!'
def draw_exclamation(x,y):
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(stroke_width)

    ctx.move_to(x + module_size / 2, y + grid_size / 4)
    ctx.line_to(x + module_size / 2, y + module_size / 2)
    ctx.stroke()

    ctx.arc(x + module_size / 2, y + module_size - grid_size / 4, 2, 0, 2 * math.pi)
    ctx.fill()

# Draw modules in a grid
for row in range(0, num_rows - 1, 2):  # Step by 2 to account for module size
    for col in range(0, num_cols - 1, 2):
        x = col * grid_size
        y = row * grid_size

        # Randomly choose which module to draw
        choice = random.choice(['h', 'o', 'i', '!'])
        if choice == 'h':
            draw_h(x, y)
        elif choice == 'o':
            draw_o(x, y)
        elif choice == 'i':
            draw_i(x, y)
        else:
            draw_exclamation(x, y)
