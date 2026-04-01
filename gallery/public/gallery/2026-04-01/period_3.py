import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Colors: Accented neutrals (Swiss-inspired palette)
color_bg = (0.95, 0.94, 0.90)  # Muted Cream
color_dark = (0.1, 0.1, 0.15)  # Deep Charcoal
color_accent1 = (0.1, 0.3, 0.5) # Sophisticated Teal-Blue
color_accent2 = (0.74, 0.29, 0.17) # Earthy Red

# Background
ctx.set_source_rgb(*color_bg)
ctx.paint()

def polar_to_cartesian(cx, cy, r, angle):
    return cx + r * math.cos(angle), cy + r * math.sin(angle)

def draw_polar_grid_cell(cx, cy, r1, r2, a1, a2, weight, color, alpha=1.0):
    """Draws a segment of a polar grid with varied line weights."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(weight)
    
    # Outer arc
    ctx.arc(cx, cy, r2, a1, a2)
    ctx.stroke()
    
    # Radial boundary
    p1 = polar_to_cartesian(cx, cy, r1, a1)
    p2 = polar_to_cartesian(cx, cy, r2, a1)
    ctx.move_to(p1[0], p1[1])
    ctx.line_to(p2[0], p2[1])
    ctx.stroke()

# Configuration for the "Emergent Structuralism"
cx, cy = width / 2, height / 2
rings = 40
slices = 60
max_radius = min(width, height) * 0.8
random.seed(42) # For consistent "precise chaos"

# 1. THE RADIAL FLOW FIELD (Underlying Structure)
for i in range(rings):
    r_norm = i / rings
    r_inner = r_norm * max_radius
    r_outer = (i + 1) / rings * max_radius
    
    for j in range(slices):
        theta_norm = j / slices
        a_start = theta_norm * 2 * math.pi
        a_end = (j + 1) / slices * 2 * math.pi
        
        # Apply radial distortion logic
        # Distortion is based on a harmonic of the angle and radius
        distortion = math.sin(theta_norm * math.pi * 4 + r_norm * 5) * 0.5 + 0.5
        
        # Thresholding to create "Dynamic Asymmetry"
        # Only draw if it meets a certain density probability
        if random.random() > (0.3 + 0.5 * r_norm):
            # Line weight modulation as a proxy for depth
            weight = 0.2 + (1.5 * distortion)
            
            # Select color based on "Topographic" clusters
            if distortion > 0.8:
                col = color_accent1
            elif distortion < 0.2 and random.random() > 0.8:
                col = color_accent2
            else:
                col = color_dark
                
            # Randomly subdivide or create "micro-patterns"
            if random.random() > 0.92:
                # Dense Dithering: Draw tiny dots instead of lines
                for _ in range(5):
                    dr = random.uniform(r_inner, r_outer)
                    da = random.uniform(a_start, a_end)
                    px, py = polar_to_cartesian(cx, cy, dr, da)
                    ctx.arc(px, py, weight * 0.8, 0, 2 * math.pi)
                    ctx.fill()
            else:
                draw_polar_grid_cell(cx, cy, r_inner, r_outer, a_start, a_end, weight, col, alpha=0.8)

# 2. OVERLAYING THE RIGID SWISS GRID
# A subtle rectangular grid to provide tension against the polar distortion
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.1, 0.1, 0.1, 0.2)
grid_spacing = 40
for x in range(0, width, grid_spacing):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_spacing):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 3. ANCHORING ELEMENTS (Typography/Brutalist Blocks)
# Representing "Information Hierarchy"
def draw_data_block(x, y, w, h, label):
    ctx.set_source_rgb(*color_dark)
    ctx.rectangle(x, y, w, h)
    ctx.fill()
    
    # Simple line-based "text" abstraction
    ctx.set_source_rgb(*color_bg)
    line_y = y + 5
    while line_y < y + h - 5:
        ctx.set_line_width(1)
        ctx.move_to(x + 5, line_y)
        ctx.line_to(x + w - random.uniform(5, w/2), line_y)
        ctx.stroke()
        line_y += 4

# Place blocks in corners to define the frame
draw_data_block(20, 20, 80, 40, "SYS_01")
draw_data_block(width - 100, height - 60, 80, 40, "REF_POLAR")

# 4. FINAL PROGRESSIVE DISTORTION (Vector Paths)
# Long sweeping arcs that cut through the composition
ctx.set_line_width(0.5)
ctx.set_source_rgba(*color_accent1, 0.4)
for i in range(5):
    start_angle = random.uniform(0, 2 * math.pi)
    path_radius = random.uniform(100, max_radius)
    ctx.arc(cx, cy, path_radius, start_angle, start_angle + math.pi/2)
    ctx.stroke()

# 5. CENTER NUCLEUS (The "Origin" of the system)
ctx.set_source_rgb(*color_dark)
ctx.arc(cx, cy, 3, 0, 2 * math.pi)
ctx.fill()
ctx.set_line_width(0.5)
ctx.arc(cx, cy, 10, 0, 2 * math.pi)
ctx.stroke()

