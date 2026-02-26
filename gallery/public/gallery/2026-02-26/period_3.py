import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Technical Deep Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration for Schematic Abstraction
cx, cy = width / 2, height / 2
num_rings = 45
num_sectors = 72
max_radius = min(width, height) * 0.45

def get_distorted_coords(r_idx, theta_idx):
    """Calculates polar-to-cartesian with radial distortion field."""
    # Base radius with a slight logarithmic expansion for hierarchy
    base_r = (r_idx / num_rings) ** 1.1 * max_radius
    angle = (theta_idx / num_sectors) * 2 * math.pi
    
    # Distortion logic: Sinusoidal interference pattern
    # Creates "Information Topography" peaks and valleys
    distortion = 12 * math.sin(r_idx * 0.2 + angle * 4) 
    distortion += 8 * math.cos(angle * 8 - r_idx * 0.1)
    
    current_r = base_r + distortion
    
    # Apply transformation
    x = cx + current_r * math.cos(angle)
    y = cy + current_r * math.sin(angle)
    return x, y

# 1. DRAW MESH / VECTOR GRAPH (The Schematic Base)
ctx.set_line_width(0.4)
for r in range(num_rings):
    # Modulate alpha based on radius to create depth/fading
    alpha = 0.1 + (0.4 * (1 - r/num_rings))
    ctx.set_source_rgba(0.0, 0.8, 1.0, alpha) # Technical Cyan
    
    for s in range(num_sectors):
        x1, y1 = get_distorted_coords(r, s)
        x2, y2 = get_distorted_coords(r, (s + 1) % num_sectors)
        
        # Draw radial arcs (ring segments)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # Draw spokes (connecting rings)
        if r < num_rings - 1:
            x3, y3 = get_distorted_coords(r + 1, s)
            ctx.move_to(x1, y1)
            ctx.line_to(x3, y3)
            ctx.stroke()

# 2. PRIMITIVE SUBSTITUTION (The Data Nodes)
# Placing markers at specific intervals to simulate a node-link architecture
for r in range(0, num_rings, 4):
    for s in range(0, num_sectors, 6):
        x, y = get_distorted_coords(r, s)
        
        # Logic-based primitive selection
        importance = (math.sin(r * 0.5) + math.cos(s * 0.2)) / 2
        
        ctx.set_source_rgba(1, 1, 1, 0.7)
        if importance > 0.6:
            # Draw a Cross (Primary Node)
            size = 3
            ctx.set_line_width(1.0)
            ctx.move_to(x - size, y)
            ctx.line_to(x + size, y)
            ctx.move_to(x, y - size)
            ctx.line_to(x, y + size)
            ctx.stroke()
        elif importance < -0.2:
            # Draw a tiny Square (Secondary Node)
            ctx.rectangle(x - 1, y - 1, 2, 2)
            ctx.fill()
        else:
            # Draw a subtle circle
            ctx.arc(x, y, 0.8, 0, 2 * math.pi)
            ctx.fill()

# 3. MOIRÉ INTERFERENCE LAYERS
# Adding fine, non-distorted secondary grid for spatial reference
ctx.set_source_rgba(0.5, 0.6, 0.7, 0.05)
ctx.set_line_width(0.2)
for i in range(0, width, 20):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, 20):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 4. SWISS ANNOTATIONS (Marginalia)
# Systematic text-like blocks to imply technical data
def draw_data_block(x, y, rows):
    ctx.set_source_rgba(0.0, 0.8, 1.0, 0.6)
    for i in range(rows):
        w = random.uniform(10, 40)
        ctx.rectangle(x, y + (i * 4), w, 1.5)
        ctx.fill()

# Top Left Block
draw_data_block(30, 30, 8)
# Bottom Right Block
draw_data_block(width - 70, height - 50, 5)

# 5. DIRECTIONAL TENSION (Center Focus)
# High-contrast core element
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(1.5)
ctx.arc(cx, cy, 4, 0, 2 * math.pi)
ctx.stroke()
ctx.set_line_width(0.5)
ctx.arc(cx, cy, 10, 0, 2 * math.pi)
ctx.stroke()

# Final subtle highlight - sweeping arc indicating a 'scan' or 'threshold'
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.15)
ctx.set_line_width(20)
ctx.arc(cx, cy, max_radius * 0.8, 4.5, 5.2)
ctx.stroke()

