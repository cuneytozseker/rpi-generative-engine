import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Black
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Constants
PHI = (1 + 5**0.5) / 2
GOLDEN_RATIO = 1 / PHI

def draw_subdivision(x, y, w, h, depth, max_depth, orientation):
    if depth > max_depth or w < 2 or h < 2:
        return

    # Draw the current boundary
    line_weight = (max_depth - depth + 1) * 0.4
    ctx.set_line_width(line_weight)
    
    # Swiss-inspired palette: High contrast White/Grey with a highlight
    if random.random() > 0.92:
        ctx.set_source_rgba(0.9, 0.1, 0.1, 0.8) # Swiss Red highlight
    else:
        alpha = 0.3 + (0.7 * (depth / max_depth))
        ctx.set_source_rgba(0.9, 0.9, 0.9, alpha)

    ctx.rectangle(x, y, w, h)
    
    # Variety of rendering styles per cell
    style_roll = random.random()
    if style_roll > 0.85:
        ctx.fill() # Solid block
    elif style_roll > 0.6:
        ctx.stroke() # Simple outline
    elif style_roll > 0.4:
        # Internal rhythm lines (Hatching)
        ctx.stroke()
        ctx.set_line_width(0.2)
        spacing = 3.0
        if orientation == 'v':
            for i in range(1, int(w/spacing)):
                ctx.move_to(x + i*spacing, y)
                ctx.line_to(x + i*spacing, y + h)
        else:
            for i in range(1, int(h/spacing)):
                ctx.move_to(x, y + i*spacing)
                ctx.line_to(x + w, y + i*spacing)
        ctx.stroke()
    else:
        ctx.stroke()

    # Recursive logic
    if orientation == 'v':
        new_w = w * GOLDEN_RATIO
        # Decide which side to keep as the "square" and which to subdivide
        if random.random() > 0.5:
            draw_subdivision(x, y, new_w, h, depth + 1, max_depth, 'h')
            draw_subdivision(x + new_w, y, w - new_w, h, depth + 1, max_depth, 'h')
        else:
            draw_subdivision(x + (w - new_w), y, new_w, h, depth + 1, max_depth, 'h')
            draw_subdivision(x, y, w - new_w, h, depth + 1, max_depth, 'h')
    else:
        new_h = h * GOLDEN_RATIO
        if random.random() > 0.5:
            draw_subdivision(x, y, w, new_h, depth + 1, max_depth, 'v')
            draw_subdivision(x, y + new_h, w, h - new_h, depth + 1, max_depth, 'v')
        else:
            draw_subdivision(x, y + (h - new_h), w, new_h, depth + 1, max_depth, 'v')
            draw_subdivision(x, y, w, h - new_h, depth + 1, max_depth, 'v')

def draw_detail_overlay():
    """Adds a fine mathematical grid overlay to enhance the technical feel."""
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.set_line_width(0.5)
    
    # Vertical markers
    step = width / 20
    for i in range(21):
        ctx.move_to(i * step, 0)
        ctx.line_to(i * step, 10)
        ctx.move_to(i * step, height - 10)
        ctx.line_to(i * step, height)
    
    # Horizontal markers
    step = height / 20
    for i in range(21):
        ctx.move_to(0, i * step)
        ctx.line_to(10, i * step)
        ctx.move_to(width - 10, i * step)
        ctx.line_to(width, i * step)
    
    ctx.stroke()

# --- Execution ---

# 1. Main compositional layers
# We create three overlapping subdivision systems with different scales
random.seed(42) # For consistent rhythm

# Layer 1: Large structural blocks
draw_subdivision(40, 40, width-80, height-80, 0, 4, 'v')

# Layer 2: Medium scale details (slightly offset)
ctx.set_operator(cairo.OPERATOR_ADD) # Lighten overlaps
draw_subdivision(60, 60, width-120, height-120, 0, 6, 'h')

# Layer 3: Fine micro-structures in specific zones
ctx.set_operator(cairo.OPERATOR_OVER)
for _ in range(3):
    rx = random.randint(100, 400)
    ry = random.randint(100, 300)
    rw = random.randint(100, 200)
    rh = random.randint(100, 200)
    draw_subdivision(rx, ry, rw, rh, 0, 8, 'v')

# 2. Final Swiss design accents
draw_detail_overlay()

# Tiny data-points (crosses) at random grid intersections
ctx.set_source_rgb(0.8, 0.8, 0.8)
ctx.set_line_width(1.0)
for _ in range(15):
    px, py = random.randint(50, 550), random.randint(50, 430)
    size = 4
    ctx.move_to(px - size, py)
    ctx.line_to(px + size, py)
    ctx.move_to(px, py - size)
    ctx.line_to(px, py + size)
    ctx.stroke()

# Clean border
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
