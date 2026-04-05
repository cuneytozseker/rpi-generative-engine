import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal / Indigo
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

PHI = (1 + math.sqrt(5)) / 2
INV_PHI = 1 / PHI

# Storage for node connections to create the "mapping" feel
nodes = []

def draw_glpyh(x, y, size, style):
    """Draws a functional data-marker at a specific coordinate."""
    ctx.set_line_width(0.5)
    if style == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
    elif style == "circle":
        ctx.arc(x, y, size, 0, 2 * math.pi)
    elif style == "dot":
        ctx.arc(x, y, 0.8, 0, 2 * math.pi)
        ctx.fill()
    ctx.stroke()

def draw_grid_unit(x, y, w, h, depth):
    """Fills a subdivision with systemic cartographic details."""
    
    # Draw ultra-fine grid (Hairlines)
    ctx.set_source_rgba(0.4, 0.4, 0.5, 0.2)
    ctx.set_line_width(0.15)
    
    steps = 4
    for i in range(steps + 1):
        # Vertical lines
        lx = x + (i / steps) * w
        ctx.move_to(lx, y)
        ctx.line_to(lx, y + h)
        # Horizontal lines
        ly = y + (i / steps) * h
        ctx.move_to(x, ly)
        ctx.line_to(x + w, ly)
    ctx.stroke()

    # Probability-based "Data Hub" identification
    is_hub = random.random() > 0.7 and depth > 3
    
    if is_hub:
        # Accent Color (Fluorescent Cyan or Magenta)
        if random.random() > 0.5:
            ctx.set_source_rgb(0.0, 1.0, 0.8) # Cyan
        else:
            ctx.set_source_rgb(1.0, 0.1, 0.4) # Magenta
        
        # Central Marker
        draw_glpyh(x + w/2, y + h/2, 3, "circle")
        
        # Diagonal Vector paths
        ctx.set_line_width(0.3)
        ctx.move_to(x, y)
        ctx.line_to(x + w, y + h)
        ctx.stroke()
        
        # Record node for later interconnectivity
        nodes.append((x + w/2, y + h/2))
    else:
        # Subtle "topographic" scatter
        ctx.set_source_rgba(0.7, 0.7, 0.8, 0.4)
        if w > 10:
            draw_glpyh(x + w * 0.2, y + h * 0.8, 1, "dot")
            draw_glpyh(x + w * 0.8, y + h * 0.2, 1, "dot")

def subdivide(x, y, w, h, depth, max_depth):
    if depth >= max_depth:
        draw_grid_unit(x, y, w, h, depth)
        return

    # Draw the boundary of the current subdivision
    ctx.set_source_rgba(0.5, 0.5, 0.6, 0.15)
    ctx.set_line_width(0.4)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Determine split direction based on aspect ratio
    # Applying PHI-based subdivision
    if w > h:
        split = w * INV_PHI
        # Randomly flip the split side to create "data-informed asymmetry"
        if random.random() > 0.5:
            subdivide(x, y, split, h, depth + 1, max_depth)
            subdivide(x + split, y, w - split, h, depth + 1, max_depth)
        else:
            subdivide(x, y, w - split, h, depth + 1, max_depth)
            subdivide(x + (w - split), y, split, h, depth + 1, max_depth)
    else:
        split = h * INV_PHI
        if random.random() > 0.5:
            subdivide(x, y, w, split, depth + 1, max_depth)
            subdivide(x, y + split, w, h - split, depth + 1, max_depth)
        else:
            subdivide(x, y, w, h - split, depth + 1, max_depth)
            subdivide(x, y + (h - split), w, split, depth + 1, max_depth)

# Initial execution
subdivide(40, 40, width - 80, height - 80, 0, 8)

# Post-processing: Node-and-link architecture
# Connect nearby hubs with structural vectors
ctx.set_line_width(0.2)
ctx.set_dash([2, 4]) # Dashed lines for "inferred" connections
for i, (x1, y1) in enumerate(nodes):
    for x2, y2 in nodes[i+1:]:
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        if dist < 120:
            ctx.set_source_rgba(1, 1, 1, 0.15)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

# Final border to ground the composition
ctx.set_dash([])
ctx.set_line_width(2)
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.rectangle(20, 20, width - 40, height - 40)
ctx.stroke()

# Tiny technical labels (Swiss Style)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(8)
ctx.move_to(30, height - 25)
ctx.show_text("REF: SYSTEMIC_CARTOGRAPHY // GOLDEN_RATIO_RECURSION")
ctx.move_to(width - 120, height - 25)
ctx.show_text(f"NODES_ACTIVE: {len(nodes)}")

