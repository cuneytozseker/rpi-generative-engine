import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal (Swiss Minimalist Base)
ctx.set_source_rgb(0.08, 0.08, 0.09)
ctx.paint()

def polar_to_cartesian(cx, cy, r, angle):
    return cx + r * math.cos(angle), cy + r * math.sin(angle)

def draw_anchor(x, y, size, color):
    """Small geometric markers to ground the abstract movement."""
    ctx.set_source_rgba(*color)
    ctx.rectangle(x - size/2, y - size/2, size, size)
    ctx.fill()

def get_systemic_color(depth, radius):
    """Logic-based color assignment: Earthy tones with a high-saturation accent."""
    # Palette: Bone, Slate, Clay, and Swiss International Orange
    palette = [
        (0.92, 0.89, 0.83), # Bone
        (0.55, 0.52, 0.48), # Muted Clay
        (0.35, 0.38, 0.42), # Slate
    ]
    
    # Rare high-saturation accent logic
    if random.random() > 0.96:
        return (1.0, 0.22, 0.05, 0.9) # Swiss Red/Orange
        
    color = list(palette[depth % len(palette)])
    # Fade based on radius to simulate dissolution
    alpha = max(0.2, 1.0 - (radius / 400))
    color.append(alpha)
    return tuple(color)

def recursive_polar_grid(cx, cy, r_start, r_end, a_start, a_end, depth):
    if depth > 5 or (depth > 2 and random.random() > 0.85):
        # Calculate distortion based on a vector field-like influence
        # Entropy increases with radius
        entropy = (r_start / 300.0) ** 2
        offset_a = math.sin(r_start * 0.05) * 0.1 * entropy
        offset_r = math.cos(a_start * 3) * 15 * entropy
        
        r1, r2 = r_start + offset_r, r_end + offset_r
        a1, a2 = a_start + offset_a, a_end + offset_a
        
        # Color based on recursion logic
        color = get_systemic_color(depth, r1)
        ctx.set_source_rgba(*color)
        
        # Staccato Density: Use modulated line weights
        ctx.set_line_width(0.5 + (5 / (depth + 1)))
        
        # Draw distorted arc segment
        # We draw as a path of segments to allow for varied thickness or stippling
        res = 8
        ctx.move_to(*polar_to_cartesian(cx, cy, r1, a1))
        for i in range(res + 1):
            angle = a1 + (a2 - a1) * (i / res)
            ctx.line_to(*polar_to_cartesian(cx, cy, r1, angle))
        
        # Occasional radial connection
        if random.random() > 0.5:
            ctx.line_to(*polar_to_cartesian(cx, cy, r2, a2))
            
        ctx.stroke()
        
        # Anchor points at intersections
        if depth % 2 == 0:
            anchor_x, anchor_y = polar_to_cartesian(cx, cy, r1, a1)
            draw_anchor(anchor_x, anchor_y, 2.5 / (depth + 1), color)

        return

    # Subdivision logic
    r_mid = (r_start + r_end) / 2
    a_mid = (a_start + a_end) / 2
    
    # Recursive branching
    # Alternating radial and angular splits for grid feel
    if depth % 2 == 0:
        recursive_polar_grid(cx, cy, r_start, r_mid, a_start, a_end, depth + 1)
        recursive_polar_grid(cx, cy, r_mid, r_end, a_start, a_end, depth + 1)
    else:
        recursive_polar_grid(cx, cy, r_start, r_end, a_start, a_mid, depth + 1)
        recursive_polar_grid(cx, cy, r_start, r_end, a_mid, a_end, depth + 1)

# Main Execution
cx, cy = width / 2, height / 2

# Draw multiple layers of the transformed grid
for i in range(6):
    # Rotate each layer slightly
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(i * (math.pi / 3))
    ctx.translate(-cx, -cy)
    
    # Polar subdivision of the circle
    num_sectors = 6
    for s in range(num_sectors):
        angle_step = (2 * math.pi) / num_sectors
        recursive_polar_grid(
            cx, cy, 
            30, 320, 
            s * angle_step, (s + 1) * angle_step, 
            0
        )
    ctx.restore()

# Add a "System Blueprint" overlay: subtle concentric circles for structural tension
ctx.set_source_rgba(1, 1, 1, 0.03)
ctx.set_line_width(0.5)
for r in range(50, 400, 50):
    ctx.arc(cx, cy, r, 0, 2 * math.pi)
    ctx.stroke()

# Focal point: High-density core
ctx.set_source_rgba(0.92, 0.89, 0.83, 0.8)
ctx.arc(cx, cy, 3, 0, 2 * math.pi)
ctx.fill()

# Final noise texture (staccato digital vibration)
for _ in range(800):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.15))
    ctx.rectangle(tx, ty, 1, 1)
    ctx.fill()

