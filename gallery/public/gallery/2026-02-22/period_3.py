import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Stark Swiss Black
ctx.set_source_rgb(0, 0, 0)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = min(width, height) * 0.45
RINGS = 12
SECTORS = 24
SUBDIVISION_CHANCE = 0.6

def get_polar_coords(r, theta):
    """Converts polar coordinates to Cartesian for Cairo."""
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

def draw_polar_cell(r0, r1, t0, t1, depth=0):
    """
    Draws a wedge-shaped cell in polar space. 
    Implements recursive subdivision based on distance from center (entropy).
    """
    # Calculate middle points for potential subdivision
    mid_r = (r0 + r1) / 2
    mid_t = (t0 + t1) / 2
    
    # Distance-based probability: further from center = higher entropy/fragmentation
    normalized_dist = r1 / MAX_RADIUS
    entropy_trigger = random.random() < (SUBDIVISION_CHANCE * (1.0 - normalized_dist))
    
    if depth < 3 and entropy_trigger:
        # Recursive Subdivision: split the cell into 4 sub-cells
        draw_polar_cell(r0, mid_r, t0, mid_t, depth + 1)
        draw_polar_cell(mid_r, r1, t0, mid_t, depth + 1)
        draw_polar_cell(r0, mid_r, mid_t, t1, depth + 1)
        draw_polar_cell(mid_r, r1, mid_t, t1, depth + 1)
    else:
        # Render the leaf cell
        render_logic(r0, r1, t0, t1, depth, normalized_dist)

def render_logic(r0, r1, t0, t1, depth, dist):
    """Visualizes a specific cell based on its hierarchy and position."""
    
    # Margin for "Grid" feel
    margin_r = 1.5
    margin_t = 0.01 / (dist + 0.1)
    
    # Geometry Path
    def construct_wedge_path(ir0, ir1, it0, it1):
        ctx.arc(CENTER_X, CENTER_Y, ir0, it0, it1)
        ctx.line_to(*get_polar_coords(ir1, it1))
        ctx.arc_negative(CENTER_X, CENTER_Y, ir1, it1, it0)
        ctx.close_path()

    # Determine Style
    style_roll = random.random()
    
    # High-contrast Block (Swiss Kinetic energy)
    if style_roll > 0.85 - (dist * 0.2):
        ctx.set_source_rgb(1, 1, 1)
        construct_wedge_path(r0 + margin_r, r1 - margin_r, t0 + margin_t, t1 - margin_t)
        ctx.fill()
        
    # Precision Lines (Grid Logic)
    elif style_roll > 0.4:
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(0.4 if dist > 0.5 else 1.2)
        construct_wedge_path(r0 + margin_r, r1 - margin_r, t0 + margin_t, t1 - margin_t)
        ctx.stroke()
        
    # Shrapnel / Glitch (Entropy)
    elif style_roll > 0.1:
        ctx.set_source_rgb(0.8, 0.8, 0.8)
        ctx.set_line_width(0.2)
        # Draw radial bursts
        for _ in range(3):
            angle = random.uniform(t0, t1)
            ctx.move_to(*get_polar_coords(r0, angle))
            ctx.line_to(*get_polar_coords(r1 + (random.random() * 20), angle))
            ctx.stroke()

# --- Systematic Generation ---

# 1. Base Structure: Iterate through primary grid
for i in range(RINGS):
    # Non-linear radial spacing (Radial tension)
    r_start = MAX_RADIUS * math.pow(i / RINGS, 1.2)
    r_end = MAX_RADIUS * math.pow((i + 1) / RINGS, 1.2)
    
    # Modulated sector count (Frequency modulation)
    current_sectors = SECTORS if i < RINGS // 2 else SECTORS * 2
    
    for j in range(current_sectors):
        t_start = (j / current_sectors) * 2 * math.pi
        t_end = ((j + 1) / current_sectors) * 2 * math.pi
        
        # Apply slight angular distortion based on radius
        distortion = math.sin(i * 0.5) * 0.02
        draw_polar_cell(r_start, r_end, t_start + distortion, t_end + distortion)

# 2. Overlay: Technical Annotation / Floating Primitives
ctx.set_source_rgb(1, 1, 1)
for _ in range(12):
    # Precise tiny circles marking intersections (Swiss precision)
    rand_r = random.uniform(0, MAX_RADIUS)
    rand_t = random.uniform(0, math.pi * 2)
    px, py = get_polar_coords(rand_r, rand_t)
    
    ctx.set_line_width(0.5)
    ctx.arc(px, py, 2, 0, 2 * math.pi)
    ctx.stroke()
    
    # Horizontal/Vertical crosshairs
    ctx.move_to(px - 10, py)
    ctx.line_to(px + 10, py)
    ctx.move_to(px, py - 10)
    ctx.line_to(px, py + 10)
    ctx.stroke()

# 3. Vignette of entropy
# Randomized 'glitch' strokes cutting through the logic
ctx.set_line_width(0.3)
for i in range(5):
    ctx.set_source_rgba(1, 1, 1, 0.4)
    r_static = random.uniform(MAX_RADIUS * 0.3, MAX_RADIUS * 0.9)
    ctx.arc(CENTER_X, CENTER_Y, r_static, 0, 2 * math.pi)
    ctx.stroke()

# Final Polish: Central Void
ctx.set_source_rgb(0, 0, 0)
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS * 0.05, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS * 0.05, 0, 2 * math.pi)
ctx.stroke()

