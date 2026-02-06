import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Neutral
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def draw_truchet_tile(x, y, size, variant, color, weight):
    """Draws a technical-style Truchet tile with arcs and nodal points."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    # Rounded arc paths (Smith-style Truchet)
    if variant == 0:
        # Arc top-left and bottom-right
        ctx.arc(x, y, size / 2, 0, 0.5 * math.pi)
        ctx.stroke()
        ctx.arc(x + size, y + size, size / 2, math.pi, 1.5 * math.pi)
        ctx.stroke()
    else:
        # Arc top-right and bottom-left
        ctx.arc(x + size, y, size / 2, 0.5 * math.pi, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, size / 2, 1.5 * math.pi, 2 * math.pi)
        ctx.stroke()

    # Technical "Nodal" points at the midpoints of the edges
    # These create the "signal" clusters
    ctx.set_source_rgba(color[0], color[1], color[2], color[3] * 0.8)
    node_size = weight * 1.5
    nodes = [(x + size/2, y), (x + size/2, y + size), (x, y + size/2), (x + size, y + size/2)]
    for nx, ny in nodes:
        if random.random() > 0.7:
            ctx.arc(nx, ny, node_size, 0, 2 * math.pi)
            ctx.fill()

def recursive_subdivide(x, y, size, depth, max_depth):
    """Partitions the plane into hierarchical scales based on proximity to centers of interest."""
    # Distance-based entropy: smaller subdivisions near a 'signal' point
    dist_to_center = math.sqrt((x + size/2 - width/2)**2 + (y + size/2 - height/2)**2)
    normalize_dist = dist_to_center / (width / 1.5)
    
    # Probability of splitting increases near the center or randomly
    split_chance = 0.6 * (1.0 - normalize_dist) + 0.2
    
    if depth < max_depth and random.random() < split_chance:
        new_size = size / 2
        recursive_subdivide(x, y, new_size, depth + 1, max_depth)
        recursive_subdivide(x + new_size, y, new_size, depth + 1, max_depth)
        recursive_subdivide(x, y + new_size, new_size, depth + 1, max_depth)
        recursive_subdivide(x + new_size, y + new_size, new_size, depth + 1, max_depth)
    else:
        # Style parameters
        variant = random.randint(0, 1)
        
        # Determine color and weight based on depth
        # Higher depth (smaller tiles) gets finer lines and brighter colors
        if depth % 2 == 0:
            color = (0.9, 0.9, 0.9, 0.7) # White/Technical grey
            weight = 0.5 + (max_depth - depth) * 0.3
        else:
            # Occasional primary accent (Swiss Red)
            if random.random() > 0.85:
                color = (0.85, 0.1, 0.1, 0.8)
            else:
                color = (0.4, 0.5, 0.6, 0.5) # Muted Blueprint Blue
            weight = 0.3 + (max_depth - depth) * 0.2
            
        draw_truchet_tile(x, y, size, variant, color, weight)

# --- Layer 1: Background Noise / Data Cartography ---
# Fine hairline paths connecting random nodes across the grid
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.3, 0.3, 0.4, 0.2)
for _ in range(40):
    ctx.move_to(random.random() * width, random.random() * height)
    ctx.line_to(random.random() * width, random.random() * height)
    ctx.stroke()

# --- Layer 2: Main Recursive Truchet Composition ---
# We use multiple passes with slightly different offsets to create depth
offsets = [(0, 0), (2, 2)]
for i, (ox, oy) in enumerate(offsets):
    random.seed(42) # Ensure layers align structurally but vary in detail
    grid_size = 120
    for gx in range(0, width, grid_size):
        for gy in range(0, height, grid_size):
            ctx.save()
            ctx.translate(ox, oy)
            if i == 1: # Shadow/Offset layer
                ctx.set_operator(cairo.OPERATOR_OVER)
            recursive_subdivide(gx, gy, grid_size, 0, 4)
            ctx.restore()

# --- Layer 3: Technical Overlays & Rhythmic Punctuation ---
# Overlaying a modular grid of micro-primitives
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.15)
dot_spacing = 20
for dx in range(0, width, dot_spacing):
    for dy in range(0, height, dot_spacing):
        if (dx + dy) % 3 == 0:
            ctx.rectangle(dx - 0.5, dy - 0.5, 1, 1)
            ctx.fill()

# High-contrast "Signal" areas - Small filled rectangles for hierarchy
for _ in range(12):
    sx = random.randint(0, width)
    sy = random.randint(0, height)
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.9)
    ctx.rectangle(sx, sy, 2, 8)
    ctx.fill()
    if random.random() > 0.5:
        ctx.set_source_rgba(0.85, 0.1, 0.1, 1.0)
        ctx.rectangle(sx + 5, sy, 10, 1)
        ctx.fill()

# --- Layer 4: Mathematical Margin Markers ---
# Simulating a technical blueprint or calculation snapshot
ctx.set_source_rgba(0.6, 0.6, 0.7, 0.4)
ctx.set_line_width(0.5)
margin = 20
ctx.move_to(margin, margin)
ctx.line_to(width - margin, margin)
ctx.move_to(margin, height - margin)
ctx.line_to(width - margin, height - margin)
ctx.stroke()

# Tiny vertical scale markers
for mx in range(margin, width - margin, 40):
    ctx.move_to(mx, margin - 3)
    ctx.line_to(mx, margin + 3)
    ctx.stroke()

# Final texture: Subtle noise to break the digital flatness
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.rectangle(random.random() * width, random.random() * height, 0.5, 0.5)
    ctx.fill()

