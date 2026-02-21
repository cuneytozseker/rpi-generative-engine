import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
num_rings = 40
num_sectors = 12
phi = (1 + math.sqrt(5)) / 2  # Golden ratio for organic spacing

def draw_polar_block(ctx, r1, r2, a1, a2, color, fill=True):
    """Draws a segment of a ring (a 'polar rectangle')"""
    ctx.set_source_rgba(*color)
    ctx.new_path()
    # Outer arc
    ctx.arc(center_x, center_y, r2, a1, a2)
    # Line to inner arc
    ctx.line_to(center_x + r1 * math.cos(a2), center_y + r1 * math.sin(a2))
    # Inner arc (reversed)
    ctx.arc_negative(center_x, center_y, r1, a2, a1)
    ctx.close_path()
    if fill:
        ctx.fill()
    else:
        ctx.stroke()

# 1. ATMOSPHERIC DIFFUSION (The Glow Core)
# Creating a radial gradient to simulate "chromatic diffusion" from the center
gradient = cairo.RadialGradient(center_x, center_y, 20, center_x, center_y, 300)
gradient.add_color_stop_rgba(0.0, 1.0, 1.0, 1.0, 0.15)  # Hot core
gradient.add_color_stop_rgba(0.4, 0.0, 0.5, 0.8, 0.05)  # Cool periphery
gradient.add_color_stop_rgba(1.0, 0.0, 0.0, 0.0, 0.0)   # Fade to black
ctx.set_source(gradient)
ctx.arc(center_x, center_y, 300, 0, 2 * math.pi)
ctx.fill()

# 2. THE SYSTEMATIC GRID (Polar Swiss Transformation)
# We use a non-linear subdivision for radii to create centripetal density
radii = [0]
current_r = 10
for i in range(num_rings):
    # Exponential expansion: density increases towards center
    current_r += 4 + (i * 0.4) 
    radii.append(current_r)

for i in range(len(radii) - 1):
    r_inner = radii[i]
    r_outer = radii[i+1]
    
    # Calculate angular segments - subdivision increases as we move out
    # This maintains a 'modular' grid size across the transformation
    current_sectors = num_sectors if i < 10 else num_sectors * 2
    angle_step = (2 * math.pi) / current_sectors
    
    for j in range(current_sectors):
        angle_start = j * angle_step
        angle_end = (j + 1) * angle_step
        
        # Systematic Randomness: decide if we draw a block, a line, or nothing
        seed = random.random()
        
        # Swiss Accent Color (Chromatic Interruption)
        # Higher probability of color near the center/axes
        is_axis = (j % (current_sectors//4) == 0)
        if seed > 0.92 or (is_axis and seed > 0.7):
            color = (1.0, 0.2, 0.3, 0.9) # Swiss Red/Pink
        elif seed > 0.8:
            color = (1.0, 1.0, 1.0, 0.8) # Pure White
        else:
            color = (1.0, 1.0, 1.0, 0.1) # Ghostly vectors
            
        # Geometric Logic: Draw different forms based on distance
        if seed > 0.4:
            # Draw structural blocks
            draw_polar_block(ctx, r_inner, r_outer, angle_start, angle_end, color, fill=(seed > 0.6))
        
        # 3. HAIR-LINE VECTORS (Precision Layer)
        if seed > 0.85:
            ctx.set_line_width(0.5)
            ctx.set_source_rgba(1, 1, 1, 0.4)
            # Draw radial 'stinger' lines
            ext_r = r_outer + 40
            ctx.move_to(center_x + r_outer * math.cos(angle_start), center_y + r_outer * math.sin(angle_start))
            ctx.line_to(center_x + ext_r * math.cos(angle_start), center_y + ext_r * math.sin(angle_start))
            ctx.stroke()

# 4. CROSS-HAIR HIERARCHY (The Tether)
# Reinforcing the central axis with high-contrast hairline strokes
ctx.set_line_width(0.75)
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.move_to(center_x, 0)
ctx.line_to(center_x, height)
ctx.move_to(0, center_y)
ctx.line_to(width, center_y)
ctx.stroke()

# 5. RECURSIVE SCALING (Small modules clustering)
# Small "data bits" near the center to imply complexity
for _ in range(100):
    a = random.uniform(0, 2 * math.pi)
    r = random.uniform(5, 50)
    size = random.uniform(1, 3)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.5, 1.0))
    ctx.rectangle(center_x + r * math.cos(a), center_y + r * math.sin(a), size, size)
    ctx.fill()

# Final Polish: A vignette ring to constrain the centripetal force
ctx.set_line_width(2)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.arc(center_x, center_y, 220, 0, 2 * math.pi)
ctx.stroke()
