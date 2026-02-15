import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
cx, cy = width // 2, height // 2

# Background: Deep Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_to_cartesian(r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

# Parameters for Non-Linear Orthogonal Subdivisions
rings = 40
spokes = 72
max_radius = min(width, height) * 0.45
accent_color = (0.0, 1.0, 0.9)  # Technical Cyan

# 1. DRAW UNDERLYING RADIAL GRID (Hairlines)
ctx.set_line_width(0.3)
for i in range(rings):
    # Logarithmic radial distribution for centripetal tension
    # Higher density towards the center
    r = max_radius * math.pow(i / rings, 1.5)
    
    # Grid lines become more transparent as they move outwards
    alpha = 0.5 * (1 - (i / rings))
    ctx.set_source_rgba(0.7, 0.8, 1.0, alpha)
    
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()

for j in range(spokes):
    theta = (j / spokes) * 2 * math.pi
    r_start = 10
    r_end = max_radius * (0.8 + 0.2 * math.sin(theta * 3)) # Subtle distortion
    
    x1, y1 = polar_to_cartesian(r_start, theta)
    x2, y2 = polar_to_cartesian(r_end, theta)
    
    ctx.set_source_rgba(0.7, 0.8, 1.0, 0.15)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 2. DIMENSIONAL CONTRAST: Opaque Masses (Swiss "Blocks")
# We treat the polar grid as a coordinate system for rectangular data blocks
for _ in range(120):
    r_idx = random.randint(5, rings - 5)
    s_idx = random.randint(0, spokes - 1)
    
    # Map indices to geometry
    r1 = max_radius * math.pow(r_idx / rings, 1.5)
    r2 = max_radius * math.pow((r_idx + random.randint(1, 4)) / rings, 1.5)
    t1 = (s_idx / spokes) * 2 * math.pi
    t2 = ((s_idx + random.randint(1, 6)) / spokes) * 2 * math.pi
    
    # Probability gate: higher density near center
    if random.random() > (r_idx / rings):
        ctx.set_source_rgba(0.9, 0.9, 1.0, random.uniform(0.1, 0.6))
        
        # Draw arc-based "rectangle"
        ctx.new_path()
        ctx.arc(cx, cy, r1, t1, t2)
        ctx.arc_negative(cx, cy, r2, t2, t1)
        ctx.close_path()
        
        if random.random() > 0.8:
            ctx.set_source_rgba(*accent_color, 0.8) # Signal accent
            ctx.fill()
        else:
            ctx.fill()

# 3. NODE-LINK SYSTEM (Stochastic Clustering)
# Connecting random coordinates to simulate informational flow
points = []
for _ in range(15):
    r = max_radius * random.uniform(0.2, 0.9)
    t = random.uniform(0, 2 * math.pi)
    points.append(polar_to_cartesian(r, t))

ctx.set_line_width(0.5)
for i, p1 in enumerate(points):
    for p2 in points[i+1:]:
        dist = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        if dist < 150:
            ctx.set_source_rgba(1, 1, 1, 0.2)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()
            
            # Draw tiny data nodes at intersections
            ctx.set_source_rgba(*accent_color, 1.0)
            ctx.arc(p1[0], p1[1], 1.5, 0, 2 * math.pi)
            ctx.fill()

# 4. DECONSTRUCTED TEXTURE (Micro-Metadata)
# Adding "bit-streams" or small ticks along the outer edges
for j in range(spokes * 2):
    theta = (j / (spokes * 2)) * 2 * math.pi
    if random.random() > 0.4:
        r_base = max_radius * 1.02
        length = random.randint(2, 15)
        
        x1, y1 = polar_to_cartesian(r_base, theta)
        x2, y2 = polar_to_cartesian(r_base + length, theta)
        
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.set_line_width(0.8)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # Occasional numeric-like markers
        if random.random() > 0.92:
            ctx.set_source_rgba(*accent_color, 1.0)
            ctx.rectangle(x2, y2, 3, 3)
            ctx.fill()

# 5. FINAL CENTER ATTRACTOR
# A heavy mass at the core to ground the centripetal tension
ctx.set_source_rgb(0.05, 0.05, 0.1)
ctx.arc(cx, cy, 15, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgba(*accent_color, 0.4)
ctx.set_line_width(1)
ctx.arc(cx, cy, 20, 0, 2 * math.pi)
ctx.stroke()

# Clean up
