import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
NUM_SECTORS = 12
NUM_RINGS = 8
LINE_WHITE = (0.95, 0.95, 0.98)

def get_polar_coords(r, theta):
    """Converts polar to Cartesian with a slight radial distortion."""
    # Radial distortion: non-linear expansion to create a 'lens' effect
    distorted_r = MAX_RADIUS * math.pow(r / MAX_RADIUS, 1.2)
    x = CENTER_X + distorted_r * math.cos(theta)
    y = CENTER_Y + distorted_r * math.sin(theta)
    return x, y

def draw_subdivided_cell(r1, r2, a1, a2, depth):
    """Recursively subdivides a polar grid cell based on Swiss modularity."""
    if depth > 3:
        return

    # Random chance to subdivide or draw
    # Probability increases for larger cells or lower depths
    should_subdivide = random.random() < (0.7 / (depth + 1))
    
    if should_subdivide:
        # Split either radially or angularly
        if random.random() > 0.5:
            mid_a = (a1 + a2) / 2
            draw_subdivided_cell(r1, r2, a1, mid_a, depth + 1)
            draw_subdivided_cell(r1, r2, mid_a, a2, depth + 1)
        else:
            mid_r = (r1 + r2) / 2
            draw_subdivided_cell(r1, mid_r, a1, a2, depth + 1)
            draw_subdivided_cell(mid_r, r2, a1, a2, depth + 1)
    else:
        # Draw the cell structure
        ctx.set_line_width(0.4 / (depth + 1))
        alpha = 0.8 / (depth + 1)
        ctx.set_source_rgba(LINE_WHITE[0], LINE_WHITE[1], LINE_WHITE[2], alpha)
        
        # Arc 1
        ctx.new_sub_path()
        ctx.arc(CENTER_X, CENTER_Y, r1, a1, a2)
        ctx.stroke()
        
        # Arc 2
        ctx.new_sub_path()
        ctx.arc(CENTER_X, CENTER_Y, r2, a1, a2)
        ctx.stroke()
        
        # Radial lines
        x1, y1 = get_polar_coords(r1, a1)
        x2, y2 = get_polar_coords(r2, a1)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # Occasional "Network Node" - tiny circles at intersections
        if random.random() > 0.6:
            ctx.set_source_rgba(1, 1, 1, 0.9)
            ctx.arc(x1, y1, 1.2, 0, 2 * math.pi)
            ctx.fill()

# 1. THE UNDERLYING GRID SYSTEM
# Create concentric rings with modulated spacing (Golden Ratio influence)
rings = [0]
current_r = 30
for i in range(NUM_RINGS):
    rings.append(current_r)
    current_r += (MAX_RADIUS - current_r) * 0.35

# 2. GENERATE COMPOSITION
for i in range(len(rings) - 1):
    r_start = rings[i]
    r_end = rings[i+1]
    
    for s in range(NUM_SECTORS):
        angle_start = (s / NUM_SECTORS) * 2 * math.pi
        angle_end = ((s + 1) / NUM_SECTORS) * 2 * math.pi
        
        # Apply recursive subdivision to each primary grid cell
        draw_subdivided_cell(r_start, r_end, angle_start, angle_end, 0)

# 3. GLOBAL CONNECTIVITY (The "Network Density" Layer)
# Draw long-distance chord lines connecting different parts of the system
ctx.set_line_width(0.2)
for _ in range(40):
    r_idx = random.randint(1, len(rings)-1)
    s_idx1 = random.randint(0, NUM_SECTORS-1)
    s_idx2 = random.randint(0, NUM_SECTORS-1)
    
    a1 = (s_idx1 / NUM_SECTORS) * 2 * math.pi
    a2 = (s_idx2 / NUM_SECTORS) * 2 * math.pi
    
    x1, y1 = get_polar_coords(rings[r_idx], a1)
    x2, y2 = get_polar_coords(rings[r_idx], a2)
    
    ctx.set_source_rgba(0.5, 0.7, 1.0, 0.15) # Subtle blue tint for depth
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 4. SWISS TYPOGRAPHIC ANCHORS (Symbolic mapping)
# Adding small numerical markers or glyph-like shapes to suggest precision
for i in range(NUM_SECTORS):
    angle = (i / NUM_SECTORS) * 2 * math.pi
    tx, ty = get_polar_coords(MAX_RADIUS + 15, angle)
    
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.set_line_width(0.8)
    # Draw small "L" markers
    ctx.move_to(tx - 3, ty)
    ctx.line_to(tx + 3, ty)
    ctx.move_to(tx, ty - 3)
    ctx.line_to(tx, ty + 3)
    ctx.stroke()

# 5. CENTRAL VOID / CORE
# High contrast central element
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.arc(CENTER_X, CENTER_Y, 25, 0, 2*math.pi)
ctx.fill()
ctx.set_source_rgb(0.95, 0.95, 0.98)
ctx.set_line_width(1.5)
ctx.arc(CENTER_X, CENTER_Y, 20, 0, 2*math.pi)
ctx.stroke()

# Add a crosshair in the center
ctx.set_line_width(0.5)
ctx.move_to(CENTER_X - 10, CENTER_Y)
ctx.line_to(CENTER_X + 10, CENTER_Y)
ctx.move_to(CENTER_X, CENTER_Y - 10)
ctx.line_to(CENTER_X, CENTER_Y + 10)
ctx.stroke()
