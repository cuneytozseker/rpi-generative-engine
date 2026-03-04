import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep "Blueprint" Blue
ctx.set_source_rgb(0.05, 0.1, 0.2)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
rings = 18
segments = 40
inner_radius = 40
outer_radius = 320

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    """Converts polar coordinates to cartesian with radial distortion."""
    # Apply a harmonic radial distortion based on the angle
    r += math.sin(theta * 3) * distortion_factor * 15
    r += math.cos(theta * 5) * distortion_factor * 10
    
    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)
    return x, y

# Generate the Geometric System
for r_idx in range(rings):
    # Normalized radius (0.0 to 1.0)
    nr = r_idx / rings
    current_r = inner_radius + (outer_radius - inner_radius) * nr
    
    # Entropic decay: nodes become less frequent and more distorted at the edges
    distortion = nr * 2.5
    
    # Swiss precision vs. randomness logic
    for s_idx in range(segments):
        # Normalized angle
        theta_start = (s_idx / segments) * 2 * math.pi
        theta_end = ((s_idx + 0.8) / segments) * 2 * math.pi
        
        # Decide what to draw based on density clusters
        # Centered clusters (low nr) vs skeletal voids (high nr)
        cluster_density = math.cos(nr * math.pi * 0.5)
        draw_prob = random.random()
        
        if draw_prob < cluster_density * 0.9 + 0.1:
            # 1. THE RECTANGULAR FRAGMENTS (Vector Flow Field)
            # We draw curved segments as if they were grid-aligned rectangles
            ctx.set_line_width(random.uniform(0.5, 3.5) * (1 - nr + 0.1))
            
            # High-value contrast (Stark White)
            ctx.set_source_rgba(0.95, 0.95, 0.98, random.uniform(0.4, 0.9))
            
            ctx.new_path()
            p1 = polar_to_cartesian(current_r, theta_start, distortion)
            p2 = polar_to_cartesian(current_r, theta_end, distortion)
            p3 = polar_to_cartesian(current_r + 8, theta_end, distortion)
            p4 = polar_to_cartesian(current_r + 8, theta_start, distortion)
            
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.line_to(*p3)
            ctx.line_to(*p4)
            ctx.close_path()
            
            if random.random() > 0.3:
                ctx.fill()
            else:
                ctx.stroke()
                
            # 2. DATA-LINKS (Hairline annotations)
            if random.random() > 0.8:
                ctx.set_source_rgba(0.9, 0.9, 1.0, 0.3)
                ctx.set_line_width(0.3)
                p_next_ring = polar_to_cartesian(current_r + 40, theta_start, distortion)
                ctx.move_to(*p1)
                ctx.line_to(*p_next_ring)
                ctx.stroke()

        # 3. CHROMATIC NOISE (Vibrant Accents)
        # Occasional "data intensity" markers
        if random.random() > 0.97:
            ctx.set_source_rgb(1.0, 0.3, 0.1) # Neon Orange/Red
            nx, ny = polar_to_cartesian(current_r + random.uniform(-5, 5), theta_start, distortion)
            ctx.rectangle(nx - 2, ny - 2, 4, 4)
            ctx.fill()
            
            # Small technical label-like line
            ctx.set_line_width(0.5)
            ctx.move_to(nx, ny)
            ctx.line_to(nx + 15, ny - 10)
            ctx.stroke()

# 4. RADIAL GRID OVERLAY (The "Digital Sediment")
# Extremely thin, systematic lines to reinforce the radial grid
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.2)
for i in range(12):
    angle = (i / 12) * 2 * math.pi
    p_start = polar_to_cartesian(inner_radius, angle, 0)
    p_end = polar_to_cartesian(outer_radius + 20, angle, 0)
    ctx.move_to(*p_start)
    ctx.line_to(*p_end)
    ctx.stroke()

for r in range(inner_radius, outer_radius, 40):
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()

# 5. RIGID NODES (Technical markers)
# Adding small geometric annotations to give a diagrammatic feel
for _ in range(15):
    angle = random.uniform(0, 2 * math.pi)
    r = random.uniform(inner_radius, outer_radius)
    nx, ny = polar_to_cartesian(r, angle, 1.0)
    
    ctx.set_source_rgb(0.1, 0.8, 0.9) # Cyan accent
    ctx.set_line_width(1.0)
    size = random.randint(2, 6)
    ctx.move_to(nx - size, ny)
    ctx.line_to(nx + size, ny)
    ctx.move_to(nx, ny - size)
    ctx.line_to(nx, ny + size)
    ctx.stroke()

# Final composition polish: A heavy border frame (Swiss minimal style)
ctx.set_source_rgba(0.0, 0.0, 0.0, 0.2)
ctx.set_line_width(40)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Signature technical block
ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.rectangle(width - 80, height - 40, 50, 10)
ctx.fill()
ctx.set_line_width(0.5)
ctx.move_to(width - 80, height - 45)
ctx.line_to(width - 30, height - 45)
ctx.stroke()
