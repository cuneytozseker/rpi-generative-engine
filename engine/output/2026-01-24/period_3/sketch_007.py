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
radius = min(width, height) / 2 * 0.9  # Radius of the overall structure
segment_angle = 2 * math.pi / num_segments
num_rings = 5  # Number of concentric rings

ctx.set_line_width(2)

for i in range(num_segments):
    angle = i * segment_angle
    x1 = center_x + radius * math.cos(angle)
    y1 = center_y + radius * math.sin(angle)

    # Vary line thickness and color per segment
    if i % 3 == 0:
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(3)  # Make certain lines thicker
    else:
        ctx.set_source_rgb(0.8, 0.8, 0.8)
        ctx.set_line_width(1)

    ctx.move_to(center_x, center_y)
    ctx.line_to(x1, y1)
    ctx.stroke()

    # Introduce small arcs as breaking points along each radial line
    for j in range(num_rings):
        arc_radius = radius / num_rings * (j + 1) * 0.2
        arc_x = center_x + arc_radius * math.cos(angle)
        arc_y = center_y + arc_radius * math.sin(angle)

        # Subtle rotation to offset arcs from the main line
        rotation_offset = random.uniform(-0.1, 0.1) # Radians
        arc_start = angle - 0.1 + rotation_offset
        arc_end = angle + 0.1 + rotation_offset

        ctx.set_source_rgb(0.9, 0.9, 0.9)
        ctx.set_line_width(1.5)
        ctx.arc(arc_x, arc_y, 3, arc_start, arc_end)
        ctx.stroke()
