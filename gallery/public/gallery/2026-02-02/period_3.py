import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Golden Ratio Constant
PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI

# Color Palette: Deep Cobalt, Stark White, Signal Red
BG_COLOR = (0.01, 0.02, 0.05)
LINE_COLOR = (0.9, 0.9, 1.0)
ACCENT_COLOR = (1.0, 0.2, 0.1)
COBALT = (0.1, 0.3, 0.8)

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

nodes = []

def draw_halftone(ctx, x, y, w, h, density=4):
    """Draws a technical dithered/halftone pattern within a region."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    step = max(2, int(w / density))
    for i in range(0, int(w), step):
        for j in range(0, int(h), step):
            if (i + j) % 3 == 0:
                ctx.set_source_rgba(1, 1, 1, 0.15)
                ctx.rectangle(x + i, y + j, 1, 1)
                ctx.fill()
    ctx.restore()

def draw_label(ctx, x, y, text_val):
    """Simulates typographic noise/data labels."""
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(0.5)
    # Draw tiny faux-glyph
    ctx.move_to(x + 2, y - 2)
    ctx.line_to(x + 8, y - 2)
    ctx.stroke()
    # Draw binary string representation
    if random.random() > 0.5:
        ctx.set_source_rgba(0.1, 0.3, 0.8, 0.5)
        ctx.rectangle(x + 2, y + 2, 4, 2)
        ctx.fill()

def subdivide(x, y, w, h, depth, orientation):
    if depth <= 0:
        return

    nodes.append((x + w/2, y + h/2))
    
    # Draw boundary
    ctx.set_source_rgba(1, 1, 1, 0.1 + (depth * 0.05))
    ctx.set_line_width(0.5)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Visual texture inside the box
    if depth < 4 and random.random() > 0.6:
        draw_halftone(ctx, x, y, w, h, density=random.randint(5, 15))

    # Calculate split point using Golden Ratio
    if orientation == 'v':
        split = w * INV_PHI
        # Split into a square and a smaller rectangle
        if random.random() > 0.2:
            subdivide(x, y, split, h, depth - 1, 'h')
            subdivide(x + split, y, w - split, h, depth - 1, 'h')
        else: # Occasional asymmetry/break in logic
            draw_label(ctx, x + 5, y + 10, depth)
    else:
        split = h * INV_PHI
        if random.random() > 0.2:
            subdivide(x, y, w, split, depth - 1, 'v')
            subdivide(x, y + split, w, h - split, depth - 1, 'v')
        else:
            # Highlight a "logical anomaly"
            ctx.set_source_rgba(*ACCENT_COLOR, 0.8)
            ctx.rectangle(x + 2, y + 2, 3, 3)
            ctx.fill()

# 1. Main Recursive Subdivision
subdivide(40, 40, width - 80, height - 80, 7, 'v')

# 2. Point-to-Point Connectivity Layer
# Connect nodes that are within a certain "functional proximity"
ctx.set_line_width(0.3)
for i, p1 in enumerate(nodes):
    for p2 in nodes[i+1:]:
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if 30 < dist < 80:
            ctx.set_source_rgba(0.1, 0.3, 0.8, 0.2)
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(p2[0], p2[1])
            ctx.stroke()

# 3. Geometric Pulses (Rhythmic tension points)
for _ in range(12):
    node = random.choice(nodes)
    ctx.set_source_rgba(*ACCENT_COLOR, 0.9)
    ctx.arc(node[0], node[1], 1.5, 0, 2 * math.pi)
    ctx.fill()
    
    # Concentric ghost circles
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.arc(node[0], node[1], 8, 0, 2 * math.pi)
    ctx.stroke()

# 4. Global Logarithmic Grid Overlay (Subtle)
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.05)
for i in range(15):
    pos = width * (1 - math.exp(-i * 0.2))
    ctx.move_to(pos, 0)
    ctx.line_to(pos, height)
    ctx.stroke()

# 5. Typographic Noise/Data Stream (Bottom Edge)
for i in range(20):
    tx = 40 + (i * 25)
    ty = height - 25
    ctx.set_source_rgba(1, 1, 1, 0.4)
    if random.random() > 0.3:
        ctx.rectangle(tx, ty, 10, 1)
        ctx.fill()
    if random.random() > 0.8:
        ctx.set_source_rgb(*ACCENT_COLOR)
        ctx.rectangle(tx, ty - 5, 2, 2)
        ctx.fill()

# Final Polish: Central Axis Marker
ctx.set_source_rgba(0.1, 0.3, 0.8, 0.4)
ctx.set_line_width(1)
ctx.move_to(width/2, 40)
ctx.line_to(width/2, height-40)
ctx.set_dash([10, 5])
ctx.stroke()

