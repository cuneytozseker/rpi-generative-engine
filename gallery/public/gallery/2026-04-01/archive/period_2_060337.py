import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Technical "Blueprint" Navy
ctx.set_source_rgb(0.02, 0.04, 0.08)
ctx.paint()

def to_polar(r, theta, cx, cy):
    x = cx + r * math.cos(theta)
    y = cy + r * math.sin(theta)
    return x, y

def draw_glyph(ctx, x, y, size, color):
    ctx.save()
    ctx.set_source_rgba(*color)
    ctx.set_line_width(0.5)
    # Draw a small cross marker
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    # Tiny core
    ctx.arc(x, y, size/4, 0, 2*math.pi)
    ctx.fill()
    ctx.restore()

# Parameters
cx, cy = width / 2, height / 2
rings = 18
spokes = 36
max_radius = min(width, height) * 0.45

# 1. PRIMARY RADIAL GRID (Swiss precision)
ctx.set_line_width(0.3)
for i in range(rings):
    # Logarithmic spacing for rings to create depth/perspective
    r = math.pow(i / rings, 1.2) * max_radius
    alpha = 0.1 + (i / rings) * 0.3
    ctx.set_source_rgba(0.4, 0.7, 1.0, alpha)
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()

for i in range(spokes):
    theta = (i / spokes) * 2 * math.pi
    r_start = 20
    r_end = max_radius + 10
    x1, y1 = to_polar(r_start, theta, cx, cy)
    x2, y2 = to_polar(r_end, theta, cx, cy)
    ctx.set_source_rgba(0.4, 0.7, 1.0, 0.15)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 2. STOCHASTIC PATHFINDING (The "Flow")
# Generating "data-stream" lines that follow distorted polar paths
for _ in range(12):
    start_theta = random.uniform(0, 2 * math.pi)
    arc_length = random.uniform(math.pi/4, math.pi)
    base_r = random.uniform(40, max_radius)
    
    ctx.set_line_width(random.uniform(0.5, 1.5))
    ctx.set_source_rgba(0.0, 0.9, 1.0, 0.6)
    
    # Draw a path with radial noise
    steps = 100
    for s in range(steps):
        t = s / steps
        current_theta = start_theta + t * arc_length
        # Radial distortion using sine harmonics
        distortion = 15 * math.sin(current_theta * 8) * math.cos(current_theta * 3)
        r = base_r + distortion
        
        x, y = to_polar(r, current_theta, cx, cy)
        if s == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# 3. DENSITY MODULATION (Hatched clusters)
for _ in range(5):
    center_theta = random.uniform(0, 2*math.pi)
    center_r = random.uniform(max_radius * 0.3, max_radius * 0.8)
    
    ctx.save()
    bx, by = to_polar(center_r, center_theta, cx, cy)
    ctx.translate(bx, by)
    ctx.rotate(center_theta + math.pi/2)
    
    # Localized cross-hatching
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(0.2)
    h_size = 30
    for h in range(-5, 6):
        ctx.move_to(-h_size, h * 3)
        ctx.line_to(h_size, h * 3)
        ctx.move_to(h * 3, -h_size)
        ctx.line_to(h * 3, h_size)
    ctx.stroke()
    ctx.restore()

# 4. DATA NODES & ANCHOR GLYPHS
# Placing markers at specific grid intersections
for i in range(4):
    for j in range(6):
        if random.random() > 0.4:
            r = math.pow(i/4, 1.2) * max_radius + 40
            theta = (j/6) * 2 * math.pi + (i * 0.2)
            gx, gy = to_polar(r, theta, cx, cy)
            
            # Draw technical marker
            draw_glyph(ctx, gx, gy, 4, (1.0, 0.3, 0.2, 0.8)) # Safety Red highlight
            
            # Connect to center with a fine line
            ctx.set_source_rgba(1, 1, 1, 0.1)
            ctx.set_line_width(0.4)
            ctx.move_to(cx, cy)
            ctx.line_to(gx, gy)
            ctx.stroke()

# 5. PERIMETER DATA
# Geometric labels/ticks around the edge
ctx.set_source_rgba(0.8, 0.9, 1.0, 0.4)
ctx.set_line_width(1.0)
for i in range(120):
    theta = (i / 120) * 2 * math.pi
    length = 5 if i % 10 != 0 else 15
    r1 = max_radius + 15
    r2 = r1 + length
    x1, y1 = to_polar(r1, theta, cx, cy)
    x2, y2 = to_polar(r2, theta, cx, cy)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Final focal element - Central core
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.arc(cx, cy, 20, 0, 2*math.pi)
ctx.fill()
ctx.set_source_rgba(0.0, 0.9, 1.0, 0.8)
ctx.set_line_width(1)
ctx.arc(cx, cy, 5, 0, 2*math.pi)
ctx.stroke()
