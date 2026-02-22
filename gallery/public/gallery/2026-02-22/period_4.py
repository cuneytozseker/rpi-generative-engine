import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Atmospheric Deep Cobalt
ctx.set_source_rgb(0.02, 0.04, 0.08)
ctx.paint()

def to_cartesian(r, theta, center_x, center_y):
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return x, y

def draw_glitch_rect(ctx, x, y, size, color):
    # Staccato noise block
    ctx.set_source_rgba(*color)
    ctx.rectangle(x - size/2, y - size/2, size, size * random.uniform(0.1, 2.0))
    ctx.fill()

# Compositional Constants
cx, cy = width / 2, height / 2
rings = 18
segments = 40
max_radius = 350

# 1. LAYERED GLOW (Atmospheric depth)
radial_grad = cairo.RadialGradient(cx, cy, 20, cx, cy, max_radius)
radial_grad.add_color_stop_rgba(0, 0.1, 0.3, 0.6, 0.15)
radial_grad.add_color_stop_rgba(0.8, 0, 0, 0, 0)
ctx.set_source(radial_grad)
ctx.arc(cx, cy, max_radius, 0, 2 * math.pi)
ctx.fill()

# 2. THE DISTORTED POLAR GRID (Precision meets Entropy)
for i in range(1, rings):
    r = (i / rings) ** 1.2 * max_radius # Exponential scaling for depth
    entropy = (i / rings) ** 2 # Entropy increases with distance from core
    
    ctx.set_line_width(0.4 if i % 4 != 0 else 0.8)
    
    for j in range(segments):
        theta = (j / segments) * 2 * math.pi
        next_theta = ((j + 1) / segments) * 2 * math.pi
        
        # Jitter coordinates based on entropy
        jitter_r = random.uniform(-10, 10) * entropy
        jitter_t = random.uniform(-0.05, 0.05) * entropy
        
        p1_x, p1_y = to_cartesian(r + jitter_r, theta + jitter_t, cx, cy)
        p2_x, p2_y = to_cartesian(r + jitter_r, next_theta + jitter_t, cx, cy)
        
        # Draw ring segments
        ctx.set_source_rgba(0.8, 0.9, 1.0, 0.6 - (entropy * 0.4))
        ctx.move_to(p1_x, p1_y)
        ctx.line_to(p2_x, p2_y)
        ctx.stroke()
        
        # Radial Connectors (Rays)
        if j % 2 == 0:
            r_inner = ((i-1) / rings) ** 1.2 * max_radius
            p0_x, p0_y = to_cartesian(r_inner, theta, cx, cy)
            ctx.set_source_rgba(0.7, 0.8, 1.0, 0.3)
            ctx.move_to(p0_x, p0_y)
            ctx.line_to(p1_x, p1_y)
            ctx.stroke()

        # 3. TECHNICAL SPECIMENS (Data Nodes)
        if random.random() > 0.85 - (entropy * 0.2):
            node_size = random.uniform(1, 4)
            # High-saturated spectral accent (Orange/Cyan)
            if random.random() > 0.7:
                color = (1.0, 0.35, 0.1, 0.9) # International Orange
            else:
                color = (0.9, 0.95, 1.0, 0.8) # Ivory
            
            draw_glitch_rect(ctx, p1_x, p1_y, node_size, color)

# 4. VERTEX-EDGE OVERLAY (High precision paths)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.0, 1.0, 0.8, 0.4) # Cyan hair-lines
points = []
for _ in range(12):
    ang = random.uniform(0, 2 * math.pi)
    dist = random.uniform(50, max_radius)
    points.append(to_cartesian(dist, ang, cx, cy))

for i in range(len(points)):
    for j in range(i + 1, len(points)):
        if random.random() > 0.6:
            ctx.move_to(*points[i])
            ctx.line_to(*points[j])
            ctx.stroke()

# 5. THE CORE (Central Density)
ctx.set_source_rgb(1, 1, 1)
ctx.arc(cx, cy, 3, 0, 2 * math.pi)
ctx.fill()

# Concentric core rings
for r_core in [8, 12, 25]:
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(0.5)
    ctx.arc(cx, cy, r_core, 0, 2 * math.pi)
    ctx.stroke()

# 6. MARGINAL DATA TEXTURE (Noise blocks)
for _ in range(100):
    x = random.uniform(0, width)
    y = random.uniform(0, height)
    # Filter to keep center relatively clear or create specific density
    dist_to_center = math.sqrt((x-cx)**2 + (y-cy)**2)
    if dist_to_center > 150:
        alpha = random.uniform(0.05, 0.2)
        ctx.set_source_rgba(0.8, 0.9, 1.0, alpha)
        ctx.rectangle(x, y, random.uniform(1, 10), 1)
        ctx.fill()

# Fine Swiss borders / crop marks
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(1)
ctx.move_to(20, 20)
ctx.line_to(40, 20)
ctx.move_to(20, 20)
ctx.line_to(20, 40)
ctx.stroke()

ctx.move_to(width-20, height-20)
ctx.line_to(width-40, height-20)
ctx.move_to(width-20, height-20)
ctx.line_to(width-20, height-40)
ctx.stroke()
