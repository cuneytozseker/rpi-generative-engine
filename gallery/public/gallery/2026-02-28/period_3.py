import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Utility for polar conversion with distortion
def get_coords(r, theta, center_x, center_y, distortion_freq=5, distortion_amp=15):
    # Apply radial distortion based on angle and radius
    # This creates the "Analytical Formalism" ripple effect
    r_mod = r + math.sin(theta * distortion_freq + r * 0.02) * distortion_amp
    x = center_x + r_mod * math.cos(theta)
    y = center_y + r_mod * math.sin(theta)
    return x, y

cx, cy = width / 2, height / 2

# 1. PRIMARY GRID SYSTEM (Radial Swiss Grid)
num_rings = 10
num_sectors = 24
max_radius = 280

ctx.set_line_width(0.3)
for i in range(num_rings + 1):
    r = (i / num_rings) * max_radius
    # Set transparency based on hierarchy
    alpha = 0.6 if i % 5 == 0 else 0.2
    ctx.set_source_rgba(0.8, 0.9, 1.0, alpha)
    
    # Draw concentric circles with high-fidelity segments
    ctx.new_path()
    for s in range(num_sectors * 4 + 1):
        theta = (s / (num_sectors * 4)) * 2 * math.pi
        px, py = get_coords(r, theta, cx, cy)
        if s == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.stroke()

# 2. SECTOR SUBDIVISIONS & RECURSIVE BLOCKS
# Logic: Fill specific quadrants to create visual weight/rhythm
random.seed(42) # Deterministic for "Calculated Order"
for i in range(1, num_rings):
    r_inner = (i / num_rings) * max_radius
    r_outer = ((i + 1) / num_rings) * max_radius
    
    for s in range(num_sectors):
        theta_start = (s / num_sectors) * 2 * math.pi
        theta_end = ((s + 1) / num_sectors) * 2 * math.pi
        
        # Decide if this module is "active"
        chance = random.random()
        
        if chance > 0.85:
            # Functional Accent: Signal Blue/Cyan
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.4)
            steps = 10
            ctx.new_path()
            # Construct the distorted arc segment
            for step in range(steps + 1):
                t = theta_start + (theta_end - theta_start) * (step / steps)
                px, py = get_coords(r_inner, t, cx, cy)
                ctx.line_to(px, py)
            for step in range(steps, -1, -1):
                t = theta_start + (theta_end - theta_start) * (step / steps)
                px, py = get_coords(r_outer, t, cx, cy)
                ctx.line_to(px, py)
            ctx.close_path()
            ctx.fill()
            
        elif chance > 0.6:
            # Subtle Swiss Modular Fill
            ctx.set_source_rgba(1.0, 1.0, 1.0, 0.05)
            # Draw micro-hatching inside the cell
            num_hatch = 4
            for h in range(num_hatch):
                r_h = r_inner + (r_outer - r_inner) * (h / num_hatch)
                ctx.new_path()
                for step in range(10):
                    t = theta_start + (theta_end - theta_start) * (step / 9)
                    px, py = get_coords(r_h, t, cx, cy)
                    if step == 0: ctx.move_to(px, py)
                    else: ctx.line_to(px, py)
                ctx.stroke()

# 3. TECHNICAL MARKERS (The "Micro-Information")
ctx.set_line_width(0.5)
for s in range(num_sectors):
    theta = (s / num_sectors) * 2 * math.pi
    r_edge = max_radius + 15
    px, py = get_coords(max_radius, theta, cx, cy)
    ex, ey = get_coords(r_edge, theta, cx, cy)
    
    # Radial markers
    ctx.set_source_rgba(1, 1, 1, 0.8)
    ctx.move_to(px, py)
    ctx.line_to(ex, ey)
    ctx.stroke()
    
    # Small terminal data points
    if s % 2 == 0:
        ctx.set_source_rgb(1, 0.2, 0.4) # Accent: Tech Pink
        ctx.arc(ex, ey, 1.5, 0, 2 * math.pi)
        ctx.fill()
    
    # Swiss Cross Markers at specific intersections
    for i in [3, 7]:
        r = (i / num_rings) * max_radius
        mx, my = get_coords(r, theta, cx, cy)
        ctx.set_source_rgba(1, 1, 1, 0.5)
        size = 3
        ctx.move_to(mx - size, my); ctx.line_to(mx + size, my)
        ctx.move_to(mx, my - size); ctx.line_to(mx, my + size)
        ctx.stroke()

# 4. RADIAL DISTORTION OVERLAY
# A faint, global structure to tie the "Analytical Formalism" together
ctx.set_source_rgba(1, 1, 1, 0.03)
ctx.set_line_width(1.0)
for r_mult in [0.4, 0.7, 1.1]:
    r = r_mult * max_radius
    ctx.new_path()
    for s in range(200):
        theta = (s / 200) * 2 * math.pi
        # High frequency ripple
        px, py = get_coords(r, theta, cx, cy, distortion_freq=12, distortion_amp=8)
        if s == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.close_path()
    ctx.stroke()

# 5. DATA HUD ELEMENTS (Typography-style markers)
def draw_tick_cluster(x, y, color):
    ctx.set_source_rgba(*color)
    for i in range(4):
        ctx.rectangle(x + i*4, y, 2, 8)
        ctx.fill()

draw_tick_cluster(20, 20, (1, 1, 1, 0.6))
draw_tick_cluster(width - 40, height - 30, (1, 1, 1, 0.6))

# Final vignette effect to focus on the systematic center
pattern = cairo.RadialGradient(cx, cy, max_radius * 0.5, cx, cy, max_radius * 1.5)
pattern.add_color_stop_rgba(0, 0, 0, 0, 0)
pattern.add_color_stop_rgba(1, 0.02, 0.02, 0.05, 0.8)
ctx.set_source(pattern)
ctx.paint()

