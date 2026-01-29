import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
rings = 18
segments = 40
inner_radius = 20
max_radius = 320

def to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

def draw_glyph(ctx, x, y, size, type_id):
    """Draws technical primitives based on a 'biome' ID."""
    ctx.set_line_width(0.5)
    if type_id < 0.3: # Cross
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
    elif type_id < 0.6: # Circle node
        ctx.arc(x, y, size * 0.7, 0, math.pi * 2)
        ctx.stroke()
    elif type_id < 0.85: # Parallel hatch
        ctx.move_to(x - size, y - size)
        ctx.line_to(x + size, y + size)
        ctx.move_to(x - size*0.5, y - size)
        ctx.line_to(x + size, y + size*0.5)
        ctx.stroke()
    else: # Tiny dot
        ctx.arc(x, y, 0.8, 0, math.pi * 2)
        ctx.fill()

# 1. Generate Data Structure
nodes = []
for i in range(rings):
    r_base = inner_radius + (i / rings) * max_radius
    # Exponential spacing for centripetal density
    r_log = inner_radius + math.pow(i / rings, 1.2) * max_radius
    
    # Mathematical distortion: Sine-wave radial warping
    r_distort = 15 * math.sin(i * 0.5) 
    
    current_segments = int(segments * (1 + i * 0.2)) # More segments as we go out
    for j in range(current_segments):
        theta = (j / current_segments) * 2 * math.pi
        
        # Apply distortion to the grid
        final_r = r_log + r_distort * math.cos(theta * 3)
        x, y = to_cartesian(final_r, theta)
        
        # Determine "Biome" based on quadrant and radius
        biome_val = (math.sin(theta * 2) + math.cos(i * 0.5)) / 2 + 0.5
        nodes.append({
            'pos': (x, y),
            'r': final_r,
            'theta': theta,
            'biome': random.random(), # Mixes entropy with the systematic grid
            'ring': i
        })

# 2. Draw Relational Vectors (The Network)
# Only connect nodes within specific distance thresholds to simulate emergent paths
ctx.set_source_rgba(0.9, 0.9, 0.95, 0.15)
ctx.set_line_width(0.2)
for i in range(0, len(nodes), 3):
    p1 = nodes[i]['pos']
    # Connect to a neighbor in the same ring or adjacent ring
    for j in range(i + 1, min(i + 20, len(nodes))):
        p2 = nodes[j]['pos']
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if 5 < dist < 45:
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()

# 3. Draw Modular Primitives
for node in nodes:
    x, y = node['pos']
    
    # Scalar modulation: lines get thinner and smaller further from center
    scale = max(0.2, 1.0 - (node['r'] / max_radius))
    alpha = max(0.3, 1.0 - (node['r'] / max_radius) * 0.7)
    
    ctx.set_source_rgba(0.98, 0.98, 1.0, alpha)
    
    # Use ring index to vary primitive size
    glyph_size = 1.5 + (node['ring'] % 3)
    draw_glyph(ctx, x, y, glyph_size * scale, node['biome'])

# 4. Global Structural Elements (Swiss Overlays)
# Draw subtle concentric reference guides
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.4)
for r in [100, 200, 300]:
    ctx.arc(center_x, center_y, r, 0, math.pi * 2)
    ctx.stroke()

# Crosshair / Margin markers
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.set_line_width(1.0)
m = 40 # Margin
# Corner Brackets
bracket_len = 15
corners = [(m, m), (width-m, m), (m, height-m), (width-m, height-m)]
for cx, cy in corners:
    dx = bracket_len if cx == m else -bracket_len
    dy = bracket_len if cy == m else -bracket_len
    ctx.move_to(cx, cy)
    ctx.line_to(cx + dx, cy)
    ctx.move_to(cx, cy)
    ctx.line_to(cx, cy + dy)
    ctx.stroke()

# Technical labels (Simulated with lines)
def draw_label(x, y, align_right=False):
    ctx.set_line_width(0.7)
    ctx.set_source_rgba(0.9, 0.9, 1.0, 0.6)
    direction = -1 if align_right else 1
    ctx.move_to(x, y)
    ctx.line_to(x + 40 * direction, y)
    ctx.stroke()
    # Tiny "data" bars
    for i in range(4):
        ctx.rectangle(x + (i*6 + 5)*direction, y + 4, 3, 2)
        ctx.fill()

draw_label(m + 20, height - m)
draw_label(width - m - 20, m, align_right=True)

# Central Core (high density entropy)
ctx.set_source_rgba(1, 1, 1, 0.8)
for _ in range(150):
    ang = random.uniform(0, math.pi * 2)
    rad = random.uniform(0, inner_radius * 1.5)
    ctx.arc(center_x + math.cos(ang)*rad, center_y + math.sin(ang)*rad, 0.5, 0, math.pi*2)
    ctx.fill()

