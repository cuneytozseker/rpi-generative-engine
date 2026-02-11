import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep monochromatic void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
grid_res = 32  # Number of divisions
max_radius = min(width, height) * 0.45

def project_polar(r, theta, distortion_factor=1.0):
    """
    Transforms grid coordinates into a distorted polar space.
    Uses a combination of radial expansion and angular oscillation.
    """
    # Mathematical entropy: radial shift based on angle and radius
    distortion = math.sin(theta * 5 + r * 0.01) * 15 * distortion_factor
    distorted_r = r + distortion
    
    # Polar to Cartesian transformation
    x = cx + distorted_r * math.cos(theta)
    y = cy + distorted_r * math.sin(theta)
    return x, y

def draw_annotation(x, y, size=4, color=(0.8, 0.8, 0.8, 0.6)):
    """Draws technical cross-hairs and 'data' markers."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(0.5)
    # Cross
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    # Tiny dot
    ctx.arc(x, y, 0.8, 0, 2 * math.pi)
    ctx.fill()

# --- Layer 1: Atmospheric Spectral Pulses (Glow) ---
# Simulating light diffusion through layered transparency
for pulse in range(3):
    ctx.set_line_width(2.5 - pulse * 0.5)
    r_mult = 0.8 + (pulse * 0.1)
    
    # Pulse Color: Pitting deep purple against orange
    if pulse % 2 == 0:
        ctx.set_source_rgba(0.4, 0.1, 0.8, 0.15) # Soft Purple
    else:
        ctx.set_source_rgba(1.0, 0.4, 0.0, 0.1) # Soft Orange

    for r_step in range(1, grid_res, 4):
        radius = (r_step / grid_res) * max_radius * r_mult
        ctx.new_path()
        for i in range(101):
            theta = (i / 100) * 2 * math.pi
            px, py = project_polar(radius, theta, distortion_factor=1.5)
            if i == 0: ctx.move_to(px, py)
            else: ctx.line_to(px, py)
        ctx.close_path()
        ctx.stroke()

# --- Layer 2: The Swiss Structural Grid ---
# Rigid precision transformed into polar geometry
ctx.set_line_width(0.7)

# Radial Lines (Spokes)
for i in range(grid_res):
    theta = (i / grid_res) * 2 * math.pi
    # Alternating colors for visual rhythm
    if i % 8 == 0:
        ctx.set_source_rgba(1.0, 0.5, 0.1, 0.8) # Vibrant Orange highlight
    else:
        ctx.set_source_rgba(0.7, 0.7, 0.8, 0.3) # Muted Neutral
    
    ctx.new_path()
    for r_step in range(grid_res + 1):
        radius = (r_step / grid_res) * max_radius
        px, py = project_polar(radius, theta)
        if r_step == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.stroke()

# Concentric Paths (Rings)
for r_step in range(1, grid_res + 1):
    radius = (r_step / grid_res) * max_radius
    
    # Every 4th ring is a primary subdivision (Swiss hierarchy)
    if r_step % 4 == 0:
        ctx.set_source_rgba(0.9, 0.9, 1.0, 0.6)
        ctx.set_line_width(1.0)
    else:
        ctx.set_source_rgba(0.5, 0.5, 0.6, 0.2)
        ctx.set_line_width(0.4)
        
    ctx.new_path()
    for i in range(101):
        theta = (i / 100) * 2 * math.pi
        px, py = project_polar(radius, theta)
        if i == 0: ctx.move_to(px, py)
        else: ctx.line_to(px, py)
    ctx.close_path()
    ctx.stroke()

# --- Layer 3: Annotations & Technical Data Points ---
# These represent "Digital Cartography" markers
for r_step in range(4, grid_res + 1, 4):
    for i in range(0, grid_res, 4):
        radius = (r_step / grid_res) * max_radius
        theta = (i / grid_res) * 2 * math.pi
        px, py = project_polar(radius, theta)
        
        # Draw annotation markers at intersections
        draw_annotation(px, py, size=3, color=(1.0, 1.0, 1.0, 0.7))
        
        # Occasional "Coordinate Blocks"
        if random.random() > 0.85:
            ctx.set_source_rgba(1.0, 0.4, 0.0, 0.9)
            ctx.rectangle(px + 5, py - 10, 12, 2) # Mock technical label
            ctx.fill()

# --- Layer 4: High-Density Entropy Focal Point ---
# A concentrated cluster of lines to break the uniformity
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.6, 0.2, 1.0, 0.4)
for _ in range(20):
    start_r = random.uniform(0, max_radius)
    start_theta = random.uniform(0, 2 * math.pi)
    ctx.new_path()
    curr_x, curr_y = project_polar(start_r, start_theta)
    ctx.move_to(curr_x, curr_y)
    
    for segment in range(15):
        start_r += random.uniform(-10, 15)
        start_theta += random.uniform(-0.1, 0.1)
        next_x, next_y = project_polar(start_r, start_theta)
        ctx.line_to(next_x, next_y)
    ctx.stroke()

# Border for Swiss-style framing
ctx.set_source_rgb(0.1, 0.1, 0.15)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Clean final highlight line
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(1)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

