import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep midnight
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def draw_spectral_arc(ctx, x, y, size, orient, weight, color):
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    
    # Truchet Logic: Two arcs connecting opposite midpoints of a square
    if orient == 0:
        # Top-left and Bottom-right arcs
        ctx.arc(x, y, size/2, 0, math.pi/2)
        ctx.stroke()
        ctx.arc(x + size, y + size, size/2, math.pi, 3 * math.pi / 2)
        ctx.stroke()
    else:
        # Top-right and Bottom-left arcs
        ctx.arc(x + size, y, size/2, math.pi/2, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, size/2, 3 * math.pi / 2, 2 * math.pi)
        ctx.stroke()

def draw_data_node(ctx, x, y, size):
    # Tiny systemic labels/markers to add "micro-texture"
    ctx.set_source_rgba(0.8, 0.9, 1.0, 0.4)
    ctx.set_line_width(0.5)
    ctx.move_to(x - 2, y - 2)
    ctx.line_to(x + 2, y + 2)
    ctx.move_to(x + 2, y - 2)
    ctx.line_to(x - 2, y + 2)
    ctx.stroke()
    
    if random.random() > 0.95:
        ctx.arc(x, y, 1.5, 0, 2*math.pi)
        ctx.fill()

# Use Additive blending for the "Spectral" light effect
ctx.set_operator(cairo.OPERATOR_ADD)

# Layer 1: The Ethereal Foundation (Large, soft tiles)
grid_size_lg = 80
for i in range(int(width / grid_size_lg) + 1):
    for j in range(int(height / grid_size_lg) + 1):
        x, y = i * grid_size_lg, j * grid_size_lg
        # Random orientation based on a mathematical field
        orient = 1 if (math.sin(i * 0.5) + math.cos(j * 0.5)) > 0 else 0
        
        # Distance from a conceptual "energy center"
        dist = math.sqrt((x - width*0.7)**2 + (y - height*0.3)**2)
        alpha = max(0.02, 0.15 - (dist / 1000))
        
        draw_spectral_arc(ctx, x, y, grid_size_lg, orient, 8, (0.1, 0.2, 0.6, alpha))

# Layer 2: The Primary Blueprint (Medium tiles with "thermal" gradients)
grid_size_md = 40
for i in range(int(width / grid_size_md) + 1):
    for j in range(int(height / grid_size_md) + 1):
        x, y = i * grid_size_md, j * grid_size_md
        
        # Deterministic but complex pattern
        orient = 1 if ((i * j) + i) % 3 == 0 else 0
        
        # Proximity to a diagonal "vector flow"
        line_val = abs(x - y + 100) / 200
        
        # Color shifting based on position (Blue to Magenta)
        r = 0.1 + (0.4 * math.sin(i * 0.2))
        g = 0.3 + (0.2 * math.cos(j * 0.3))
        b = 0.8
        
        weight = 1.5 + (2.0 * math.sin(i * 0.5 + j * 0.5))
        draw_spectral_arc(ctx, x, y, grid_size_md, orient, weight, (r, g, b, 0.4))

# Layer 3: High-Frequency Detail (Tiny hairline grid)
grid_size_sm = 20
ctx.set_operator(cairo.OPERATOR_OVER) # Switch back for sharper details
for i in range(int(width / grid_size_sm) + 1):
    for j in range(int(height / grid_size_sm) + 1):
        x, y = i * grid_size_sm, j * grid_size_sm
        
        # Systematic asymmetry: omit certain areas to create "voids"
        if (i + j) % 7 == 0 or (i % 5 == 0 and j % 3 == 0):
            continue
            
        orient = random.randint(0, 1)
        
        # "Thermal" highlight nodes
        dist_to_hotspot = math.sqrt((x - 450)**2 + (y - 150)**2)
        if dist_to_hotspot < 150:
            color = (0.9, 0.3, 0.5, 0.6) # Saturated Magenta/Pink
            weight = 0.8
        else:
            color = (0.2, 0.7, 1.0, 0.3) # Cyan
            weight = 0.4
            
        draw_spectral_arc(ctx, x, y, grid_size_sm, orient, weight, color)
        
        # Data labeling markers
        if i % 2 == 0 and j % 2 == 0:
            draw_data_node(ctx, x, y, 2)

# Final Polish: Geometric Hierarchy Overlays
# Draw a structural "Brutalist" frame or vector path
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(0.3)
for step in range(0, width, 120):
    ctx.move_to(step, 0)
    ctx.line_to(step, height)
    ctx.stroke()
    
# Large diagonal interference stroke
ctx.set_source_rgba(0.0, 1.0, 0.8, 0.05)
ctx.set_line_width(60)
ctx.move_to(-50, height + 50)
ctx.line_to(width + 50, -50)
ctx.stroke()

# Subtle grain: tiny random points
for _ in range(1000):
    px, py = random.uniform(0, width), random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.2))
    ctx.arc(px, py, 0.5, 0, 2*math.pi)
    ctx.fill()
