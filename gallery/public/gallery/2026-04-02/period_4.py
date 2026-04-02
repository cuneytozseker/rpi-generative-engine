import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Palette: High-contrast Cobalt and Off-White (Functional Duo-tone)
COBALT = (0.0, 0.28, 0.67)
CREAM = (0.97, 0.96, 0.93)

# Background
ctx.set_source_rgb(*CREAM)
ctx.paint()

# Configuration
origin_x, origin_y = width // 2, height // 2
rings = 18
spokes = 36
max_radius = 320

def polar_to_cartesian(r, theta, distortion=0):
    """Converts polar to cartesian with optional radial distortion."""
    # Apply a harmonic distortion based on the angle
    r_distorted = r * (1 + distortion * math.sin(theta * 6))
    x = origin_x + r_distorted * math.cos(theta)
    y = origin_y + r_distorted * math.sin(theta)
    return x, y

def draw_glitch_mark(ctx, x, y, size):
    """Draws a technical symbol (crosshair or dot)."""
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

def draw_hatch_pattern(ctx, x, y, size, density):
    """Draws a modular fill pattern within a small cell."""
    if density < 0.2: return
    ctx.save()
    ctx.translate(x, y)
    num_lines = int(density * 8)
    for i in range(num_lines):
        offset = (i / num_lines) * size - (size / 2)
        ctx.move_to(-size/2, offset)
        ctx.line_to(size/2, offset)
    ctx.set_line_width(0.4)
    ctx.stroke()
    ctx.restore()

# 1. DRAW RADIAL GRID (The Structural Container)
ctx.set_source_rgb(*COBALT)
ctx.set_line_width(0.5)

for i in range(1, rings + 1):
    r = (i / rings) * max_radius
    # Variable line dash to create "lo-fi" electronic feel
    ctx.set_dash([random.uniform(1, 4), random.uniform(2, 6)])
    
    ctx.new_path()
    for s in range(200):
        theta = (s / 200) * 2 * math.pi
        # Distortion increases with radius (entropy modulation)
        dist = 0.05 * (i / rings)
        px, py = polar_to_cartesian(r, theta, dist)
        if s == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.close_path()
    ctx.stroke()

# 2. DRAW ANGULAR SPOKES
ctx.set_dash([])
for j in range(spokes):
    theta = (j / spokes) * 2 * math.pi
    ctx.new_path()
    for r_step in range(0, max_radius, 10):
        dist = 0.05 * (r_step / max_radius)
        px, py = polar_to_cartesian(r_step, theta, dist)
        if r_step == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    
    # Only stroke some spokes to modulate density
    if random.random() > 0.4:
        ctx.set_line_width(0.3)
        ctx.stroke()

# 3. INFORMATION DENSITY CLUSTERS (Modular Fill & Symbols)
random.seed(42) # Deterministic for layout balance
for i in range(1, rings):
    for j in range(spokes):
        r = (i / rings) * max_radius
        theta = (j / spokes) * 2 * math.pi
        
        # Calculate coordinate with distortion
        dist = 0.05 * (i / rings)
        x, y = polar_to_cartesian(r, theta, dist)
        
        # Density logic: Create "hotspots" of data
        # Based on distance to center and noise-like logic
        density_val = (math.sin(r * 0.02) * math.cos(theta * 3) + 1) / 2
        
        if density_val > 0.7:
            # Dense cross-hatching
            draw_hatch_pattern(ctx, x, y, 8, density_val)
        elif density_val > 0.5:
            # Symbols / Nodes
            ctx.set_line_width(0.8)
            draw_glitch_mark(ctx, x, y, 3)
        elif density_val < 0.1 and random.random() > 0.8:
            # Occasional stochastic dot in empty space
            ctx.arc(x, y, 1, 0, 2*math.pi)
            ctx.fill()

# 4. NODAL NETWORKS (Connecting high-density points)
ctx.set_line_width(0.2)
points = []
for _ in range(40):
    r = random.uniform(50, max_radius)
    theta = random.uniform(0, 2 * math.pi)
    points.append(polar_to_cartesian(r, theta, 0.05 * (r/max_radius)))

for i, p1 in enumerate(points):
    for p2 in points[i+1:]:
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if dist < 60:
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()

# 5. TECHNICAL ANNOTATIONS (Simulated Readout)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(7)
for _ in range(12):
    r = random.uniform(100, max_radius)
    theta = random.uniform(0, 2 * math.pi)
    x, y = polar_to_cartesian(r, theta, 0)
    
    # Draw tiny data strings
    label = f"{random.randint(100, 999)}.{random.randint(10, 99)}"
    ctx.move_to(x + 5, y - 5)
    ctx.show_text(label)
    ctx.rectangle(x, y - 10, 2, 2) # small anchor block
    ctx.fill()

# Final Polish: Vignette/Border
ctx.set_line_width(2)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()
