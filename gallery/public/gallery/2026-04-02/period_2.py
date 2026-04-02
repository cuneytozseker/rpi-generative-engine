import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Swiss Charcoal
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_noise(x, y, scale=0.01):
    """Pseudo-perlin effect using harmonic sine waves for deterministic fluidity."""
    v1 = math.sin(x * scale + y * scale)
    v2 = math.cos(x * scale * 0.5 - y * scale * 1.2)
    v3 = math.sin(math.sqrt(x*x + y*y) * scale * 2.0)
    return (v1 + v2 + v3) / 3.0

def polar_warp(x, y, cx, cy, strength=40.0):
    """Transforms Cartesian grid points into a radially distorted polar space."""
    dx = x - cx
    dy = y - cy
    r = math.sqrt(dx*dx + dy*dy)
    theta = math.atan2(dy, dx)
    
    # Apply harmonic distortion to radius and angle
    noise_val = get_noise(x, y, 0.008)
    r_distorted = r + noise_val * strength
    theta_distorted = theta + (noise_val * 0.5)
    
    # Project back to Cartesian for drawing
    nx = cx + r_distorted * math.cos(theta_distorted)
    ny = cy + r_distorted * math.sin(theta_distorted)
    return nx, ny, abs(noise_val)

# Global Parameters
cx, cy = width / 2, height / 2
grid_res_x = 80
grid_res_y = 60
step_x = width / grid_res_x
step_y = height / grid_res_y

# Layer 1: The Underlying "Digital Noise" (Dithered Field)
ctx.set_line_width(0.5)
for i in range(0, width, 6):
    for j in range(0, height, 6):
        if random.random() > 0.7:
            nx, ny, energy = polar_warp(i, j, cx, cy, strength=60.0)
            alpha = 0.1 + (energy * 0.4)
            ctx.set_source_rgba(0.8, 0.9, 1.0, alpha)
            ctx.arc(nx, ny, 0.8, 0, 2 * math.pi)
            ctx.fill()

# Layer 2: The Structural Polar Grid (Modular Subdivision)
for i in range(grid_res_x):
    for j in range(grid_res_y):
        x = i * step_x
        y = j * step_y
        
        nx, ny, energy = polar_warp(x, y, cx, cy, strength=80.0)
        
        # Swiss Design: Logic-based sizing
        # Energy determines the transformation of the 'cell'
        size = 1.5 + (energy * 4.0)
        
        # Color Interaction: Thermal Energy Mapping
        # Stable regions (low energy) are white/grey. High energy = vibrant spectrum.
        if energy > 0.6:
            # High Energy: Vivid Magenta/Cyan
            ctx.set_source_rgba(1.0, 0.1, 0.4, 0.8)
        elif energy > 0.4:
            ctx.set_source_rgba(0.0, 0.8, 0.9, 0.7)
        else:
            # Stable: High Contrast White
            ctx.set_source_rgba(0.95, 0.95, 0.95, 0.5)
            
        # Draw grid primitives (tiny Swiss blocks/ticks)
        ctx.save()
        ctx.translate(nx, ny)
        ctx.rotate(math.atan2(ny - cy, nx - cx) + energy)
        
        # Systemic repetition with variation
        if (i + j) % 2 == 0:
            ctx.rectangle(-size/2, -size/2, size, size * 0.2)
        else:
            ctx.rectangle(-size/4, -size, size/2, size*2)
            
        ctx.fill()
        ctx.restore()

# Layer 3: Flow Artifacts (Connecting the Logic)
ctx.set_line_width(0.3)
for i in range(0, grid_res_x, 4):
    ctx.move_to(*polar_warp(i * step_x, 0, cx, cy)[:2])
    for j in range(grid_res_y):
        tx, ty, e = polar_warp(i * step_x, j * step_y, cx, cy, strength=80.0)
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.line_to(tx, ty)
    ctx.stroke()

# Layer 4: Hierarchy - Bold Structural Accents
ctx.set_line_width(2.0)
for r_ring in [100, 180, 260]:
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.arc(cx, cy, r_ring, 0, 2*math.pi)
    ctx.stroke()
    
    # Adding 'ticks' like a precision instrument
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        sx = cx + r_ring * math.cos(rad)
        sy = cy + r_ring * math.sin(rad)
        nx, ny, e = polar_warp(sx, sy, cx, cy, strength=100.0)
        
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.arc(nx, ny, 1.5, 0, 2*math.pi)
        ctx.fill()

# Final Polish: Global grain/texture
for _ in range(1000):
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.rectangle(random.uniform(0, width), random.uniform(0, height), 0.5, 0.5)
    ctx.fill()

