import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for Swiss-style depth
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

def draw_truchet_tile(ctx, x, y, size, variant, color, weight, style="arcs"):
    """
    Renders a single Truchet tile with specific geometric logic.
    style "arcs": Classical Smith tiles.
    style "lines": Diagonal geometric intersections.
    """
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)

    if style == "arcs":
        if variant == 0:
            ctx.arc(x, y, size/2, 0, math.pi/2)
            ctx.stroke()
            ctx.arc(x + size, y + size, size/2, math.pi, 3*math.pi/2)
            ctx.stroke()
        else:
            ctx.arc(x + size, y, size/2, math.pi/2, math.pi)
            ctx.stroke()
            ctx.arc(x, y + size, size/2, 3*math.pi/2, 2*math.pi)
            ctx.stroke()
    else: # Diagonal lines
        if variant == 0:
            ctx.move_to(x + size/2, y)
            ctx.line_to(x, y + size/2)
            ctx.move_to(x + size, y + size/2)
            ctx.line_to(x + size/2, y + size)
        else:
            ctx.move_to(x + size/2, y)
            ctx.line_to(x + size, y + size/2)
            ctx.move_to(x, y + size/2)
            ctx.line_to(x + size/2, y + size)
        ctx.stroke()

def recursive_subdivision(ctx, x, y, size, depth, max_depth):
    """
    Creates a non-linear grid progression using quadtree logic.
    Density is influenced by proximity to the center (centripetal hierarchy).
    """
    cx, cy = x + size/2, y + size/2
    dist_to_center = math.sqrt((cx - width/2)**2 + (cy - height/2)**2)
    
    # Logic: Subdivide if deep enough OR if near center (weighted randomness)
    subdivide_chance = (1.0 - (dist_to_center / (width * 0.7))) * 0.8
    
    if depth < max_depth and (random.random() < subdivide_chance or depth < 2):
        half = size / 2
        recursive_subdivision(ctx, x, y, half, depth + 1, max_depth)
        recursive_subdivision(ctx, x + half, y, half, depth + 1, max_depth)
        recursive_subdivision(ctx, x, y + half, half, depth + 1, max_depth)
        recursive_subdivision(ctx, x + half, y + half, half, depth + 1, max_depth)
    else:
        # Draw the tile at this leaf node
        variant = random.randint(0, 1)
        
        # Color Interaction: Chromatic Interruption
        # Mostly white/grey with rare 'data markers' in saturated cyan
        if random.random() > 0.96:
            color = (0.0, 0.8, 1.0, 0.9) # Cyan accent
            weight = 2.0
        else:
            alpha = max(0.1, 1.0 - (depth * 0.15))
            brightness = 0.6 + (random.random() * 0.4)
            color = (brightness, brightness, brightness, alpha)
            weight = 0.5 + (max_depth - depth) * 0.4
            
        draw_truchet_tile(ctx, x, y, size, variant, color, weight, style="arcs")
        
        # Add "Digital Grain" texture to high-density areas
        if depth >= max_depth - 1 and random.random() > 0.5:
            ctx.set_source_rgba(1, 1, 1, 0.2)
            for _ in range(4):
                ctx.arc(x + random.random()*size, y + random.random()*size, 0.5, 0, 7)
                ctx.fill()

# --- Execution Layers ---

# Layer 1: Background Systematic Grid (Static, low opacity)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.3, 0.3, 0.3, 0.2)
grid_spacing = 40
for i in range(0, width + 1, grid_spacing):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height + 1, grid_spacing):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# Layer 2: Large Transparent "Ghost" Layer
# Creates macroscopic structure
for i in range(0, width, 120):
    for j in range(0, height, 120):
        draw_truchet_tile(ctx, i, j, 120, random.randint(0, 1), (1, 1, 1, 0.05), 8, "arcs")

# Layer 3: Main Recursive Composition
# The core logic of the schematic
recursive_subdivision(ctx, 0, 0, 600, 0, 5)

# Layer 4: Linear Dual-Logic Overlay
# Adds razor-thin vector paths to break the arc-heavy flow
ctx.set_operator(cairo.OPERATOR_ADD) # Lighten overlapping areas
for _ in range(12):
    cell_size = random.choice([60, 120])
    rx = random.randint(0, int(width/cell_size)-1) * cell_size
    ry = random.randint(0, int(height/cell_size)-1) * cell_size
    draw_truchet_tile(ctx, rx, ry, cell_size, random.randint(0, 1), (0.2, 0.2, 0.3, 0.4), 0.3, "lines")

# Visual Rhythm: Final accent dots (Staccato markers)
for _ in range(30):
    ctx.set_source_rgba(1, 1, 1, 0.8)
    px = random.randint(0, width)
    py = random.randint(0, height)
    # Only place if near other elements (simplified)
    ctx.arc(px, py, 1.2, 0, 2*math.pi)
    ctx.fill()

# Clean Swiss Border
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

