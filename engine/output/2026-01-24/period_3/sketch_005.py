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

# Generative code: Brutalist rectangles

rect_count = 20  # Number of rectangles
min_size = 20
max_size = 200
padding = 20

ctx.set_source_rgb(1, 1, 1)  # White rectangles

for i in range(rect_count):
    x = random.randint(padding, width - padding)
    y = random.randint(padding, height - padding)
    w = random.randint(min_size, max_size)
    h = random.randint(min_size, max_size)

    # Ensure rectangle stays within bounds
    x = max(padding, min(x, width - w - padding))
    y = max(padding, min(y, height - h - padding))

    ctx.rectangle(x, y, w, h)

    if random.random() < 0.3: # Randomly fill some rectangles
        ctx.fill_preserve()
        ctx.set_source_rgb(0,0,0)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.set_source_rgb(1,1,1)

    else:
        ctx.set_line_width(3)
        ctx.stroke()
