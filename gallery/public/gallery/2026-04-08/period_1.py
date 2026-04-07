import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Technical Navy
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
rings = 45
segments = 80
base_radius = 5
radius_step = 6

def get_polar_coord(r_idx, theta_idx, total_rings, total_segments):
    """Calculates a distorted polar coordinate based on radial and angular indices."""
    # Normalize inputs
    norm_r = r_idx / total_rings
    angle = (theta_idx / total_segments) * 2 * math.pi
    
    # Mathematical distortion forces
    # 1. Harmonic oscillation of the radius
    r_offset = math.sin(angle * 3 + norm_r * 5) * 15
    r_offset += math.cos(angle * 8 - norm_r * 10) * 8
    
    # 2. Angular drift (torsion)
    theta_offset = math.sin(norm_r * math.pi * 2) * 0.3
    
    final_r = base_radius + (r_idx * radius_step) + r_offset
    final_theta = angle + theta_offset
    
    x = cx + final_r * math.cos(final_theta)
    y = cy + final_r * math.sin(final_theta)
    
    return x, y, final_theta

# Layer 1: The "Substrate" (Faint structural grid)
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.2, 0.4, 0.6, 0.15)

for r in range(rings):
    if r % 5 == 0: # Only draw some structural rings
        for s in range(segments + 1):
            x, y, _ = get_polar_coord(r, s, rings, segments)
            if s == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.stroke()

# Layer 2: "Data Currents" (Dynamic line fragments)
# We create segments that follow the flow field logic
for r in range(5, rings, 2):
    # Stochastic density: skip some rings or segments
    if random.random() > 0.8: continue
    
    for s in range(0, segments):
        # Determine if we draw a segment here based on "Information Density"
        # Using a mathematical threshold to create asymmetric clusters
        density_map = math.sin(s * 0.1) * math.cos(r * 0.2)
        if density_map > 0.3:
            x1, y1, t1 = get_polar_coord(r, s, rings, segments)
            x2, y2, t2 = get_polar_coord(r, s + 1.5, rings, segments)
            
            # Color based on radial position (Technical Cyan to White)
            ctx.set_source_rgba(0.3, 0.8, 1.0, 0.6)
            ctx.set_line_width(0.8)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            
            # Occasional highlight "nodes"
            if random.random() > 0.96:
                ctx.set_source_rgb(1, 1, 1)
                ctx.arc(x1, y1, 1.5, 0, 2 * math.pi)
                ctx.fill()

# Layer 3: Swiss Primitives (Rectangles aligned to tangents)
# This adds the rigid, systemic feel to the fluid distortion
for r in range(10, rings, 4):
    for s in range(0, segments, 4):
        # Spatial organization: create gaps in the grid
        if (s // 4 + r // 4) % 3 == 0: continue
        
        x, y, angle = get_polar_coord(r, s, rings, segments)
        
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(angle)
        
        # Varying weight and size based on distance
        rect_w = random.uniform(2, 8)
        rect_h = 1.5
        
        # Swiss Red accent in specific zones
        if r > rings * 0.7 and 20 < s < 40:
            ctx.set_source_rgb(0.9, 0.2, 0.2)
        else:
            ctx.set_source_rgb(0.9, 0.9, 0.9)
            
        ctx.rectangle(-rect_w/2, -rect_h/2, rect_w, rect_h)
        ctx.fill()
        ctx.restore()

# Layer 4: Radial Hierarchy / Marginalia
# Small glyph-like markers at the outer edge
ctx.set_source_rgb(0.5, 0.6, 0.7)
ctx.set_line_width(0.5)
for s in range(0, segments, 2):
    x_inner, y_inner, a = get_polar_coord(rings - 2, s, rings, segments)
    x_outer, y_outer, _ = get_polar_coord(rings + 1, s, rings, segments)
    
    ctx.move_to(x_inner, y_inner)
    ctx.line_to(x_outer, y_outer)
    ctx.stroke()
    
    # Tick marks
    if s % 10 == 0:
        ctx.save()
        ctx.translate(x_outer, y_outer)
        ctx.rotate(a)
        ctx.rectangle(2, -0.5, 10, 1)
        ctx.fill()
        ctx.restore()

# Final Polish: Center Core (Negative Space contrast)
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.arc(cx, cy, 20, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(0.5)
ctx.arc(cx, cy, 5, 0, 2 * math.pi)
ctx.stroke()

# Crosshair in the center
ctx.move_to(cx - 10, cy); ctx.line_to(cx + 10, cy)
ctx.move_to(cx, cy - 10); ctx.line_to(cx, cy + 10)
ctx.stroke()
