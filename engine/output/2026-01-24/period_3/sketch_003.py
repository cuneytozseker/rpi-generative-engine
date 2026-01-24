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
horizontal_modules = width // grid_size
vertical_modules = height // grid_size

# Color palette
white = (1, 1, 1)
black = (0, 0, 0)
gray = (0.5, 0.5, 0.5)

# Function to draw a modular character (example: 'H')
def draw_module_H(x, y, size, color):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(size / 5) # Consistent stroke weight
    
    # Vertical lines
    ctx.move_to(x + size / 5, y + size / 5)
    ctx.line_to(x + size / 5, y + size * 4 / 5)
    ctx.stroke()
    
    ctx.move_to(x + size * 4 / 5, y + size / 5)
    ctx.line_to(x + size * 4 / 5, y + size * 4 / 5)
    ctx.stroke()
    
    # Horizontal line
    ctx.move_to(x + size / 5, y + size / 2)
    ctx.line_to(x + size * 4 / 5, y + size / 2)
    ctx.stroke()


# Function to draw a modular character (example: 'O')
def draw_module_O(x, y, size, color):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(size / 5) # Consistent stroke weight
    ctx.arc(x + size/2, y + size/2, size * 2 / 5, 0, 2 * math.pi)
    ctx.stroke()


# Function to draw a modular character (example: 'X')
def draw_module_X(x, y, size, color):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(size / 5) # Consistent stroke weight
    ctx.move_to(x + size / 5, y + size / 5)
    ctx.line_to(x + size * 4 / 5, y + size * 4 / 5)
    ctx.stroke()

    ctx.move_to(x + size * 4 / 5, y + size / 5)
    ctx.line_to(x + size / 5, y + size * 4 / 5)
    ctx.stroke()



# Generate typography pattern
random.seed(42) # for deterministic results
for i in range(horizontal_modules):
    for j in range(vertical_modules):
        x = i * grid_size
        y = j * grid_size
        
        # Probabilistic character selection
        r = random.random()
        if r < 0.33:
            draw_module_H(x, y, grid_size, white)
        elif r < 0.66:
            draw_module_O(x, y, grid_size, white)
        else:
            draw_module_X(x, y, grid_size, white)
