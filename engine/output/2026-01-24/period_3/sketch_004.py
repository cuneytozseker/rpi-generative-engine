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

# Wave Interference

amplitude = 50
frequency1 = 0.02
frequency2 = 0.025
phase_shift = math.pi / 4
line_width = 2

ctx.set_line_width(line_width)
ctx.set_source_rgb(1, 1, 1) # White

for y in range(0, height, 10):
    ctx.move_to(0, y)
    for x in range(width):
        # Wave 1
        y1 = amplitude * math.sin(frequency1 * x)

        # Wave 2 (with a phase shift)
        y2 = amplitude * math.sin(frequency2 * x + phase_shift)

        # Combined wave (interference)
        y_combined = y1 + y2

        ctx.line_to(x, y + y_combined)

    ctx.stroke()
