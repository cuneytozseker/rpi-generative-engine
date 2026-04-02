import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for a Swiss-Brutalist base
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
layers = 3
ring_count = 40
spoke_count = 72

def get_polar_pos(r, theta, distortion_factor=0.0):
    """
    Calculates a polar-to-cartesian coordinate with a radial distortion 
    based on the angular position (Swiss-grid-to-organic-form).
    """
    # Radial distortion: creates a pulsing, rhythmic expansion
    # The distortion uses a harmonic of the angle to create 'waves' in the grid
    distorted_r = r * (1 + distortion_factor * math.sin(theta * 8))
    x = center_x + distorted_r * math.cos(theta)
    y = center_y + distorted_r * math.sin(theta)
    return x, y

def draw_structural_grid(ctx, r_step, theta_step, distortion, color, line_width, alpha):
    """Draws a distorted radial grid representing the systematic infrastructure."""
    ctx.set_line_width(line_width)
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    
    # Draw Rings (Concentric Circles)
    for i in range(1, ring_count + 1):
        radius = i * r_step
        ctx.new_path()
        for j in range(spoke_count + 1):
            angle = j * (2 * math.pi / spoke_count)
            x, y = get_polar_pos(radius, angle, distortion)
            if j == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.stroke()

    # Draw Spokes (Radial Lines)
    for j in range(spoke_count):
        angle = j * (2 * math.pi / spoke_count)
        ctx.new_path()
        for i in range(ring_count + 1):
            radius = i * r_step
            x, y = get_polar_pos(radius, angle, distortion)
            if i == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        ctx.stroke()

def draw_nodes(ctx, r_step, theta_step, distortion):
    """Places glyph-like nodes at intersections to highlight the 'node-to-many' connectivity."""
    for i in range(4, ring_count, 4):
        radius = i * r_step
        for j in range(0, spoke_count, 6):
            angle = j * (2 * math.pi / spoke_count)
            x, y = get_polar_pos(radius, angle, distortion)
            
            # Draw a 'Swiss Cross' node
            size = 2.5
            ctx.set_source_rgba(1.0, 0.2, 0.2, 0.8) # High contrast Red accent
            ctx.set_line_width(0.7)
            ctx.move_to(x - size, y)
            ctx.line_to(x + size, y)
            ctx.move_to(x, y - size)
            ctx.line_to(x, y + size)
            ctx.stroke()
            
            # Subtle node shadow/glow
            ctx.set_source_rgba(1, 1, 1, 0.1)
            ctx.arc(x, y, 1.5, 0, 2 * math.pi)
            ctx.fill()

# --- Execution ---

# 1. Base Layer: Static, rigid grid (Low distortion)
# This acts as the mathematical anchor of the composition
draw_structural_grid(
    ctx, 
    r_step=max_radius/ring_count, 
    theta_step=2*math.pi/spoke_count, 
    distortion=0.02, 
    color=(0.3, 0.3, 0.3), 
    line_width=0.4, 
    alpha=0.4
)

# 2. Emergent Layer: Interplay of two distorted grids (The Moire Layer)
# This creates optical texture and 'shrouds' of geometry
draw_structural_grid(
    ctx, 
    r_step=(max_radius/ring_count) * 1.05, 
    theta_step=2*math.pi/spoke_count, 
    distortion=0.08, 
    color=(0.8, 0.8, 0.8), 
    line_width=0.2, 
    alpha=0.2
)

draw_structural_grid(
    ctx, 
    r_step=(max_radius/ring_count) * 0.95, 
    theta_step=2*math.pi/spoke_count, 
    distortion=-0.06, 
    color=(0.9, 0.9, 1.0), 
    line_width=0.15, 
    alpha=0.3
)

# 3. Connectivity Layer: Node highlights
# Using the distortion from the second layer for alignment
draw_nodes(ctx, max_radius/ring_count, 2*math.pi/spoke_count, 0.08)

# 4. Focal Element: The Seed
# A high-contrast central core following Swiss hierarchy
ctx.set_source_rgba(1, 1, 1, 1)
ctx.set_line_width(1.5)
ctx.arc(center_x, center_y, 12, 0, 2 * math.pi)
ctx.stroke()
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.arc(center_x, center_y, 8, 0, 2 * math.pi)
ctx.fill()

# Final texture: Subtle noise-like grain (simulated with random dashes)
ctx.set_source_rgba(1, 1, 1, 0.03)
for _ in range(1000):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.rectangle(tx, ty, 0.5, 0.5)
    ctx.fill()

# IMPORTANT: No write_to_png call as per instructions
