import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Parameters
cx, cy = width / 2, height / 2
rings = 18
segments = 42
max_radius = 320

def get_polar_coords(r_idx, a_idx, total_r, total_a, ripple=0):
    """Calculates distorted polar coordinates for the Swiss grid."""
    angle = (a_idx / total_a) * 2 * math.pi
    # Normalizing radius with a power function for exponential spacing (Swiss hierarchy)
    base_r = (r_idx / total_r)**1.2 * max_radius
    
    # Radial distortion: apply a harmonic sine wave to the radius based on angle
    # This creates the 'chromatic diffusion' flow effect
    distortion = math.sin(angle * 6 + (r_idx * 0.5)) * (r_idx * 1.8)
    r = base_r + distortion + ripple
    
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    return x, y, angle

# 1. LAYER ONE: Chromatic Diffusion (Blurred Blooms)
# Simulating softness through low-alpha concentric expansions
for i in range(5):
    ctx.set_source_rgba(0.9, 0.1, 0.4, 0.03) # Spectral Magenta
    ctx.arc(cx, cy, 50 + i * 40, 0, 2 * math.pi)
    ctx.fill()
    
    ctx.set_source_rgba(0.1, 0.6, 0.9, 0.02) # Cyan bloom
    ctx.arc(cx - 100, cy + 50, 80 + i * 30, 0, 2 * math.pi)
    ctx.fill()

# 2. LAYER TWO: The Polar Grid (Systematic Precision)
ctx.set_line_width(0.5)
for r in range(1, rings):
    # Determine color based on radial distance (Heatmap logic)
    gradient_val = r / rings
    ctx.set_source_rgba(0.4 + gradient_val * 0.6, 0.8 - gradient_val * 0.5, 1.0 - gradient_val, 0.4)
    
    ctx.new_path()
    for a in range(segments + 1):
        x, y, _ = get_polar_coords(r, a, rings, segments)
        if a == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# 3. LAYER THREE: Stochastic Modularity (The 'Bits')
# We iterate through the grid and place discrete modular elements
for r in range(1, rings):
    for a in range(segments):
        x, y, angle = get_polar_coords(r, a, rings, segments)
        
        # Stochastic filter: only draw on certain "bits"
        seed = random.random()
        
        # Scaling elements based on radius (Radial perspective)
        size = (r / rings) * 6
        
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(angle)
        
        if seed > 0.85:
            # Swiss Cross Module
            ctx.set_source_rgb(1, 1, 1)
            ctx.set_line_width(1.5)
            thickness = size * 0.3
            ctx.rectangle(-size, -thickness/2, size*2, thickness)
            ctx.rectangle(-thickness/2, -size, thickness, size*2)
            ctx.fill()
        elif seed > 0.65:
            # Technical Slashes (Frequency-based texture)
            ctx.set_source_rgb(0.1, 0.9, 0.7)
            ctx.set_line_width(1.0)
            ctx.move_to(-size, size)
            ctx.line_to(size, -size)
            ctx.stroke()
        elif seed > 0.4:
            # Data Points (Dithering)
            ctx.set_source_rgba(1, 1, 1, 0.8)
            dot_size = (math.sin(r * 0.5) + 1.1) * 1.5
            ctx.arc(0, 0, dot_size, 0, 2 * math.pi)
            ctx.fill()
            
        ctx.restore()

# 4. LAYER FOUR: Recursive Scaling Lines
# Long radial lines that break the grid, creating directional progression
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.15)
for a in range(0, segments, 4):
    x_start, y_start, _ = get_polar_coords(2, a, rings, segments)
    x_end, y_end, _ = get_polar_coords(rings + 2, a, rings, segments, ripple=40)
    ctx.move_to(x_start, y_start)
    ctx.line_to(x_end, y_end)
    ctx.stroke()

# 5. FINAL TOUCH: High-contrast border markers (Brutalist aesthetic)
ctx.set_source_rgb(1, 1, 1)
marker_size = 15
# Top Left
ctx.move_to(20, 20)
ctx.line_to(20 + marker_size, 20)
ctx.move_to(20, 20)
ctx.line_to(20, 20 + marker_size)
# Bottom Right
ctx.move_to(width - 20, height - 20)
ctx.line_to(width - 20 - marker_size, height - 20)
ctx.move_to(width - 20, height - 20)
ctx.line_to(width - 20, height - 20 - marker_size)
ctx.set_line_width(2)
ctx.stroke()

# Center alignment mark
ctx.set_line_width(1)
ctx.arc(cx, cy, 3, 0, 2*math.pi)
ctx.stroke()
