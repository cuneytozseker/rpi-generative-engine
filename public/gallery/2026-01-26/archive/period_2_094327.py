import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - High contrast black
ctx.set_source_rgb(0, 0, 0)
ctx.paint()

def get_flow(x, y, scale=0.005):
    """Generates a pseudo-vector field based on trigonometric interference."""
    v1 = math.sin(x * scale + y * scale)
    v2 = math.cos(y * scale - x * scale)
    angle = (v1 + v2) * math.pi
    return angle

def draw_technical_grid(ctx, spacing, w, h):
    """Adds a layer of Swiss-style technical markers."""
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(1, 1, 1, 0.2)
    
    for x in range(0, w, spacing):
        for y in range(0, h, spacing):
            # Small crosshair markers
            size = 2
            ctx.move_to(x - size, y)
            ctx.line_to(x + size, y)
            ctx.move_to(x, y - size)
            ctx.line_to(x, y + size)
            ctx.stroke()
            
            # Subtle coordinate text-like marks (rectangles)
            if random.random() > 0.95:
                ctx.rectangle(x + 2, y + 2, 8, 2)
                ctx.fill()

def draw_flow_path(ctx, start_x, start_y, steps=40):
    """Draws a segmented path mimicking reaction-diffusion growth lines."""
    x, y = start_x, start_y
    ctx.move_to(x, y)
    
    # Opacity stacking based on position to create 'density nodes'
    alpha = 0.3 + (math.sin(x * 0.01) * 0.2)
    ctx.set_source_rgba(1, 1, 1, alpha)
    
    for i in range(steps):
        angle = get_flow(x, y)
        # Add slight 'chaos' to the calculation
        step_len = 3 + random.uniform(0, 2)
        x += math.cos(angle) * step_len
        y += math.sin(angle) * step_len
        
        # Keep within bounds with a slight margin
        if 0 <= x <= width and 0 <= y <= height:
            ctx.line_to(x, y)
        else:
            break
            
    ctx.set_line_width(0.8)
    ctx.stroke()

# 1. LAYER: TECHNICAL SUBSTRATE
draw_technical_grid(ctx, 40, width, height)

# 2. LAYER: CALCULATED CHAOS (Flow Field)
# We use asymmetric density - more concentrated on the left/top
num_paths = 1800
for _ in range(num_paths):
    # Biased distribution to create "asymmetric tension"
    rx = random.uniform(0, width)
    ry = random.uniform(0, height)
    
    # Weighting: denser clusters in specific zones
    if random.random() < 0.6:
        draw_flow_path(ctx, rx, ry, steps=random.randint(15, 60))

# 3. LAYER: RAY-CASTING INTERSECTIONS
# Rigid, straight lines that cut through the fluid paths
ctx.set_source_rgba(1, 1, 1, 0.6)
ctx.set_line_width(0.3)
for i in range(12):
    x_pos = random.uniform(50, width-50)
    # Vertical rays mimicking technical scan lines
    ctx.move_to(x_pos, 20)
    ctx.line_to(x_pos, height - 20)
    ctx.stroke()
    
    # Add a "data node" circle at intersection
    if random.random() > 0.5:
        ctx.arc(x_pos, random.uniform(0, height), 2, 0, 2 * math.pi)
        ctx.fill()

# 4. LAYER: MOIRÉ DENSITY NODES
# Highlight areas where 'logic' peaks with higher opacity shapes
for _ in range(5):
    nx, ny = random.uniform(100, 500), random.uniform(100, 400)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    for r in range(5, 40, 5):
        ctx.set_line_width(0.5)
        ctx.arc(nx, ny, r, 0, math.pi * 0.5) # Quarter circles for Swiss precision
        ctx.stroke()

# Final border to ground the composition (Swiss style)
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.rectangle(10, 10, width - 20, height - 20)
ctx.stroke()

