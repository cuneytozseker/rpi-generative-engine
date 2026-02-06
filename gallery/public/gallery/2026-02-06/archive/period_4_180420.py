import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# --- DETERMINISTIC NOISE GENERATOR ---
# A simple 2D Value Noise function to avoid external dependencies
RANDOM_GRID = [[random.random() for _ in range(30)] for _ in range(30)]

def get_noise(x, y):
    x = (x * 0.05) % 29
    y = (y * 0.05) % 29
    xi, yi = int(x), int(y)
    xf, yf = x - xi, y - yi
    
    # Smoothstep interpolation
    u = xf * xf * (3 - 2 * xf)
    v = yf * yf * (3 - 2 * yf)
    
    # Bilinear interpolation
    n00 = RANDOM_GRID[xi][yi]
    n01 = RANDOM_GRID[xi][yi+1]
    n10 = RANDOM_GRID[xi+1][yi]
    n11 = RANDOM_GRID[xi+1][yi+1]
    
    return n00*(1-u)*(1-v) + n10*u*(1-v) + n01*(1-u)*v + n11*u*v

# --- SYSTEMIC ELEMENTS ---

# 1. Background "Skeletal" Grid (Swiss Design Hierarchy)
ctx.set_line_width(0.5)
grid_size = 40
for i in range(0, width + 1, grid_size):
    for j in range(0, height + 1, grid_size):
        # Subtle high-frequency point density
        ctx.set_source_rgba(0.4, 0.5, 0.7, 0.2)
        ctx.arc(i, j, 0.8, 0, math.pi * 2)
        ctx.fill()
        
        # Hairline crosshairs
        if random.random() > 0.8:
            ctx.set_source_rgba(0.3, 0.4, 0.6, 0.1)
            ctx.move_to(i - 5, j)
            ctx.line_to(i + 5, j)
            ctx.move_to(i, j - 5)
            ctx.line_to(i, j + 5)
            ctx.stroke()

# 2. Atmospheric Flow Field
# This simulates "digital sublime" through overlapping particle trails
num_particles = 180
steps = 60
step_length = 8

def get_thermal_color(val):
    """Maps 0.0-1.0 to a spectral heat map: Deep Blue -> Cyan -> Hot White"""
    if val < 0.5:
        # Deep Blue to Cyan
        r = 0.0
        g = val * 1.5
        b = 0.4 + val
    else:
        # Cyan to White
        r = (val - 0.5) * 2
        g = 0.75 + (val - 0.5) * 0.5
        b = 1.0
    return (r, g, b)

# Create rhythmic progression by concentrating particles in specific "fractured" zones
for _ in range(num_particles):
    # Dynamic asymmetry: Bias starting points to create a directional flow
    px = random.uniform(-50, width * 0.7)
    py = random.uniform(-50, height + 50)
    
    # Recursive-like paths
    path_points = [(px, py)]
    
    # Calculate noise-based trajectory
    for s in range(steps):
        # Sample noise for angle and "atmospheric thickness"
        noise_val = get_noise(px * 0.1, py * 0.1)
        angle = noise_val * math.pi * 3.5 # Multi-rotation for complexity
        
        px += math.cos(angle) * step_length
        py += math.sin(angle) * step_length
        path_points.append((px, py))
    
    # Draw the trail with transparency layering
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    
    # Inner glowing core
    for i in range(1, len(path_points)):
        p1 = path_points[i-1]
        p2 = path_points[i]
        
        # Calculate local density based on noise
        local_noise = get_noise(p1[0] * 0.05, p1[1] * 0.05)
        r, g, b = get_thermal_color(local_noise)
        
        # Vary alpha and width to create "soft-edged gradients"
        alpha = (i / steps) * 0.3
        width_mod = (1.0 - (i / steps)) * 2.5
        
        ctx.set_source_rgba(r, g, b, alpha)
        ctx.set_line_width(width_mod)
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.stroke()

# 3. Geometric Logic Overlay (The Rigid System)
# A nested grid frame to anchor the organic movement
margin = 40
ctx.set_line_width(1.0)
ctx.set_source_rgba(1, 1, 1, 0.7)
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Labels and symbolic marks (Swiss minimalism)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(margin + 5, margin - 10)
ctx.show_text("SYS_REF: ATMOS_V.04")

ctx.set_font_size(6)
for i in range(4):
    y_pos = margin + (i * (height - margin*2) / 3)
    ctx.move_to(width - margin + 5, y_pos)
    ctx.show_text(f"+{1024 * (i+1)}ms")

# Add a "fractured" stochastic element: fine high-density points in flow clusters
for _ in range(800):
    rx = random.gauss(width/2, width/3)
    ry = random.gauss(height/2, height/3)
    nv = get_noise(rx * 0.1, ry * 0.1)
    if nv > 0.7: # Only in "hot" areas
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.5))
        ctx.arc(rx, ry, 0.5, 0, math.pi * 2)
        ctx.fill()

# Final atmospheric wash (vignette effect)
lg = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
lg.add_color_stop_rgba(0, 0, 0, 0, 0)
lg.add_color_stop_rgba(1, 0, 0, 0.05, 0.4)
ctx.set_source(lg)
ctx.paint()

