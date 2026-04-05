import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.06)
ctx.paint()

# Configuration for the Systematic Grid
center_x, center_y = width * 0.45, height * 0.55  # Asymmetric weight
rows = 40 
cols = 60
base_radius = 40
max_radius = 450
distortion_factor = 1.8  # Spiral twist intensity

def get_polar_coords(r_idx, theta_idx):
    """
    Transforms a standard Cartesian grid coordinate into a 
    distorted polar coordinate space with non-linear radial expansion.
    """
    # Normalized progress
    nr = r_idx / rows
    nt = theta_idx / cols
    
    # Mathematical logic for the grid transformation
    angle = nt * 2 * math.pi
    # Non-linear radius expansion (Swiss precision meets organic growth)
    radius = base_radius + (max_radius - base_radius) * (nr ** 1.5)
    
    # Radial distortion: twist increases with distance
    twist = nr * distortion_factor
    final_angle = angle + twist
    
    x = center_x + radius * math.cos(final_angle)
    y = center_y + radius * math.sin(final_angle)
    return x, y, radius, final_angle

# Draw the modular fluid system
for r in range(rows):
    # Calculate density modulation based on radius
    # Stochastic skip: creates "breathing room" in the grid
    if random.random() < 0.1: continue
    
    # Line weight increases toward the center of the vortex, then thins out
    normalized_r = r / rows
    line_weight = 0.3 + 2.5 * math.exp(-((normalized_r - 0.4) ** 2) / 0.05)
    
    for t in range(cols):
        # Sample points for the module segment
        x1, y1, rad1, ang1 = get_polar_coords(r, t)
        x2, y2, rad2, ang2 = get_polar_coords(r, t + 0.7) # Segment length
        
        # Color interaction: Monochromatic with high-tension accents
        # Occasional Swiss Red (0.9, 0.1, 0.1) or neutral grey
        if random.random() > 0.98:
            ctx.set_source_rgb(0.95, 0.1, 0.1) # Accent
            ctx.set_line_width(line_weight * 2)
        elif t % 10 == 0:
            ctx.set_source_rgb(0.9, 0.9, 0.95) # Bright Neutral
            ctx.set_line_width(line_weight)
        else:
            ctx.set_source_rgb(0.4, 0.4, 0.45) # Muted Neutral
            ctx.set_line_width(line_weight * 0.5)

        # Draw the module - using arcs for "Fluidity"
        ctx.move_to(x1, y1)
        # Instead of straight line_to, use arc for curvature consistency
        ctx.arc(center_x, center_y, rad1, ang1 + (r * 0.045), ang2 + (r * 0.045))
        ctx.stroke()

        # Add "Focal Gravity" clusters (Small data markers)
        if r % 8 == 0 and t % 12 == 0:
            ctx.set_source_rgb(0.8, 0.8, 0.8)
            ctx.arc(x1, y1, 1.5, 0, 2 * math.pi)
            ctx.fill()
            
# Secondary Layer: Structural Cartesian Ghost
# Subtle vertical bars to ground the composition against the polar flow
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.1)
for i in range(0, width, 40):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()

# Final Detail: Geometric Rhythm Interruption
# Large, hollow circles that intersect the flow, creating visual hierarchy
ctx.set_line_width(0.8)
for i in range(3):
    r_size = 120 + i * 80
    alpha = 0.3 - (i * 0.1)
    ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
    ctx.arc(center_x, center_y, r_size, 0, math.pi * 0.5) # Partial arcs
    ctx.stroke()
    
    # Typographic-like block elements
    ctx.rectangle(center_x + r_size - 5, center_y - 5, 10, 10)
    ctx.fill()

# Clean border for Swiss aesthetic
ctx.set_source_rgb(0.05, 0.05, 0.06)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
