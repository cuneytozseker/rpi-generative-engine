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

# Generative Code: Radial Symmetry with Breaking Points

center_x, center_y = width / 2, height / 2
num_segments = 24  # Number of radial segments
radius = 350
line_width = 3

ctx.set_line_width(line_width)

for i in range(num_segments):
    angle = 2 * math.pi * i / num_segments
    x1 = center_x + radius * math.cos(angle)
    y1 = center_y + radius * math.sin(angle)

    # Add some randomness to breaking points
    break_chance = 0.2  # Chance for a segment to be broken

    ctx.set_source_rgb(1, 1, 1) # White

    ctx.move_to(center_x, center_y)
    ctx.line_to(x1, y1)

    if random.random() < break_chance:
        # Intentionally break the line slightly
        break_distance = 5 + random.random() * 10 # Random break distance
        break_angle = angle + (random.random() - 0.5) * 0.1  # Small random angle offset
        break_x = center_x + (radius - break_distance) * math.cos(break_angle)
        break_y = center_y + (radius - break_distance) * math.sin(break_angle)

        ctx.line_to(break_x, break_y)
        ctx.stroke()  # Draw partial line
        
        # Draw a small white rectangle at the point
        rect_size = 2
        ctx.rectangle(break_x - rect_size/2, break_y - rect_size/2, rect_size, rect_size)
        ctx.fill()


        # Start a new line from the break point to the original target
        ctx.move_to(break_x, break_y)
        ctx.line_to(x1, y1)
        ctx.stroke() # Finish the segmented line
    else:
        ctx.stroke()  # Draw full line
