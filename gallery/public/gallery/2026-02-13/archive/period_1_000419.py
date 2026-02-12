import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for Brutalist contrast
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Constants for the Polar System
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
accent_colors = [
    (1.0, 0.2, 0.1), # Swiss Red
    (0.0, 0.6, 0.9), # Cyan Punctuation
    (1.0, 0.8, 0.0)  # Signal Yellow
]

def polar_to_cart(r, theta):
    """Converts polar coordinates to Cartesian, centered on the canvas."""
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return x, y

def draw_curved_rect(r1, r2, t1, t2, fill=False, weight=0.5):
    """Draws a segment of a polar grid (an annular sector)."""
    ctx.set_line_width(weight)
    
    # Path construction
    ctx.arc(center_x, center_y, r1, t1, t2)
    p2_x, p2_y = polar_to_cart(r2, t2)
    ctx.line_to(p2_x, p2_y)
    ctx.arc_negative(center_x, center_y, r2, t2, t1)
    ctx.close_path()
    
    if fill:
        ctx.fill()
    else:
        ctx.stroke()

def subdivide_polar(r_min, r_max, t_min, t_max, depth):
    """Recursive function to partition space based on centripetal density."""
    
    # Calculate current distance from center (normalized 0 to 1)
    dist_ratio = (r_min / max_radius)
    
    # Logic: Higher probability of subdivision closer to the center (centripetal tension)
    # and higher probability at lower recursion depths.
    split_chance = (1.5 - dist_ratio) * 0.7
    
    if depth < 5 and random.random() < split_chance:
        # Determine whether to split radially or angularly
        # Radial splits create 'rings', angular splits create 'wedges'
        if random.random() > 0.5:
            # Split Angularly
            mid_t = (t_min + t_max) / 2
            subdivide_polar(r_min, r_max, t_min, mid_t, depth + 1)
            subdivide_polar(r_min, r_max, mid_t, t_max, depth + 1)
        else:
            # Split Radially - use a weighted split to push density inward
            bias = 0.4 + (random.random() * 0.2)
            mid_r = r_min + (r_max - r_min) * bias
            subdivide_polar(r_min, mid_r, t_min, t_max, depth + 1)
            subdivide_polar(mid_r, r_max, t_min, t_max, depth + 1)
    else:
        # Render the leaf cell
        render_cell(r_min, r_max, t_min, t_max, dist_ratio, depth)

def render_cell(r1, r2, t1, t2, dist, depth):
    """Visualizes the specific cell with Swiss-inspired logic."""
    
    # Determine visual style based on distance and random seed
    style_roll = random.random()
    
    # Subtractive Sparsity: Leave some cells empty
    if style_roll < 0.2:
        return

    # Chromatic Punctuation: Rare vibrant accents
    if style_roll > 0.96:
        color = random.choice(accent_colors)
        ctx.set_source_rgba(*color, 0.9)
        draw_curved_rect(r1, r2, t1, t2, fill=True)
        return

    # Line Weight Modulation: Hairlines vs Bold
    # Cells closer to center or at deep recursion get finer lines
    line_w = 0.2 if dist > 0.5 else 1.2
    alpha = 0.8 - (dist * 0.5) # Fade out towards periphery
    
    ctx.set_source_rgba(1, 1, 1, alpha)
    
    if style_roll > 0.7:
        # Solid Block (Brutalist element)
        draw_curved_rect(r1, r2, t1, t2, fill=True)
    elif style_roll > 0.4:
        # Outline Cell
        draw_curved_rect(r1, r2, t1, t2, fill=False, weight=line_w)
    else:
        # Internal Hierarchy: Draw a smaller inset element
        padding_r = (r2 - r1) * 0.2
        padding_t = (t2 - t1) * 0.2
        draw_curved_rect(r1 + padding_r, r2 - padding_r, t1 + padding_t, t2 - padding_t, fill=False, weight=line_w/2)

# --- Execute Generative Logic ---

# Create base radial structure (The Swiss Grid foundation)
num_primary_sectors = 12
for i in range(num_primary_sectors):
    angle_start = (i / num_primary_sectors) * (2 * math.pi)
    angle_end = ((i + 1) / num_primary_sectors) * (2 * math.pi)
    
    # Create concentric tiers for recursion
    num_tiers = 4
    for j in range(num_tiers):
        # Non-linear radial spacing to create distortion
        r_start = (j / num_tiers)**1.5 * max_radius
        r_end = ((j + 1) / num_tiers)**1.5 * max_radius
        
        subdivide_polar(r_start, r_end, angle_start, angle_end, 0)

# Add Mathematical Overlays (The "Glitch" layer)
# Precision guide lines cutting through the composition
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.3)
for i in range(24):
    angle = (i / 24) * 2 * math.pi
    x1, y1 = polar_to_cart(max_radius * 0.1, angle)
    x2, y2 = polar_to_cart(max_radius * 1.1, angle)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Final focal point: The "Void" Core
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.arc(center_x, center_y, max_radius * 0.05, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1.5)
ctx.arc(center_x, center_y, max_radius * 0.05, 0, 2 * math.pi)
ctx.stroke()

# Add small typographic-like markers (Systematic anchors)
for _ in range(12):
    r = random.uniform(max_radius * 0.8, max_radius * 1.0)
    theta = random.uniform(0, 2 * math.pi)
    x, y = polar_to_cart(r, theta)
    ctx.rectangle(x-2, y-2, 4, 4)
    ctx.fill()

