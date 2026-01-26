import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep monochromatic base
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_curved_rect(ctx, cx, cy, r1, r2, a1, a2):
    """Draws a 'rectangle' in polar space."""
    ctx.arc(cx, cy, r1, a1, a2)
    p2 = polar_to_cartesian(cx, cy, r2, a2)
    ctx.line_to(p2[0], p2[1])
    ctx.arc_negative(cx, cy, r2, a2, a1)
    ctx.close_path()

def recursive_subdivide(cx, cy, r1, r2, a1, a2, depth):
    if depth <= 0 or (random.random() > 0.8 and depth < 3):
        # Base case: Render the cell
        
        # Calculate centers for "data-like" pointillism
        mid_r = (r1 + r2) / 2
        mid_a = (a1 + a2) / 2
        px, py = polar_to_cartesian(cx, cy, mid_r, mid_a)
        
        # Randomly choose visual style for this cell
        style = random.random()
        
        if style < 0.4:
            # Atmospheric fluidity: Soft gradient-like fills
            alpha = random.uniform(0.1, 0.4)
            if random.random() > 0.7:
                ctx.set_source_rgba(1.0, 0.0, 0.4, alpha) # Neon Pink accent
            else:
                ctx.set_source_rgba(0.2, 0.4, 1.0, alpha * 0.5) # Spectral blue
            draw_curved_rect(ctx, cx, cy, r1, r2, a1, a2)
            ctx.fill()
            
        elif style < 0.6:
            # Technical precision: Razor-sharp linework
            ctx.set_source_rgba(1, 1, 1, 0.6)
            ctx.set_line_width(0.4)
            draw_curved_rect(ctx, cx, cy, r1, r2, a1, a2)
            ctx.stroke()
            
        elif style < 0.7:
            # Pointillism: Anchor points
            ctx.set_source_rgba(1, 1, 1, 0.8)
            ctx.arc(px, py, 1.2, 0, math.pi * 2)
            ctx.fill()

        # Rhythmic punctuation: High-chroma saturated blocks
        if random.random() > 0.96:
            ctx.set_source_rgb(1.0, 0.8, 0.0) # Golden highlight
            draw_curved_rect(ctx, cx, cy, r1, r2, a1, a2)
            ctx.fill()
            
        return

    # Non-linear subdivision logic
    # Alternate between splitting radius (concentric) and angle (radial)
    if depth % 2 == 0:
        # Split radius using a weighted ratio (closer to focal point)
        split = random.uniform(0.3, 0.7)
        mid_r = r1 + (r2 - r1) * split
        recursive_subdivide(cx, cy, r1, mid_r, a1, a2, depth - 1)
        recursive_subdivide(cx, cy, mid_r, r2, a1, a2, depth - 1)
    else:
        # Split angle
        split = random.uniform(0.4, 0.6)
        mid_a = a1 + (a2 - a1) * split
        recursive_subdivide(cx, cy, r1, r2, a1, mid_a, depth - 1)
        recursive_subdivide(cx, cy, r1, r2, mid_a, a2, depth - 1)

# Main Composition
cx, cy = width / 2, height / 2
rings = 8
max_radius = min(width, height) * 0.45

# Create a distorted Swiss Grid transformed to Polar coordinates
for i in range(rings):
    # Non-linear radial growth (Hierarchical scaling)
    r_start = max_radius * (i / rings)**1.5
    r_end = max_radius * ((i + 1) / rings)**1.5
    
    # Increase segment frequency as we move outward
    segments = 4 + (i * 2)
    angle_step = (math.pi * 2) / segments
    
    for j in range(segments):
        a_start = j * angle_step
        a_end = (j + 1) * angle_step
        
        # Apply slight radial distortion based on angle to simulate "pulse"
        distort = math.sin(a_start * 4) * 5
        
        # Start recursion within this sector
        ctx.save()
        recursive_subdivide(cx, cy, r_start + distort, r_end + distort, a_start, a_end, 4)
        ctx.restore()

# Final Layer: Overlay "technical" crosshairs and subtle grain
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.2)
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    p1 = polar_to_cartesian(cx, cy, 0, angle)
    p2 = polar_to_cartesian(cx, cy, max_radius * 1.1, angle)
    ctx.move_to(p1[0], p1[1])
    ctx.line_to(p2[0], p2[1])
    ctx.stroke()

# Central "Void" focal point
ctx.set_source_rgb(0,0,0)
ctx.arc(cx, cy, 15, 0, math.pi*2)
ctx.fill()
ctx.set_source_rgb(1,1,1)
ctx.set_line_width(1)
ctx.arc(cx, cy, 15, 0, math.pi*2)
ctx.stroke()

# IMPORTANT: Don't call surface.write_to_png()
