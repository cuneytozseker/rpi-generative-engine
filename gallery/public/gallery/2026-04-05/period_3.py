import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Golden Ratio constant
PHI = (1 + 5**0.5) / 2

# Aesthetics: Carbon Black background and Blueprint Cyan signal
BG_COLOR = (0.02, 0.02, 0.03)
SIGNAL_COLOR = (0.0, 0.9, 1.0) # High-visibility cyan
WHITE = (1, 1, 1)

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def draw_node(x, y, size=1.5):
    """Draws a technical anchor point."""
    ctx.arc(x, y, size, 0, 2 * math.pi)
    ctx.fill()

def draw_technical_lines(x, y, w, h, depth):
    """Draws schematics inside a cell based on depth."""
    ctx.set_line_width(0.4 if depth > 3 else 0.8)
    alpha = max(0.2, 1.0 - (depth * 0.12))
    r, g, b = SIGNAL_COLOR
    ctx.set_source_rgba(r, g, b, alpha)

    # Draw border
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Draw nodes at corners
    draw_node(x, y)
    draw_node(x + w, y + h)

    # Internal Logic: Fan lines or cross-hatching based on orientation
    if depth % 2 == 0:
        # Fan lines from top-left
        num_lines = 8
        for i in range(num_lines + 1):
            ctx.move_to(x, y)
            ctx.line_to(x + (i * w / num_lines), y + h)
            ctx.stroke()
    else:
        # Concentric partial arcs
        ctx.set_line_width(0.2)
        for i in range(1, 5):
            radius = (w if w < h else h) * (i / 5)
            ctx.arc(x + w, y, radius, math.pi / 2, math.pi)
            ctx.stroke()

def subdivide(x, y, w, h, depth, max_depth):
    """Recursively subdivide space using the Golden Ratio."""
    if depth >= max_depth or w < 10 or h < 10:
        return

    # Draw the systemic elements for this cell
    draw_technical_lines(x, y, w, h, depth)

    # Determine split direction based on aspect ratio
    if w > h:
        # Split width
        w_prime = w / PHI
        # Recurse on the larger section then the smaller
        subdivide(x, y, w_prime, h, depth + 1, max_depth)
        subdivide(x + w_prime, y, w - w_prime, h, depth + 1, max_depth)
    else:
        # Split height
        h_prime = h / PHI
        subdivide(x, y, w, h_prime, depth + 1, max_depth)
        subdivide(x, y + h_prime, w, h - h_prime, depth + 1, max_depth)

# Main Generative Process
# 1. Background Grid (Systemic Foundation)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
grid_size = 40
for i in range(0, width, grid_size):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, grid_size):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. Golden Subdivision (The Core System)
# We start with a centered golden rectangle
rect_w = 500
rect_h = rect_w / PHI
offset_x = (width - rect_w) / 2
offset_y = (height - rect_h) / 2

subdivide(offset_x, offset_y, rect_w, rect_h, 0, 10)

# 3. Interconnected Network (The Data Flow)
# Connecting random focal points within the recursive logic
points = []
for _ in range(12):
    px = offset_x + random.random() * rect_w
    py = offset_y + random.random() * rect_h
    points.append((px, py))

ctx.set_line_width(0.3)
for i, p1 in enumerate(points):
    for p2 in points[i+1:]:
        if math.dist(p1, p2) < 200:
            ctx.set_source_rgba(1, 1, 1, 0.3)
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(p2[0], p2[1])
            ctx.stroke()
            
            # Intersection indicators
            ctx.set_source_rgba(*SIGNAL_COLOR, 0.6)
            ctx.arc(p1[0], p1[1], 1, 0, 2*math.pi)
            ctx.fill()

# 4. Asymmetrical Marginalia (Swiss Precision)
ctx.set_source_rgb(0.8, 0.8, 0.8)
font_size = 8
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(font_size)

# Metadata labels
ctx.move_to(20, 25)
ctx.show_text("REF_SYS: GOLDEN_RATIO_SUBDIVISION")
ctx.move_to(20, 35)
ctx.show_text(f"COORDS: {width}x{height}")
ctx.move_to(20, 45)
ctx.show_text("SCALE: 1:PHI")

# Visual rhythm: Small bars
for i in range(5):
    ctx.rectangle(width - 40, 20 + (i*8), 20, 4)
    if i == 2: ctx.set_source_rgb(*SIGNAL_COLOR)
    else: ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.fill()

# Final focal circle to break the rigid grid (Asymmetrical equilibrium)
ctx.set_source_rgba(*SIGNAL_COLOR, 0.1)
ctx.arc(width * 0.75, height * 0.25, 80, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgba(*SIGNAL_COLOR, 0.8)
ctx.set_line_width(1.5)
ctx.arc(width * 0.75, height * 0.25, 80, 0, math.pi * 0.5)
ctx.stroke()

