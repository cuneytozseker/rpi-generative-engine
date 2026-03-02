import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Technical Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
rings = 14
sectors = 36
center_void = 40
max_radius = min(width, height) * 0.45

# Colors
COBALT = (0.0, 0.47, 0.85)
OFF_WHITE = (0.9, 0.9, 0.92)
MID_GREY = (0.4, 0.4, 0.45)

def polar_to_cartesian(r, theta, distortion=0):
    # Apply a non-linear radial distortion based on the angle
    # This creates the "Information Matrix" tension
    r_distorted = r + (math.sin(theta * 4) * distortion)
    x = cx + r_distorted * math.cos(theta)
    y = cy + r_distorted * math.sin(theta)
    return x, y

def draw_crosshair(x, y, size, color):
    ctx.set_source_rgb(*color)
    ctx.set_line_width(0.5)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

def draw_data_glyph(x, y, r):
    # Small technical markers
    ctx.set_source_rgb(*COBALT)
    ctx.rectangle(x-1.5, y-1.5, 3, 3)
    ctx.fill()
    ctx.set_source_rgb(*OFF_WHITE)
    ctx.set_line_width(0.3)
    ctx.arc(x, y, 5, 0, 2 * math.pi)
    ctx.stroke()

# 1. Primary Grid Structure (Radial & Concentric)
for i in range(rings):
    r = center_void + (i / rings) * (max_radius - center_void)
    
    # Draw concentric arcs with systematic gaps
    ctx.set_source_rgba(0.4, 0.4, 0.45, 0.3)
    ctx.set_line_width(0.5 if i % 2 == 0 else 0.2)
    
    for s in range(sectors):
        theta_start = (s / sectors) * 2 * math.pi
        theta_end = ((s + 0.8) / sectors) * 2 * math.pi
        
        # Add slight wobble to the rings
        distort = 5 * math.sin(i * 0.5)
        
        # Trace path
        points = 20
        for p in range(points + 1):
            t = theta_start + (p / points) * (theta_end - theta_start)
            px, py = polar_to_cartesian(r, t, distort)
            if p == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.stroke()

# 2. Information Axes (Radial Rays)
for s in range(sectors):
    if s % 3 != 0: continue # Swiss hierarchy: selective density
    
    theta = (s / sectors) * 2 * math.pi
    distort = 5 * math.sin(s)
    
    ctx.set_source_rgba(0.9, 0.9, 0.92, 0.15)
    ctx.set_line_width(0.4)
    
    start_x, start_y = polar_to_cartesian(center_void, theta, distort)
    end_x, end_y = polar_to_cartesian(max_radius, theta, distort)
    
    ctx.move_to(start_x, start_y)
    ctx.line_to(end_x, end_y)
    ctx.stroke()

# 3. Recursive Geometric Events (Conditional Intersections)
random.seed(42) # Deterministic randomness for precision
for i in range(rings):
    for s in range(sectors):
        # Only place elements at specific algorithmic intersections
        if (i * s) % 17 == 0 or (i + s) % 13 == 0:
            r = center_void + (i / rings) * (max_radius - center_void)
            theta = (s / sectors) * 2 * math.pi
            distort = 5 * math.sin(i * 0.5)
            x, y = polar_to_cartesian(r, theta, distort)
            
            # Draw hierarchical markers
            if i > rings * 0.7:
                draw_data_glyph(x, y, r)
            elif i % 4 == 0:
                draw_crosshair(x, y, 4, OFF_WHITE)
            
            # Connect some nodes with high-tension chords
            if random.random() > 0.92:
                next_s = (s + 5) % sectors
                nx, ny = polar_to_cartesian(r, (next_s / sectors) * 2 * math.pi, distort)
                ctx.set_source_rgba(0.0, 0.47, 0.85, 0.4)
                ctx.set_line_width(0.3)
                ctx.move_to(x, y)
                ctx.line_to(nx, ny)
                ctx.stroke()

# 4. Optical Shading / Technical Annotation
# Adding a "measurement scale" on the horizontal axis
for step in range(10):
    scale_r = center_void + (step / 10) * (max_radius - center_void)
    sx, sy = polar_to_cartesian(scale_r, 0, 0)
    ctx.set_source_rgb(*MID_GREY)
    ctx.set_line_width(1.0)
    ctx.move_to(sx, sy - 3)
    ctx.line_to(sx, sy + 3)
    ctx.stroke()

# 5. Global Texture - Micro Dots
for _ in range(200):
    rx = random.uniform(0, width)
    ry = random.uniform(0, height)
    # Check if inside the matrix influence
    dist_to_center = math.sqrt((rx-cx)**2 + (ry-cy)**2)
    if center_void < dist_to_center < max_radius + 20:
        ctx.set_source_rgba(0.9, 0.9, 0.92, 0.2)
        ctx.arc(rx, ry, 0.5, 0, 2*math.pi)
        ctx.fill()

# Final Polish: Center Hub
ctx.set_source_rgb(*OFF_WHITE)
ctx.set_line_width(1.5)
ctx.arc(cx, cy, center_void - 10, 0, 2 * math.pi)
ctx.stroke()

ctx.set_source_rgb(*COBALT)
ctx.set_line_width(0.5)
ctx.arc(cx, cy, center_void - 15, 0, 2 * math.pi)
ctx.stroke()
