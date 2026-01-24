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

# Concentric Circles with Systematic Offset
center_x, center_y = width / 2, height / 2
num_circles = 40
max_radius = min(width, height) / 2 * 0.9  # leave some margin
radius_step = max_radius / num_circles
offset_factor = 0.05  # Controls the amount of offset
random.seed(42)  # Fixed seed for reproducibility

for i in range(num_circles):
    radius = radius_step * (i + 1)
    angle_offset = offset_factor * radius  # Offset increases with radius
    num_segments = 24 # Fixed number of segments to maintain consistency

    for j in range(num_segments):
      angle = 2 * math.pi * j / num_segments + angle_offset * (1 if i % 2 == 0 else -1) # Alternating direction
      x = center_x + radius * math.cos(angle)
      y = center_y + radius * math.sin(angle)

      if j == 0:
          ctx.move_to(x, y)
      else:
          ctx.line_to(x, y)

    ctx.close_path() # Ensures the shape is closed
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(1)
    ctx.stroke()
