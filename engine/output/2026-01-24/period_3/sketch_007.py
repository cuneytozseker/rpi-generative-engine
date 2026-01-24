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

# Generative code: Radial symmetry with breaking points

center_x, center_y = width / 2, height / 2
num_segments = 16  # Number of radial segments
radius = min(width, height) / 2 * 0.9
segment_angle = 2 * math.pi / num_segments

ctx.set_line_width(2)

for i in range(num_segments):
    angle = i * segment_angle

    # Calculate start and end points for the line segment
    start_x = center_x + radius * math.cos(angle)
    start_y = center_y + radius * math.sin(angle)
    end_x = center_x
    end_y = center_y

    # Decide whether to draw the line segment or "break" it
    if random.random() < 0.8: # Probability of drawing a line
        ctx.set_source_rgb(1, 1, 1)  # White
        ctx.move_to(start_x, start_y)
        ctx.line_to(end_x, end_y)
        ctx.stroke()
    else:
         # Draw a small circle as a breaking point
        break_radius = 5
        ctx.set_source_rgb(1, 0, 0) # Red to emphasize break
        ctx.arc(start_x, start_y, break_radius, 0, 2 * math.pi)
        ctx.fill()
