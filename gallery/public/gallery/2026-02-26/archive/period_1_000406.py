import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Monochromatic Void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# HELPER: Simple pseudo-noise function using harmonics
def get_angle(x, y):
    scale1 = 0.005
    scale2 = 0.015
    angle = math.sin(x * scale1) * math.cos(y * scale1) * math.pi * 2
    angle += math.sin(y * scale2 + x * scale2) * math.pi
    return angle

# 1. THE GRID (Swiss Design Foundation)
ctx.set_line_width(0.5)
ctx.set_source_rgba(0.3, 0.3, 0.4, 0.2)
grid_size = 40
for i in range(0, width, grid_size):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, grid_size):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. RECURSIVE SUBDIVISIONS (Quadtree Logic for "Data Blocks")
def draw_recursive_rects(x, y, w, h, depth):
    if depth > 4:
        return
    
    # Draw a technical marker
    if random.random() > 0.7:
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.1)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        
        # Micro-typography / Metadata simulation
        if w > 20:
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.4) # Electric Blue accent
            ctx.rectangle(x + 2, y + 2, 4, 1)
            ctx.fill()

    if random.random() < 0.6 and depth < 4:
        draw_recursive_rects(x, y, w/2, h/2, depth + 1)
        draw_recursive_rects(x + w/2, y, w/2, h/2, depth + 1)
        draw_recursive_rects(x, y + h/2, w/2, h/2, depth + 1)
        draw_recursive_rects(x + w/2, y + h/2, w/2, h/2, depth + 1)

draw_recursive_rects(0, 0, width, height, 0)

# 3. PERLIN-LIKE FLOW FIELD PARTICLES
# We simulate the "Entropy" through particle trails
num_particles = 1200
steps = 45

# Set color for trails - ghostly white with varying transparency
for _ in range(num_particles):
    # Cluster particles more towards the center (Radial Dispersion)
    angle_spawn = random.uniform(0, math.pi * 2)
    dist_spawn = random.uniform(0, 200) ** 1.2 / 10 # Power rule for density
    px = width/2 + math.cos(angle_spawn) * dist_spawn
    py = height/2 + math.sin(angle_spawn) * dist_spawn
    
    ctx.set_line_width(random.uniform(0.2, 0.8))
    
    # Vary trail color slightly
    r_val = random.uniform(0.7, 0.9)
    ctx.set_source_rgba(r_val, r_val, r_val + 0.1, random.uniform(0.1, 0.4))
    
    ctx.move_to(px, py)
    
    for _ in range(steps):
        angle = get_angle(px, py)
        # Move particle
        px += math.cos(angle) * 3
        py += math.sin(angle) * 3
        
        # Draw segment
        ctx.line_to(px, py)
        
    ctx.stroke()

# 4. CONNECTIVE VECTORS (The "Systemic Logic")
# Draw long, thin paths connecting arbitrary focal points
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.0, 0.8, 1.0, 0.6) # Cyan/Electric Blue
nodes = [(random.randint(0, width), random.randint(0, height)) for _ in range(12)]

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        if random.random() > 0.85:
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
            
            # Draw a tiny circular "node" at intersections
            ctx.arc(x1, y1, 1.5, 0, 2 * math.pi)
            ctx.fill()

# 5. OVERLAY TEXTURE (Technical Glitch/Stochastic Offsets)
for _ in range(100):
    tx = random.randint(0, width)
    ty = random.randint(0, height)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    if random.random() > 0.95:
        # Static "Glitch" bit
        ctx.rectangle(tx, ty, random.randint(10, 40), 0.5)
        ctx.fill()
    elif random.random() > 0.98:
        # Crosshair marker
        length = 5
        ctx.move_to(tx - length, ty)
        ctx.line_to(tx + length, ty)
        ctx.move_to(tx, ty - length)
        ctx.line_to(tx, ty + length)
        ctx.stroke()

# Final Hierarchy: A single bold geometric element for Swiss impact
ctx.set_line_width(1.0)
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.arc(width/2, height/2, 220, 0, math.pi * 0.15)
ctx.stroke()
ctx.arc(width/2, height/2, 225, math.pi, math.pi * 1.15)
ctx.stroke()

# End of code
