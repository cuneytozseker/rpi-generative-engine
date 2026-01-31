import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
max_radius = min(width, height) * 0.45
grid_rings = 18
grid_sectors = 48
accent_color = (1.0, 0.3, 0.1) # Swiss Safety Orange
neutral_light = (0.9, 0.9, 0.95)

def get_displaced_polar(r_norm, theta_norm):
    """
    Transforms normalized grid coordinates (0-1) into distorted polar screen coordinates.
    r_norm: distance from center (0 to 1)
    theta_norm: angle (0 to 1)
    """
    # Base angle and radius
    angle = theta_norm * 2 * math.pi
    radius = r_norm * max_radius
    
    # Apply field-driven distortion
    # A combination of harmonic sine waves to simulate a vector field displacement
    distortion = math.sin(theta_norm * 12 + r_norm * 5) * 15
    distortion += math.cos(r_norm * 10 - theta_norm * 8) * 10
    
    # Secondary "twist" based on radius
    angle += math.sin(r_norm * math.pi) * 0.4
    
    final_radius = radius + distortion
    px = cx + final_radius * math.cos(angle)
    py = cy + final_radius * math.sin(angle)
    
    return px, py

# 1. DRAW UNDERLYING RADIAL MESH
ctx.set_line_width(0.5)
for i in range(grid_rings + 1):
    r_n = i / grid_rings
    ctx.move_to(*get_displaced_polar(r_n, 0))
    for j in range(101):
        t_n = j / 100.0
        ctx.line_to(*get_displaced_polar(r_n, t_n))
    
    alpha = 0.1 + (r_n * 0.3)
    ctx.set_source_rgba(0.8, 0.8, 0.9, alpha)
    ctx.stroke()

# 2. DRAW SECTOR SPOKES WITH MODULATED DENSITY
for j in range(grid_sectors):
    t_n = j / grid_sectors
    
    # Variable line length for visual rhythm
    length_mod = 1.0 if j % 4 == 0 else 0.7
    if j % 12 == 0: length_mod = 1.2
    
    ctx.move_to(cx, cy)
    steps = 20
    for s in range(steps + 1):
        r_n = (s / steps) * length_mod
        ctx.line_to(*get_displaced_polar(r_n, t_n))
    
    if j % 12 == 0:
        ctx.set_source_rgba(*neutral_light, 0.6)
        ctx.set_line_width(0.8)
    else:
        ctx.set_source_rgba(0.5, 0.5, 0.6, 0.2)
        ctx.set_line_width(0.3)
    ctx.stroke()

# 3. RECURSIVE SUBDIVISIONS / ACCENT BURSTS
# Highlight specific "data paths" in the topography
random.seed(42)
for _ in range(8):
    start_r = random.uniform(0.2, 0.6)
    target_theta = random.uniform(0, 1)
    path_len = random.randint(5, 15)
    
    ctx.set_source_rgba(*accent_color, 0.8)
    ctx.set_line_width(1.5)
    
    px, py = get_displaced_polar(start_r, target_theta)
    ctx.move_to(px, py)
    
    for k in range(path_len):
        step_r = start_r + (k * 0.03)
        step_t = target_theta + (math.sin(k * 0.5) * 0.01)
        ctx.line_to(*get_displaced_polar(step_r, step_t))
    ctx.stroke()

# 4. SYSTEMATIC GEOMETRIC MARKS (CROSSES AND DOTS)
# Placed at grid intersections to emphasize the Cartesian-to-Polar mapping
for i in range(1, grid_rings, 2):
    for j in range(0, grid_sectors, 3):
        r_n = i / grid_rings
        t_n = j / grid_sectors
        px, py = get_displaced_polar(r_n, t_n)
        
        # Draw small technical markers
        size = 2
        if (i + j) % 7 == 0:
            # Saturated Accent Dots
            ctx.set_source_rgb(*accent_color)
            ctx.arc(px, py, 1.5, 0, 2 * math.pi)
            ctx.fill()
        else:
            # Precision Crosses
            ctx.set_source_rgba(1, 1, 1, 0.4)
            ctx.set_line_width(0.5)
            ctx.move_to(px - size, py)
            ctx.line_to(px + size, py)
            ctx.move_to(px, py - size)
            ctx.line_to(px, py + size)
            ctx.stroke()

# 5. ATMOSPHERIC DEPTH (Vignette & Gradient Overlay)
# Create a radial gradient to focus attention on the center
rad_grad = cairo.RadialGradient(cx, cy, 50, cx, cy, max_radius * 1.5)
rad_grad.add_color_stop_rgba(0, 0, 0, 0, 0)
rad_grad.add_color_stop_rgba(0.8, 0.05, 0.05, 0.07, 0.4)
rad_grad.add_color_stop_rgba(1, 0.05, 0.05, 0.07, 1)
ctx.set_source(rad_grad)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# 6. TEXT AS ARCHITECTURAL ELEMENT
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgba(*neutral_light, 0.8)
ctx.move_to(20, height - 20)
ctx.show_text("SYNTHETIC TOPOGRAPHY // REF. POLAR_TRANS_04")

# Draw a small scale bar
ctx.set_line_width(1)
ctx.move_to(width - 120, height - 25)
ctx.line_to(width - 20, height - 25)
ctx.stroke()
for b in range(5):
    ctx.move_to(width - 120 + (b * 25), height - 25)
    ctx.line_to(width - 120 + (b * 25), height - 30)
    ctx.stroke()
