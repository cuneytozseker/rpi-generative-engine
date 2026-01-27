import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep architectural charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration for the kinetic system
cx, cy = width / 2, height / 2
num_rings = 42
num_sectors = 64
max_radius = min(width, height) * 0.45

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to cartesian with a radial distortion field."""
    # Radial distortion: logic creates a 'pulse' or 'gravity' effect
    # warping the grid based on its angular position.
    distortion = 1.0 + 0.15 * math.sin(theta * 5 + r * 0.02)
    r_distorted = r * distortion
    
    x = cx + r_distorted * math.cos(theta)
    y = cy + r_distorted * math.sin(theta)
    return x, y

# 1. DRAW UNDERLYING "DATA CLOUD" (Atmospheric Depth)
# Low opacity particles following the mathematical current
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.05)
for _ in range(800):
    r = random.uniform(20, max_radius * 1.2)
    t = random.uniform(0, math.pi * 2)
    # Entropy increases with radius
    jitter = (r / max_radius) * 15
    px, py = polar_to_cartesian(r, t)
    ctx.arc(px + random.uniform(-jitter, jitter), 
            py + random.uniform(-jitter, jitter), 
            0.5, 0, 2 * math.pi)
    ctx.fill()

# 2. GENERATE SWISS POLAR GRID (Structural Hierarchy)
for i in range(num_rings):
    r = (i / num_rings) * max_radius
    # Progressive line weight: thicker near the core, gossamer at the edges
    line_weight = 0.2 + (1.0 - i / num_rings) * 1.5
    ctx.set_line_width(line_weight)
    
    # Calculate transparency based on ring index for "atmospheric depth"
    alpha = 0.1 + (0.5 * (1.0 - i / num_rings))
    
    for j in range(num_sectors):
        t1 = (j / num_sectors) * 2 * math.pi
        t2 = ((j + 1) / num_sectors) * 2 * math.pi
        
        # Directed Entropy: Skip cells randomly, probability increases with radius
        if random.random() < (i / num_rings) * 0.7:
            continue
            
        # Draw the distorted grid cell (arc segment)
        p1_x, p1_y = polar_to_cartesian(r, t1)
        p2_x, p2_y = polar_to_cartesian(r, t2)
        
        # Color Logic: Transition from White to Swiss Red accent
        if random.random() > 0.96:
            ctx.set_source_rgba(0.89, 0.12, 0.12, alpha * 2) # Swiss Red
        else:
            ctx.set_source_rgba(0.95, 0.95, 0.95, alpha)
            
        ctx.move_to(p1_x, p1_y)
        ctx.line_to(p2_x, p2_y)
        ctx.stroke()
        
        # Add "Kinetic Dashes" along radial lines
        if j % 4 == 0:
            r2 = r + (max_radius / num_rings) * 0.8
            p3_x, p3_y = polar_to_cartesian(r2, t1)
            ctx.set_line_width(line_weight * 0.5)
            ctx.move_to(p1_x, p1_y)
            ctx.line_to(p3_x, p3_y)
            ctx.stroke()

# 3. OVERLAY BRUTALIST BLOCKS (Geometric Anchors)
# Heavier elements that follow the distorted flow to emphasize the vector field
for _ in range(12):
    r_start = random.uniform(0.2, 0.7) * max_radius
    t_start = random.uniform(0, 2 * math.pi)
    span_t = random.uniform(0.1, 0.4)
    span_r = 12
    
    # Draw a warped "rectangular" segment
    ctx.set_source_rgba(1, 1, 1, 0.8)
    
    # Trace the four corners of the warped segment
    steps = 10
    # Top edge
    for s in range(steps + 1):
        curr_t = t_start + (span_t * (s/steps))
        px, py = polar_to_cartesian(r_start, curr_t)
        if s == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    # Right edge
    for s in range(steps + 1):
        curr_r = r_start + (span_r * (s/steps))
        px, py = polar_to_cartesian(curr_r, t_start + span_t)
        ctx.line_to(px, py)
    # Bottom edge
    for s in range(steps + 1):
        curr_t = t_start + span_t - (span_t * (s/steps))
        px, py = polar_to_cartesian(r_start + span_r, curr_t)
        ctx.line_to(px, py)
    # Left edge
    ctx.close_path()
    ctx.fill()

# 4. FINAL VELOCITY VECTORS (Directional Flow)
# Ultra-fine lines slicing through the composition to suggest high speed
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.3)
for _ in range(20):
    angle = random.uniform(0, 2 * math.pi)
    length = random.uniform(100, 400)
    start_r = random.uniform(0, 50)
    
    for step in range(20):
        curr_r = start_r + (step / 20) * length
        # Spiral distortion
        curr_t = angle + (curr_r * 0.002)
        px, py = polar_to_cartesian(curr_r, curr_t)
        if step == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.stroke()

# Subtle grain/noise for texture
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.rectangle(random.random()*width, random.random()*height, 1, 1)
    ctx.fill()
