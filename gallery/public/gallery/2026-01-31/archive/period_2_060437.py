import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep technical void
ctx.set_source_rgb(0.02, 0.02, 0.03) 
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_glitched_arc(ctx, cx, cy, r, start_angle, end_angle, fragments=5):
    """Draws an arc as a series of fragmented segments to simulate digital decay."""
    step = (end_angle - start_angle) / fragments
    for i in range(fragments):
        if random.random() > 0.2:  # Controlled entropy: some segments vanish
            s = start_angle + i * step
            e = s + step * 0.8  # Gap between fragments
            ctx.arc(cx, cy, r, s, e)
            ctx.stroke()

# Configuration for the "Glitched Blueprint"
cx, cy = width / 2, height / 2
rings = 18
slices = 40
max_radius = min(width, height) * 0.45

# Set base line properties
ctx.set_line_cap(cairo.LINE_CAP_BUTT)

# 1. LAYER: THE UNDERLYING MATHEMATICAL SCAFFOLD (Subtle)
ctx.set_source_rgba(0.2, 0.4, 0.8, 0.15)  # Blueprint blue
ctx.set_line_width(0.5)
for i in range(rings):
    r = (i / rings) * max_radius
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()

for i in range(slices):
    theta = (i / slices) * 2 * math.pi
    x2, y2 = polar_to_cartesian(cx, cy, max_radius, theta)
    ctx.move_to(cx, cy)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 2. LAYER: SYSTEMIC FRAGMENTATION (The Core logic)
for i in range(1, rings):
    r = (i / rings) * max_radius
    # Decay function: elements become more erratic as they move outward
    entropy_factor = (i / rings) ** 1.5
    
    for j in range(slices):
        theta_start = (j / slices) * 2 * math.pi
        theta_end = ((j + 1) / slices) * 2 * math.pi
        
        # Center-weighted dispersion logic
        if random.random() > entropy_factor * 0.7:
            # Color logic: High contrast monochrome with technical accents
            if random.random() > 0.9:
                ctx.set_source_rgba(0.1, 0.5, 1.0, 0.8) # Technical blue accent
            else:
                brightness = 0.6 + (random.random() * 0.4)
                ctx.set_source_rgba(brightness, brightness, brightness, 0.9)

            # Determine visual "weight" based on proximity to center
            ctx.set_line_width(max(0.5, 4 * (1 - entropy_factor)))
            
            # Geometric Perturbation
            offset_r = (random.random() - 0.5) * 10 * entropy_factor
            
            # Draw block or fragmented line
            if random.random() > 0.3:
                draw_glitched_arc(ctx, cx, cy, r + offset_r, theta_start, theta_end, fragments=random.randint(2, 6))
            else:
                # Occasional radial "spikes" connecting layers
                r2 = r + (max_radius / rings) * random.uniform(0.5, 1.5)
                x1, y1 = polar_to_cartesian(cx, cy, r, theta_start)
                x2, y2 = polar_to_cartesian(cx, cy, r2, theta_start)
                ctx.move_to(x1, y1)
                ctx.line_to(x2, y2)
                ctx.stroke()

# 3. LAYER: DATA DEBRIS (Optical Mixing)
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.5)
for _ in range(200):
    # Dithered point cloud appearing in "fractures"
    angle = random.uniform(0, 2 * math.pi)
    # Weighted towards the center
    dist = (random.random() ** 0.5) * max_radius * 1.2
    px, py = polar_to_cartesian(cx, cy, dist, angle)
    
    size = random.uniform(0.5, 2.0)
    if random.random() > 0.5:
        ctx.rectangle(px, py, size, size) # Square "pixels"
    else:
        ctx.arc(px, py, size/2, 0, 2 * math.pi) # Round "nodes"
    ctx.fill()

# 4. LAYER: MARGINAL COORDINATES (Swiss precision markers)
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.set_line_width(1)
marker_r = max_radius + 20
for i in range(8):
    angle = (i / 8) * 2 * math.pi
    x1, y1 = polar_to_cartesian(cx, cy, marker_r, angle)
    x2, y2 = polar_to_cartesian(cx, cy, marker_r + 15, angle)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
    
    # Tiny crosshair markers at edges
    ctx.move_to(x1 - 3, y1)
    ctx.line_to(x1 + 3, y1)
    ctx.move_to(x1, y1 - 3)
    ctx.line_to(x1, y1 + 3)
    ctx.stroke()

# Final Polish: Central high-density node
ctx.set_source_rgba(1, 1, 1, 1)
ctx.arc(cx, cy, 3, 0, 2 * math.pi)
ctx.fill()
ctx.set_line_width(0.5)
ctx.arc(cx, cy, 8, 0, 2 * math.pi)
ctx.stroke()

