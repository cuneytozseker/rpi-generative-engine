import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format for polar symmetry
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

def draw_polar_rect(ctx, cx, cy, r, theta, dr, dtheta, fill=False):
    """Draws a segment of a polar grid transformed into a trapezoidal/arc shape."""
    # Calculate corner points
    ctx.new_path()
    ctx.arc(cx, cy, r, theta, theta + dtheta)
    ctx.arc_negative(cx, cy, r + dr, theta + dtheta, theta)
    ctx.close_path()
    
    if fill:
        ctx.fill()
    else:
        ctx.stroke()

def recursive_subdivide(ctx, cx, cy, r, theta, dr, dtheta, depth):
    """
    Recursively subdivides polar cells based on distance from center.
    Entropy increases as depth increases and as radius increases.
    """
    # Deterministic entropy factor based on distance from center
    dist_factor = r / (width * 0.4)
    
    # Base case or random stop based on 'order vs entropy'
    if depth > 4 or (depth > 1 and random.random() < dist_factor * 0.7):
        # Draw the cell
        
        # Color Logic: High contrast monochrome with terminal accents
        is_accent = random.random() < 0.03 and dist_factor > 0.3
        
        if is_accent:
            # Vibrant Swiss Red or Electric Cyan punctuation
            ctx.set_source_rgb(1.0, 0.1, 0.2)
            ctx.set_line_width(2.0)
        else:
            # Varying greys based on depth (atmospheric perspective)
            val = min(1.0, 0.4 + (depth * 0.15))
            ctx.set_source_rgba(val, val, val, 0.9 - (dist_factor * 0.5))
            ctx.set_line_width(0.4 if depth > 2 else 1.2)

        # Style logic: Blocks vs Outlines
        if random.random() > 0.6 - (dist_factor * 0.3):
            draw_polar_rect(ctx, cx, cy, r, theta, dr, dtheta, fill=True)
        else:
            draw_polar_rect(ctx, cx, cy, r, theta, dr, dtheta, fill=False)
            
        # Add "hairline" detail connectors
        if random.random() < 0.2:
            ctx.set_source_rgba(1, 1, 1, 0.2)
            ctx.set_line_width(0.2)
            ctx.move_to(cx + r * math.cos(theta), cy + r * math.sin(theta))
            ctx.line_to(cx + (r + dr*2) * math.cos(theta), cy + (r + dr*2) * math.sin(theta))
            ctx.stroke()
            
        return

    # Subdivide logic
    mid_r = dr * (0.4 + random.random() * 0.2) # Non-linear spacing
    mid_theta = dtheta / 2
    
    # Recursive branches
    recursive_subdivide(ctx, cx, cy, r, theta, mid_r, mid_theta, depth + 1)
    recursive_subdivide(ctx, cx, cy, r + mid_r, theta, dr - mid_r, mid_theta, depth + 1)
    recursive_subdivide(ctx, cx, cy, r, theta + mid_theta, mid_r, dtheta - mid_theta, depth + 1)
    recursive_subdivide(ctx, cx, cy, r + mid_r, theta + mid_theta, dr - mid_r, dtheta - mid_theta, depth + 1)

# --- Execution ---

center_x, center_y = width / 2, height / 2
rings = 8
slices = 12

# Draw systematic scaffolding (The "Order")
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for i in range(rings):
    radius = (i + 1) * (width * 0.05)
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.stroke()

# Draw recursive grid (The "Entropy")
initial_dr = width * 0.06
for i in range(rings):
    # Logarithmic spacing for radial rings
    r_start = 40 + (i**1.6) * 10
    r_width = ( (i+1)**1.6 - i**1.6 ) * 10
    
    for s in range(slices):
        t_start = (s / slices) * 2 * math.pi
        t_width = (1 / slices) * 2 * math.pi
        
        # Introduce a "gap" in the grid for negative space hierarchy
        if (i + s) % 7 != 0:
            recursive_subdivide(ctx, center_x, center_y, r_start, t_start, r_width, t_width, 0)

# Final Overlays: High-precision radial lines to ground the composition
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.3)
for i in range(48):
    angle = (i / 48) * 2 * math.pi
    ctx.move_to(center_x + 50 * math.cos(angle), center_y + 50 * math.sin(angle))
    ctx.line_to(center_x + (width * 0.45) * math.cos(angle), center_y + (width * 0.45) * math.sin(angle))
    ctx.stroke()

# Add a central "Singularity" core
ctx.set_source_rgb(1, 1, 1)
ctx.arc(center_x, center_y, 4, 0, 2 * math.pi)
ctx.fill()

# Border for Swiss precision feel
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

