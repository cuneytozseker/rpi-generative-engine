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

# Radial Symmetry with Breaking Points
center_x, center_y = width / 2, height / 2
num_segments = 12  # Number of radial segments
radius = min(width, height) / 2 * 0.9 # Radius of the overall pattern

for i in range(num_segments):
    angle = 2 * math.pi * i / num_segments
    x1 = center_x + radius * math.cos(angle)
    y1 = center_y + radius * math.sin(angle)

    # Introduce variation: probability of line breaking
    break_probability = 0.25
    if random.random() > break_probability:
        ctx.set_source_rgb(1, 1, 1) # White lines
        ctx.set_line_width(2)
        ctx.move_to(center_x, center_y)
        ctx.line_to(x1, y1)
        ctx.stroke()

    # Smaller circles along the lines with slight offset
    num_circles = 5
    for j in range(num_circles):
        t = (j + 1) / (num_circles + 1)  # Parameter for position along the line
        circle_x = center_x + t * (x1 - center_x)
        circle_y = center_y + t * (y1 - center_y)
        circle_radius = radius * 0.03 * (0.8 + 0.2 * random.random())  # Varying circle radius

        # Introduce offset based on segment number
        offset_angle = angle + math.pi / (num_segments * 4) * (i % 4 - 1.5) # Small angular offset
        offset_x = circle_radius * 0.5 * math.cos(offset_angle)
        offset_y = circle_radius * 0.5 * math.sin(offset_angle)
        circle_x += offset_x
        circle_y += offset_y
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(circle_x, circle_y, circle_radius, 0, 2 * math.pi)
        ctx.fill()

    # Add small black squares at intersections if adjacent lines present

    angle_next = 2 * math.pi * (i + 1) / num_segments

    if random.random() > break_probability:
        ctx.set_source_rgb(0, 0, 0)
        square_size = radius * 0.01
        ctx.rectangle(x1 - square_size/2, y1- square_size/2, square_size, square_size)
        ctx.fill()
