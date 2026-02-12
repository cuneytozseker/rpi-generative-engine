import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep midnight void
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Constants
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
MAX_DEPTH = 5

def to_polar(norm_x, norm_y, distortion=0):
    """Maps normalized 0-1 coordinates to polar space with radial distortion."""
    angle = norm_x * 2 * math.pi - math.pi / 2
    # Apply a harmonic radial distortion based on angle
    radius_mod = distortion * math.sin(angle * 8) * 10
    radius = norm_y * MAX_RADIUS + radius_mod
    
    px = CENTER_X + radius * math.cos(angle)
    py = CENTER_Y + radius * math.sin(angle)
    return px, py

def draw_polar_cell(nx, ny, nw, nh, depth):
    """Renders a subdivided cell as a polar segment with spectral lighting."""
    
    # Calculate corners in polar space
    p1 = to_polar(nx, ny)
    p2 = to_polar(nx + nw, ny)
    p3 = to_polar(nx + nw, ny + nh)
    p4 = to_polar(nx, ny + nh)

    # Calculate color based on position and depth
    # Spectral palette: Cyan, Magenta, White
    hue_shift = (nx + ny) * 0.5
    r = 0.1 + 0.9 * math.sin(hue_shift * math.pi)
    g = 0.5 + 0.5 * math.cos(hue_shift * math.pi * 2)
    b = 0.8 + 0.2 * math.sin(depth)
    
    # Transparency layers for "ordered decay" effect
    alpha = max(0.1, 1.0 - (depth / MAX_DEPTH))
    
    # 1. Draw the 'Atmospheric' glow (Soft Layer)
    grad = cairo.RadialGradient(CENTER_X, CENTER_Y, ny * MAX_RADIUS, 
                                CENTER_X, CENTER_Y, (ny + nh) * MAX_RADIUS)
    grad.add_color_stop_rgba(0, r, g, b, alpha * 0.3)
    grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(grad)
    ctx.move_to(*p1)
    # Using arcs for the radial boundaries for "precision"
    ctx.arc(CENTER_X, CENTER_Y, ny * MAX_RADIUS, 
            nx * 2 * math.pi - math.pi/2, (nx + nw) * 2 * math.pi - math.pi/2)
    ctx.line_to(*p3)
    ctx.arc_negative(CENTER_X, CENTER_Y, (ny + nh) * MAX_RADIUS, 
                     (nx + nw) * 2 * math.pi - math.pi/2, nx * 2 * math.pi - math.pi/2)
    ctx.close_path()
    ctx.fill()

    # 2. Draw the high-precision Swiss linework
    ctx.set_source_rgba(r, g, b, alpha * 0.8)
    ctx.set_line_width(0.5 if depth < 3 else 0.2)
    
    # Jittering effect on the outer edges (Stochastic Dispersion)
    jitter = (depth / MAX_DEPTH) * 2.0
    
    ctx.move_to(p1[0] + random.uniform(-jitter, jitter), p1[1])
    ctx.arc(CENTER_X, CENTER_Y, ny * MAX_RADIUS, 
            nx * 2 * math.pi - math.pi/2, (nx + nw) * 2 * math.pi - math.pi/2)
    ctx.stroke()

def recursive_partition(nx, ny, nw, nh, depth):
    """Quadtree logic to subdivide space based on proximity to center."""
    
    # Probability of subdivision increases toward the edge for "Resonance"
    # Or based on a mathematical attractor
    dist_to_center = math.sqrt((nx-0.5)**2 + (ny-0.5)**2)
    subdivide_chance = 0.4 + (dist_to_center * 0.5)
    
    if depth < MAX_DEPTH and (random.random() < subdivide_chance or depth < 2):
        half_w = nw / 2
        half_h = nh / 2
        recursive_partition(nx, ny, half_w, half_h, depth + 1)
        recursive_partition(nx + half_w, ny, half_w, half_h, depth + 1)
        recursive_partition(nx, ny + half_h, half_w, half_h, depth + 1)
        recursive_partition(nx + half_w, ny + half_h, half_w, half_h, depth + 1)
    else:
        draw_polar_cell(nx, ny, nw, nh, depth)

# Execution
random.seed(42) # Deterministic for aesthetic control

# Layer 1: The underlying structural skeleton (Fixed grid)
ctx.set_line_width(0.1)
ctx.set_source_rgba(1, 1, 1, 0.05)
for i in range(12):
    r_ring = (i / 12) * MAX_RADIUS
    ctx.arc(CENTER_X, CENTER_Y, r_ring, 0, 2 * math.pi)
    ctx.stroke()

# Layer 2: The recursive resonance system
recursive_partition(0, 0.1, 1.0, 0.9, 0)

# Layer 3: Chromatic "light-bleed" overlay
# Adds horizontal jittered lines to simulate digital scan/decay
for _ in range(40):
    y_pos = random.uniform(0, height)
    ctx.set_source_rgba(0.5, 0.8, 1.0, random.uniform(0.01, 0.05))
    ctx.set_line_width(random.uniform(1, 4))
    ctx.move_to(0, y_pos)
    ctx.line_to(width, y_pos)
    ctx.stroke()

# Final focal element - The Core
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.arc(CENTER_X, CENTER_Y, 2, 0, 2 * math.pi)
ctx.fill()

# Geometric "Swiss" labels (abstracted)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.set_source_rgba(1, 1, 1, 0.4)
for i in range(4):
    angle = i * (math.pi / 2)
    tx = CENTER_X + (MAX_RADIUS + 20) * math.cos(angle)
    ty = CENTER_Y + (MAX_RADIUS + 20) * math.sin(angle)
    ctx.move_to(tx, ty)
    ctx.show_text(f"RES_P.{i+1:02d}")

# Finalizing
ctx.stroke()
