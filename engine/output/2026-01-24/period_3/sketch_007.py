import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0, 0, 0)  # Black background
ctx.paint()

# Generative Code: Radial Symmetry with Breaking Points

center_x, center_y = width / 2, height / 2
num_segments = 12
radius = min(width, height) / 3
segment_angle = 2 * math.pi / num_segments

ctx.set_line_width(2)

for i in range(num_segments):
    angle = i * segment_angle
    x1 = center_x + radius * math.cos(angle)
    y1 = center_y + radius * math.sin(angle)

    # Introduce variation in line length
    length_factor = random.uniform(0.5, 1.0)  # Vary length between 50% and 100% of radius
    x2 = center_x + length_factor * radius * math.cos(angle)
    y2 = center_y + length_factor * radius * math.sin(angle)

    # Introduce gaps and random color changes
    if random.random() < 0.2:  # 20% chance of a gap
        continue

    ctx.set_source_rgb(1, 1, 1)  # White lines

    ctx.move_to(center_x, center_y)
    ctx.line_to(x2, y2) # Use modified end point
    ctx.stroke()

    # Add small circles at some endpoints
    if random.random() < 0.1: # 10% chance of circle
        ctx.arc(x2, y2, 3, 0, 2 * math.pi)
        ctx.fill()

# Add a central element
ctx.set_source_rgb(1, 0, 0) # Red center
ctx.arc(center_x, center_y, radius / 8, 0, 2 * math.pi)
ctx.fill()
