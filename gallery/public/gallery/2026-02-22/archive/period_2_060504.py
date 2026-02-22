import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
RINGS = 45
SLICES = 72
MAX_RADIUS = math.sqrt(CENTER_X**2 + CENTER_Y**2)
ACCENT_COLOR = (1.0, 0.2, 0.1) # Swiss Red

def get_polar_coord(r_idx, theta_idx, r_total, theta_total):
    """Calculates a distorted polar coordinate mapped to Cartesian space."""
    # Logarithmic radial distribution for 'implied gravity' towards center
    norm_r = r_idx / r_total
    r = MAX_RADIUS * (math.pow(norm_r, 1.6)) 
    
    # Angular distortion: slices bunch up or spread based on radial distance
    angle_offset = math.sin(norm_r * math.pi * 2) * 0.2
    theta = (theta_idx / theta_total) * 2 * math.pi + angle_offset
    
    # Cartesian transformation
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

# Draw the underlying systematic grid
ctx.set_line_width(0.4)
for r in range(1, RINGS):
    # Determine visual weight based on hierarchy
    alpha = 0.1 + (0.4 * (1.0 - r/RINGS))
    ctx.set_source_rgba(0.9, 0.9, 0.9, alpha)
    
    for t in range(SLICES):
        p1 = get_polar_coord(r, t, RINGS, SLICES)
        p2 = get_polar_coord(r, (t + 1) % SLICES, RINGS, SLICES)
        p3 = get_polar_coord(r + 1, t, RINGS, SLICES)
        
        # Draw Circumferential lines
        ctx.move_to(*p1)
        ctx.line_to(*p2)
        ctx.stroke()
        
        # Draw Radial lines (logical threads)
        if r < RINGS - 1:
            ctx.move_to(*p1)
            ctx.line_to(*p3)
            ctx.stroke()

# Secondary Layer: Structural Connectors and Chromatic Events
# This layer emphasizes connectivity rules and focal points
random.seed(42) # Deterministic randomness for systematic feel
for _ in range(180):
    r_rand = random.randint(5, RINGS - 5)
    t_rand = random.randint(0, SLICES - 1)
    
    p_start = get_polar_coord(r_rand, t_rand, RINGS, SLICES)
    
    # Logic: Connect nodes that share a 'harmonic' relationship
    step = random.choice([3, 5, 8]) # Fibonacci-inspired steps
    p_end = get_polar_coord(r_rand, (t_rand + step) % SLICES, RINGS, SLICES)
    
    # Draw logic thread
    ctx.set_source_rgba(0.8, 0.8, 1.0, 0.3)
    ctx.set_line_width(0.2)
    ctx.move_to(*p_start)
    ctx.line_to(*p_end)
    ctx.stroke()
    
    # Chromatic Event: Occurs at specific logical intersections
    if r_rand % 7 == 0 and t_rand % 4 == 0:
        ctx.set_source_rgb(*ACCENT_COLOR)
        ctx.arc(p_start[0], p_start[1], 1.5, 0, 2 * math.pi)
        ctx.fill()
        
        # Visual anchor: Crosshair motif
        ctx.set_line_width(0.5)
        ctx.move_to(p_start[0] - 5, p_start[1])
        ctx.line_to(p_start[0] + 5, p_start[1])
        ctx.move_to(p_start[0], p_start[1] - 5)
        ctx.line_to(p_start[0], p_start[1] + 5)
        ctx.stroke()

# Tertiary Layer: Density Accumulation (Texture)
# Recursive arcs to create "perceived weight" in high-activity hubs
for i in range(10):
    hub_r = random.randint(10, 30)
    hub_t = random.randint(0, SLICES)
    cx, cy = get_polar_coord(hub_r, hub_t, RINGS, SLICES)
    
    for layer in range(5):
        radius = layer * 3
        ctx.set_source_rgba(1, 1, 1, 0.05)
        ctx.set_line_width(0.3)
        ctx.arc(cx, cy, radius, 0, math.pi * 2)
        ctx.stroke()

# Final Polish: Edge Mask/Vignette to focus on the systematic core
lg = cairo.RadialGradient(CENTER_X, CENTER_Y, 50, CENTER_X, CENTER_Y, MAX_RADIUS)
lg.add_color_stop_rgba(0, 1, 1, 1, 0)
lg.add_color_stop_rgba(0.8, 0, 0, 0, 0)
lg.add_color_stop_rgba(1, 0, 0, 0, 0.7)
ctx.set_source(lg)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# Top Layer: Minimalist Data Markers
ctx.set_source_rgb(0.7, 0.7, 0.7)
ctx.set_line_width(1.0)
margin = 20
ctx.move_to(margin, margin)
ctx.line_to(margin + 40, margin)
ctx.stroke()
# (The layout uses negative space and precise line work to evoke a technical drafting)
