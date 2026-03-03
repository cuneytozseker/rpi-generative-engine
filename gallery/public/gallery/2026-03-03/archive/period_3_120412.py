import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Golden Ratio
PHI = (1 + 5**0.5) / 2

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)  # Near black
ctx.paint()

def draw_stipple(ctx, x, y, w, h, density):
    """Creates a field of points simulating topographic depth."""
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.6)
    for _ in range(int(w * h * density)):
        px = x + random.random() * w
        py = y + random.random() * h
        ctx.arc(px, py, 0.4, 0, 2 * math.pi)
        ctx.fill()

def draw_hatch(ctx, x, y, w, h, orientation):
    """Systematic line repetition with varying weights."""
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(0.8, 0.8, 0.8, 0.4)
    step = 4
    if orientation == 'v':
        for i in range(0, int(w), step):
            ctx.move_to(x + i, y)
            ctx.line_to(x + i, y + h)
    else:
        for i in range(0, int(h), step):
            ctx.move_to(x, y + i)
            ctx.line_to(x + w, y + i)
    ctx.stroke()

def draw_spectral_glow(ctx, x, y, w, h):
    """Adds atmospheric diffusion / light bleed."""
    gradient = cairo.RadialGradient(x + w/2, y + h/2, 2, x + w/2, y + h/2, max(w, h))
    # Chromatic aberration-inspired palette
    colors = [
        (1.0, 0.0, 0.4, 0.15), # Magenta
        (0.0, 0.8, 1.0, 0.1),  # Cyan
        (0.0, 0.0, 0.0, 0.0)   # Transparent
    ]
    gradient.add_color_stop_rgba(0.0, *colors[0])
    gradient.add_color_stop_rgba(0.4, *colors[1])
    gradient.add_color_stop_rgba(1.0, *colors[2])
    ctx.set_source(gradient)
    ctx.rectangle(x, y, w, h)
    ctx.fill()

def recursive_subdivision(x, y, w, h, depth, horizontal=True):
    """Recursive geometric subdivision using golden ratio proportions."""
    if depth <= 0 or w < 10 or h < 10:
        # Base case: Draw the 'glyph' or texture for this partition
        choice = random.random()
        
        # Subtle border to define the grid
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.set_line_width(0.3)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()

        if choice < 0.3:
            draw_stipple(ctx, x, y, w, h, 0.15)
        elif choice < 0.6:
            draw_hatch(ctx, x, y, w, h, 'v' if random.random() > 0.5 else 'h')
        elif choice < 0.8:
            # High-density motion lines
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.set_line_width(1.2)
            ctx.move_to(x + 2, y + h/2)
            ctx.line_to(x + w - 2, y + h/2)
            ctx.stroke()
        
        # Occasional light bleed
        if random.random() > 0.85:
            draw_spectral_glow(ctx, x, y, w, h)
        return

    # Determine split point using Golden Ratio
    if horizontal:
        div = w / PHI
        recursive_subdivision(x, y, div, h, depth - 1, not horizontal)
        recursive_subdivision(x + div, y, w - div, h, depth - 1, not horizontal)
    else:
        div = h / PHI
        recursive_subdivision(x, y, w, div, depth - 1, not horizontal)
        recursive_subdivision(x, y + div, w, h - div, depth - 1, not horizontal)

# Start recursion from center-weighted area
padding = 40
main_w, main_h = width - padding*2, height - padding*2
recursive_subdivision(padding, padding, main_w, main_h, depth=8)

# Add "Temporal Vibration" - Overlapping ghost grid
ctx.set_operator(cairo.OPERATOR_ADD)
for i in range(3):
    offset = i * 1.5
    ctx.set_source_rgba(0.1, 0.4, 0.8, 0.05)
    ctx.set_line_width(0.5)
    # Draw a few large-scale rhythmic lines
    for j in range(5):
        pos = (main_w / 5) * j + padding + offset
        ctx.move_to(pos, padding)
        ctx.line_to(pos, height - padding)
        ctx.stroke()

# Finishing touches: sharpen certain edges
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(2)
ctx.move_to(padding, padding)
ctx.line_to(padding + main_w, padding)
ctx.stroke()
ctx.move_to(padding, height - padding)
ctx.line_to(padding + main_w, height - padding)
ctx.stroke()

