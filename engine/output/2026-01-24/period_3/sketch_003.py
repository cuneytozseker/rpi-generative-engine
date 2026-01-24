import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # or your choice
ctx.paint()

# Generative Code: Modular Typography System

grid_size = 20
module_size = width / grid_size
gap = module_size * 0.1

def draw_module(x, y, module_type, color=(1,1,1)):
    ctx.set_source_rgb(*color)
    x = x * module_size
    y = y * module_size

    if module_type == 0:  # Empty
        pass
    elif module_type == 1: # Horizontal bar
        ctx.rectangle(x + gap, y + module_size/2 - module_size/8, module_size - 2*gap, module_size/4)
        ctx.fill()
    elif module_type == 2: # Vertical bar
        ctx.rectangle(x + module_size/2 - module_size/8, y + gap, module_size/4, module_size - 2*gap)
        ctx.fill()
    elif module_type == 3: # Diagonal top-left to bottom-right
        ctx.move_to(x + gap, y + gap)
        ctx.line_to(x + module_size - gap, y + module_size - gap)
        ctx.set_line_width(module_size/4)
        ctx.stroke()
    elif module_type == 4: # Diagonal top-right to bottom-left
        ctx.move_to(x + module_size - gap, y + gap)
        ctx.line_to(x + gap, y + module_size - gap)
        ctx.set_line_width(module_size/4)
        ctx.stroke()
    elif module_type == 5: # Circle segment - top left
        ctx.arc(x+module_size/2, y+module_size/2, module_size/2 - gap, math.pi, 3*math.pi/2)
        ctx.set_line_width(module_size/4)
        ctx.stroke()
    elif module_type == 6: # Circle segment - top right
         ctx.arc(x+module_size/2, y+module_size/2, module_size/2 - gap, 3*math.pi/2, 0)
         ctx.set_line_width(module_size/4)
         ctx.stroke()
    elif module_type == 7: # Circle segment - bottom right
         ctx.arc(x+module_size/2, y+module_size/2, module_size/2 - gap, 0, math.pi/2)
         ctx.set_line_width(module_size/4)
         ctx.stroke()
    elif module_type == 8: # Circle segment - bottom left
         ctx.arc(x+module_size/2, y+module_size/2, module_size/2 - gap, math.pi/2, math.pi)
         ctx.set_line_width(module_size/4)
         ctx.stroke()

# Define a few "letters" using the modules
letters = {
    "A": [[1,2,1],
          [2,0,2],
          [2,1,2]],
    "B": [[1,2,1],
          [2,1,2],
          [1,2,1]],
    "C": [[1,1,1],
          [2,0,0],
          [1,1,1]],
    "D": [[1,2,1],
          [2,0,2],
          [1,2,1]]
}

# Choose a letter or make your own pattern
chosen_letter = "A"

# Render the letter multiple times, offset and scaled
num_repeats = 4
offset_x = 2
offset_y = 2

for i in range(num_repeats):
    for row_index, row in enumerate(letters[chosen_letter]):
        for col_index, module_type in enumerate(row):
            x = col_index + i*offset_x
            y = row_index + i*offset_y
            draw_module(x, y, module_type)

# Example with other modules - a pattern
# for i in range(grid_size):
#     for j in range(grid_size):
#         module_type = (i + j) % 9 # Cycle through the modules
#         draw_module(i,j, module_type)
