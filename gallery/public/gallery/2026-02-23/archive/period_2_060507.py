import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep "Technical Cobalt"
ctx.set_source_rgb(0.02, 0.05, 0.15) 
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
rings = 8
segments = 12
main_color = (0.9, 0.95, 1.0) # Stark white-blue
accent_color = (0.3, 0.5, 0.9) # Mid-tone cobalt

def to_polar_distorted(r, theta, distortion_factor=15):
    """Applies a radial distortion based on the angle and distance."""
    # Radial distortion using sine waves to create a 'harmonic' wobble
    r_new = r + math.sin(theta * 6) * distortion_factor + math.cos(r * 0.05) * 10
    x = center_x + r_new * math.cos(theta)
    y = center_y + r_new * math.sin(theta)
    return x, y

def draw_schematic_marker(x, y, size=4):
    """Draws a tiny crosshair or coordinate marker."""
    ctx.set_line_width(0.5)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# 1. PRIMARY GRID: Distorted Polar Rings
for i in range(1, rings + 1):
    r = i * 35
    ctx.set_source_rgba(*main_color, 0.2 if i % 2 == 0 else 0.5)
    ctx.set_line_width(0.7 if i % 2 == 0 else 1.5)
    
    # Draw ring segments with variable precision
    steps = 200
    for s in range(steps):
        t1 = (s / steps) * math.pi * 2
        t2 = ((s + 1) / steps) * math.pi * 2
        
        p1 = to_polar_distorted(r, t1)
        p2 = to_polar_distorted(r, t2)
        
        ctx.move_to(*p1)
        ctx.line_to(*p2)
    ctx.stroke()

# 2. RADIAL CONNECTORS (Spikes)
for j in range(segments):
    theta = (j / segments) * math.pi * 2
    ctx.set_source_rgba(*main_color, 0.4)
    ctx.set_line_width(0.5)
    
    # Draw a dashed radial line with markers
    for r_step in range(20, 300, 10):
        p1 = to_polar_distorted(r_step, theta)
        p2 = to_polar_distorted(r_step + 5, theta)
        ctx.move_to(*p1)
        ctx.line_to(*p2)
        ctx.stroke()
        
        # Occasional blueprint markers
        if r_step % 60 == 0:
            draw_schematic_marker(*p1)

# 3. RELATIONAL NETWORKING (Floating Nodes)
# Create 'logical connections' between arbitrary points in the distorted grid
random.seed(42) # Deterministic randomness for 'systematic' feel
nodes = []
for _ in range(15):
    r_rand = random.uniform(50, 250)
    t_rand = random.uniform(0, math.pi * 2)
    nodes.append(to_polar_distorted(r_rand, t_rand))

ctx.set_source_rgba(*accent_color, 0.6)
ctx.set_line_width(0.3)
for i, node_a in enumerate(nodes):
    for node_b in nodes[i+1:]:
        if math.dist(node_a, node_b) < 150:
            ctx.move_to(*node_a)
            ctx.line_to(*node_b)
            ctx.stroke()

# 4. DIGITAL ARTIFACTING (Dithered Noise & Blocks)
# Simulating 'data clusters' or quadtree partitions
for _ in range(40):
    r_val = random.uniform(80, 280)
    t_val = random.uniform(0, math.pi * 2)
    x, y = to_polar_distorted(r_val, t_val)
    
    # Small brutalist blocks
    ctx.set_source_rgba(*main_color, random.uniform(0.1, 0.8))
    size = random.choice([2, 4, 8])
    if random.random() > 0.7:
        ctx.rectangle(x, y, size, size)
        ctx.fill()
    else:
        # Micro-type markers (non-functional)
        ctx.set_line_width(0.2)
        ctx.move_to(x, y)
        ctx.line_to(x + 10, y)
        ctx.stroke()

# 5. HIGH-FREQUENCY "NOISE" TEXTURE
# Adding a layer of 'blueprint' stippling
for _ in range(1000):
    nx = random.uniform(0, width)
    ny = random.uniform(0, height)
    # Only draw noise if it falls near the circular composition
    dist = math.dist((nx, ny), (center_x, center_y))
    if 280 < dist < 300 or random.random() > 0.98:
        ctx.set_source_rgba(*main_color, 0.15)
        ctx.rectangle(nx, ny, 1, 1)
        ctx.fill()

# 6. CENTRAL HIERARCHICAL CORE
# A solid geometric anchor
ctx.set_source_rgb(*main_color)
ctx.arc(center_x, center_y, 4, 0, math.pi * 2)
ctx.fill()
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 12, 0, math.pi * 2)
ctx.stroke()

# Framing: Technical borders
ctx.set_source_rgba(*main_color, 0.8)
ctx.set_line_width(2)
# Corner brackets
pad = 20
length = 40
corners = [(pad, pad), (width-pad, pad), (width-pad, height-pad), (pad, height-pad)]
for i, (cx, cy) in enumerate(corners):
    ctx.move_to(cx + (length if i in [0, 3] else -length), cy)
    ctx.line_to(cx, cy)
    ctx.line_to(cx, cy + (length if i in [0, 1] else -length))
    ctx.stroke()

# Final Polish: Systematic line through center
ctx.set_line_width(0.5)
ctx.set_source_rgba(*accent_color, 0.3)
ctx.move_to(0, center_y)
ctx.line_to(width, center_y)
ctx.move_to(center_x, 0)
ctx.line_to(center_x, height)
ctx.stroke()

