import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_polar_shard(cx, cy, r1, r2, t1, t2, color, weight, style="solid"):
    """Draws a segment of a ring (a polar 'rectangle')"""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    if style == "solid":
        ctx.arc(cx, cy, r1, t1, t2)
        ctx.line_to(*polar_to_cartesian(cx, cy, r2, t2))
        ctx.arc_negative(cx, cy, r2, t2, t1)
        ctx.close_path()
        ctx.fill()
    elif style == "outline":
        ctx.arc(cx, cy, r1, t1, t2)
        ctx.stroke()
        ctx.arc(cx, cy, r2, t1, t2)
        ctx.stroke()
    elif style == "hatch":
        # Radial hatching
        steps = int(max(3, (t2 - t1) * 20))
        for i in range(steps + 1):
            t = t1 + (t2 - t1) * (i / steps)
            p1 = polar_to_cartesian(cx, cy, r1, t)
            p2 = polar_to_cartesian(cx, cy, r2, t)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
        ctx.stroke()
    elif style == "dots":
        # Stochastic dot distribution within the sector
        dots = int((r2 - r1) * (t2 - t1) * 2)
        for _ in range(dots):
            dr = random.uniform(r1, r2)
            dt = random.uniform(t1, t2)
            px, py = polar_to_cartesian(cx, cy, dr, dt)
            ctx.arc(px, py, weight/2, 0, math.pi * 2)
            ctx.fill()

def recursive_polar_grid(cx, cy, r1, r2, t1, t2, depth):
    """Hierarchical partitioning of a polar space"""
    
    # Base case or random termination based on 'Digital Stratigraphy'
    # Use a radial attractor to influence density: center is denser
    dist_from_center = (r1 + r2) / 2
    stop_prob = 0.3 + (dist_from_center / (width/2)) * 0.4
    
    if depth > 5 or (depth > 1 and random.random() < stop_prob):
        # Determine visual content of the leaf node cell
        seed = random.random()
        gray = random.uniform(0.7, 1.0)
        alpha = random.uniform(0.4, 0.9)
        
        # Stochastic Erosion: some cells remain empty
        if seed < 0.15:
            return 
        
        # Fragmented Logic: assign styles based on depth and position
        if seed < 0.4:
            draw_polar_shard(cx, cy, r1, r2, t1, t2, (gray, gray, gray, alpha), 0.5, "hatch")
        elif seed < 0.6:
            draw_polar_shard(cx, cy, r1, r2, t1, t2, (gray, gray, gray, alpha), 1.0, "dots")
        elif seed < 0.8:
            # Thin architectural lines
            draw_polar_shard(cx, cy, r1, r2, t1, t2, (gray, gray, gray, alpha*0.5), 0.3, "outline")
        else:
            # Solid shard - the 'stratigraphy' layers
            # Slightly offset to create 'glitch' effect
            offset = random.uniform(-0.02, 0.02)
            draw_polar_shard(cx, cy, r1 + offset, r2 - offset, t1 + offset, t2 - offset, (gray, gray, gray, alpha), 0, "solid")
        return

    # Subdivision Logic
    # Alternate between splitting radius and splitting angle
    if depth % 2 == 0:
        # Split radially
        mid_r = r1 + (r2 - r1) * random.uniform(0.3, 0.7)
        recursive_polar_grid(cx, cy, r1, mid_r, t1, t2, depth + 1)
        recursive_polar_grid(cx, cy, mid_r, r2, t1, t2, depth + 1)
    else:
        # Split angularly
        mid_t = t1 + (t2 - t1) * random.uniform(0.3, 0.7)
        recursive_polar_grid(cx, cy, r1, r2, t1, mid_t, depth + 1)
        recursive_polar_grid(cx, cy, r1, r2, mid_t, t2, depth + 1)

# Execution
cx, cy = width / 2, height / 2

# Layer 1: Subtle background structure (large radial lines)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for i in range(24):
    angle = i * (math.pi * 2 / 24)
    ctx.move_to(cx, cy)
    ctx.line_to(*polar_to_cartesian(cx, cy, width * 0.8, angle))
    ctx.stroke()

# Layer 2: Main Recursive Composition
# We divide the circle into 4 quadrants initially to ensure balanced asymmetry
num_sectors = 4
for i in range(num_sectors):
    t_start = i * (math.pi * 2 / num_sectors)
    t_end = (i + 1) * (math.pi * 2 / num_sectors)
    recursive_polar_grid(cx, cy, 20, width * 0.45, t_start, t_end, 0)

# Layer 3: High-contrast "Glitch" Shards
# These sit on top and break the grid logic
for _ in range(12):
    r_base = random.uniform(50, width * 0.4)
    t_base = random.uniform(0, math.pi * 2)
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(random.uniform(1, 3))
    
    # A single high-contrast radial tick
    p1 = polar_to_cartesian(cx, cy, r_base, t_base)
    p2 = polar_to_cartesian(cx, cy, r_base + 30, t_base)
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()

# Layer 4: Minimal Type-like elements (Swiss hierarchy)
# Using small rectangles as symbolic glyphs
for _ in range(20):
    r = random.uniform(100, 250)
    t = random.uniform(0, math.pi * 2)
    px, py = polar_to_cartesian(cx, cy, r, t)
    
    ctx.save()
    ctx.translate(px, py)
    ctx.rotate(t + math.pi/2)
    ctx.set_source_rgb(1, 1, 1)
    # Draw tiny modular "bits"
    h = random.choice([2, 4, 8])
    ctx.rectangle(0, 0, 1.5, h)
    ctx.fill()
    ctx.restore()

# Edge Vignette / Radial Distortion masking
# To simulate the atmospheric periphery
gradient = cairo.RadialGradient(cx, cy, width * 0.2, cx, cy, width * 0.5)
gradient.add_color_stop_rgba(0, 0, 0, 0, 0)
gradient.add_color_stop_rgba(1, 0.02, 0.02, 0.03, 1)
ctx.set_source(gradient)
ctx.paint()

