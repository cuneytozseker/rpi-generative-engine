import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)  # Deep near-black
ctx.paint()

# Constants
PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI
ACCENT_COLOR = (0.0, 0.8, 1.0) # Technical Cyan
NODES = []

def draw_technical_marker(x, y, size):
    """Draws a small crosshair or coordinate marker."""
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(0.8, 0.8, 0.8, 0.6)
    
    # Crosshair
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    
    # Micro-rect
    if random.random() > 0.5:
        ctx.rectangle(x + 2, y + 2, size/2, size/4)
        ctx.fill()

def draw_data_cluster(x, y, w, h, density):
    """Fills a region with high-density informational primitives."""
    ctx.set_line_width(0.3)
    steps = int(density * 10)
    for i in range(steps):
        # Vertical bars of varying height
        vx = x + (i/steps) * w
        vh = random.uniform(2, h * 0.8)
        ctx.set_source_rgba(0.9, 0.9, 0.9, random.uniform(0.1, 0.5))
        ctx.rectangle(vx, y + (h - vh)/2, 1, vh)
        ctx.fill()

def recursive_subdivide(x, y, w, h, depth, horizontal=True):
    """Golden ratio subdivision with varying functional contents."""
    if depth <= 0 or w < 10 or h < 10:
        # Terminal leaf node: draw content
        NODES.append((x + w/2, y + h/2))
        
        style = random.random()
        if style < 0.3:
            # High density data cluster
            draw_data_cluster(x + 2, y + 2, w - 4, h - 4, random.uniform(5, 15))
        elif style < 0.6:
            # Geometric boundary with inner node
            ctx.set_source_rgba(1, 1, 1, 0.1)
            ctx.rectangle(x, y, w, h)
            ctx.stroke()
            ctx.arc(x + w/2, y + h/2, min(w, h) * 0.1, 0, 2*math.pi)
            ctx.set_source_rgba(*ACCENT_COLOR, 0.8)
            ctx.fill()
        elif style < 0.8:
            # Technical "blueprint" lines
            ctx.set_source_rgba(0.5, 0.5, 0.5, 0.3)
            ctx.set_line_width(0.4)
            for i in range(0, int(w), 4):
                ctx.move_to(x + i, y)
                ctx.line_to(x + i, y + h)
            ctx.stroke()
        return

    # Determine split point using golden ratio logic
    # Introduce entropy by slightly jittering the split
    entropy = random.uniform(-0.05, 0.05)
    split_pct = INV_PHI + entropy
    
    if horizontal:
        split_w = w * split_pct
        recursive_subdivide(x, y, split_w, h, depth - 1, not horizontal)
        recursive_subdivide(x + split_w, y, w - split_w, h, depth - 1, not horizontal)
        
        # Draw structural divider
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.set_line_width(0.7)
        ctx.move_to(x + split_w, y)
        ctx.line_to(x + split_w, y + h)
        ctx.stroke()
    else:
        split_h = h * split_pct
        recursive_subdivide(x, y, w, split_h, depth - 1, not horizontal)
        recursive_subdivide(x, y + split_h, w, h - split_h, depth - 1, not horizontal)
        
        # Draw structural divider
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.set_line_width(0.7)
        ctx.move_to(x, y + split_h)
        ctx.line_to(x + w, y + split_h)
        ctx.stroke()

# Start recursion
random.seed(42) # Ensure structured randomness
recursive_subdivide(20, 20, width - 40, height - 40, 7)

# Layer: Informational Entropy (Vector Paths)
# Connect random nodes from the recursion to suggest a hidden network
ctx.set_line_width(0.2)
for _ in range(15):
    p1 = random.choice(NODES)
    p2 = random.choice(NODES)
    
    # Path with "glitch" deviation
    ctx.set_source_rgba(0, 0.8, 1.0, 0.3)
    ctx.move_to(p1[0], p1[1])
    # Create a step-like path (orthogonal)
    mid_x = p1[0] + (p2[0] - p1[0]) * random.random()
    ctx.line_to(mid_x, p1[1])
    ctx.line_to(mid_x, p2[1])
    ctx.line_to(p2[0], p2[1])
    ctx.stroke()
    
    # Add a marker at the junction
    draw_technical_marker(mid_x, p2[1], 3)

# Layer: Global Hierarchy Overlay
# Subtle large-scale geometric sweeps to unify the composition
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(1.0)
ctx.arc(width/2, height/2, height * 0.4, 0, 2 * math.pi)
ctx.stroke()

ctx.rectangle(10, 10, width - 20, height - 20)
ctx.set_line_width(0.5)
ctx.stroke()

# Final Annotations: Micro-labels
for _ in range(20):
    tx = random.uniform(50, width-50)
    ty = random.uniform(50, height-50)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    # Drawing tiny "bit" blocks
    for i in range(3):
        if random.random() > 0.3:
            ctx.rectangle(tx + (i*4), ty, 2, 2)
            ctx.fill()

# Clean high-contrast accenting
ctx.set_source_rgba(*ACCENT_COLOR, 0.4)
ctx.set_line_width(2)
ctx.move_to(20, 20)
ctx.line_to(60, 20)
ctx.move_to(20, 20)
ctx.line_to(20, 60)
ctx.stroke()

