import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep "Terminal" Black/Navy
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def to_polar_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_thermal_leak(ctx, x, y, size):
    """Adds a localized spectral gradient to simulate diagnostic 'hotspots'."""
    gradient = cairo.RadialGradient(x, y, 0, x, y, size)
    # Spectral transition: deep violet -> vibrant magenta/orange -> transparent
    gradient.add_color_stop_rgba(0.0, 1.0, 0.2, 0.4, 0.6)
    gradient.add_color_stop_rgba(0.4, 0.8, 0.1, 0.8, 0.3)
    gradient.add_color_stop_rgba(1.0, 0.0, 0.0, 0.0, 0.0)
    ctx.set_source(gradient)
    ctx.arc(x, y, size, 0, 2 * math.pi)
    ctx.fill()

# Configuration
center_x, center_y = width // 2, height // 2
num_rings = 14
num_sectors = 36
distortion_strength = 25.0

# 1. LAYER: SUB-GRID (Swiss Precision Foundation)
ctx.set_line_width(0.3)
for i in range(num_rings):
    r_base = (i + 1) * 22
    ctx.set_source_rgba(0.4, 0.6, 0.9, 0.2)
    
    # Draw distorted concentric rings
    ctx.new_path()
    for s in range(400):
        angle = (s / 400) * 2 * math.pi
        # Radial distortion using harmonic interference
        r_offset = math.sin(angle * 5 + i) * 10 * math.cos(i * 0.5)
        r_distorted = r_base + r_offset
        px, py = to_polar_cartesian(center_x, center_y, r_distorted, angle)
        if s == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.close_path()
    ctx.stroke()

# 2. LAYER: RADIAL AXES & NODAL CLUSTERS
ctx.set_line_width(0.5)
for s in range(num_sectors):
    angle = (s / num_sectors) * 2 * math.pi
    
    # Every 4th axis is "Primary"
    if s % 4 == 0:
        ctx.set_source_rgba(0.8, 0.9, 1.0, 0.5)
    else:
        ctx.set_source_rgba(0.4, 0.6, 0.9, 0.15)
        
    start_r = 40
    end_r = 240 + math.sin(angle * 3) * 30
    
    x1, y1 = to_polar_cartesian(center_x, center_y, start_r, angle)
    x2, y2 = to_polar_cartesian(center_x, center_y, end_r, angle)
    
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
    
    # Add nodal points at intersections
    if s % 3 == 0:
        for r_step in [80, 140, 210]:
            nx, ny = to_polar_cartesian(center_x, center_y, r_step + math.sin(angle)*5, angle)
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.arc(nx, ny, 1.5, 0, 2 * math.pi)
            ctx.fill()
            
            # Recursive subdivision (small crosshairs)
            ctx.set_line_width(0.2)
            ctx.move_to(nx - 4, ny)
            ctx.line_to(nx + 4, ny)
            ctx.move_to(nx, ny - 4)
            ctx.line_to(nx, ny + 4)
            ctx.stroke()

# 3. LAYER: THERMAL LEAKS (Asymmetric Focal Points)
random.seed(42) # Deterministic randomness for composition
for _ in range(5):
    leak_angle = random.uniform(0, 2 * math.pi)
    leak_r = random.uniform(80, 200)
    lx, ly = to_polar_cartesian(center_x, center_y, leak_r, leak_angle)
    draw_thermal_leak(ctx, lx, ly, random.uniform(40, 100))

# 4. LAYER: DATA ARTIFACTS & DITHERING NOISE
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.4)
for _ in range(800):
    # Stochastic noise distribution clustered around center
    dist = abs(random.gauss(0, 120))
    ang = random.uniform(0, 2 * math.pi)
    nx, ny = to_polar_cartesian(center_x, center_y, dist, ang)
    
    # Draw tiny "bits"
    if random.random() > 0.5:
        ctx.rectangle(nx, ny, 1, 1)
    else:
        ctx.move_to(nx, ny)
        ctx.line_to(nx + 2, ny)
    ctx.stroke()

# 5. LAYER: SWISS TYPOGRAPHIC GEOMETRY
# Rectangular data blocks along the periphery
for i in range(12):
    angle = i * (math.pi / 6)
    r = 260
    tx, ty = to_polar_cartesian(center_x, center_y, r, angle)
    
    ctx.save()
    ctx.translate(tx, ty)
    ctx.rotate(angle + math.pi/2)
    
    # Draw status-bar-like blocks
    ctx.set_source_rgba(0.7, 0.8, 1.0, 0.6)
    for b in range(5):
        if random.random() > 0.3:
            ctx.rectangle(b * 6, 0, 4, 2)
            ctx.fill()
    
    # Hairline indicators
    ctx.set_line_width(0.5)
    ctx.move_to(-20, 0)
    ctx.line_to(40, 0)
    ctx.stroke()
    ctx.restore()

# Final Polish: Central Core
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.arc(center_x, center_y, 35, 0, 2 * math.pi)
ctx.stroke()
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.arc(center_x, center_y, 30, 0, 2 * math.pi)
ctx.fill()
