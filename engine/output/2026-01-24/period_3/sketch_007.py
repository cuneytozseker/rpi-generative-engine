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

# Generative code: Radial Symmetry with Breaking Points

center_x, center_y = width / 2, height / 2
num_segments = 12  # Number of symmetrical segments
radius = 350
line_width = 3
ctx.set_line_width(line_width)

def draw_segment(angle_start, angle_end, offset):
    # Calculate start and end points of the segment
    x1 = center_x + radius * math.cos(angle_start + offset)
    y1 = center_y + radius * math.sin(angle_start + offset)
    x2 = center_x + radius * math.cos(angle_end + offset)
    y2 = center_y + radius * math.sin(angle_end + offset)

    # Draw a line segment
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

ctx.set_source_rgb(1, 1, 1)

angle_increment = 2 * math.pi / num_segments

for i in range(num_segments):
    angle_start = i * angle_increment
    angle_end = (i + 1) * angle_increment

    # Introduce variation: Random offset to create breaking points
    offset = random.uniform(-angle_increment/4, angle_increment/4)

    draw_segment(angle_start, angle_end, offset)

    # Add small inner circles with some probability
    if random.random() < 0.3:
        inner_radius = radius * 0.3
        circle_x = center_x + inner_radius * math.cos(angle_start + angle_increment/2 + offset)
        circle_y = center_y + inner_radius * math.sin(angle_start + angle_increment/2 + offset)

        ctx.arc(circle_x, circle_y, 5, 0, 2 * math.pi)
        ctx.fill()
