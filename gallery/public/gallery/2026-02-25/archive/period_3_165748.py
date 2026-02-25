import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep "Swiss" Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration for the Structural Emergence
cx, cy = width / 2, height / 2
num_rings = 48
num_sectors = 120
max_radius = min(width, height) * 0.48

def transform_coords(r_idx, theta_idx, rings, sectors, time_offset=0):
    """
    Transforms grid indices into a distorted polar space.
    Implements non-linear radial scaling and harmonic perturbation.
    """
    # Normalized coordinates
    norm_r = r_idx / rings
    norm_theta = (theta_idx / sectors) * 2 * math.pi
    
    # Apply radial distortion: The "Swiss" grid follows a power-law distribution
    # Creating density closer to the center or edges based on exponent
    distorted_r = math.pow(norm_r, 1.2) * max_radius
    
    # Introduce harmonic oscillation based on sector position
    # This creates the "structural flux"
    perturbation = 15 * math.sin(norm_theta * 6 + norm_r * 4) * (1 - norm_r)
    distorted_r += perturbation
    
    # Add a slight spiral twist
    final_theta = norm_theta + (norm_r * 0.4)
    
    x = cx + distorted_r * math.cos(final_theta)
    y = cy + distorted_r * math.sin(final_theta)
    return x, y

# 1. DRAW UNDERLYING NODAL NETWORK (Optical Grays)
# Fine lines create a moiré effect and texture
ctx.set_line_width(0.15)
ctx.set_source_rgba(0.8, 0.8, 0.8, 0.3)

for r in range(0, num_rings, 2):
    for s in range(num_sectors):
        x1, y1 = transform_coords(r, s, num_rings, num_sectors)
        x2, y2 = transform_coords(r, (s + 1) % num_sectors, num_rings, num_sectors)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

# 2. DRAW RADIAL RIBS WITH MODULATED LINE WEIGHT
for s in range(0, num_sectors, 4):
    # Determine color based on "Accented Neutral" palette
    if s % 12 == 0:
        ctx.set_source_rgba(0.9, 0.3, 0.2, 0.8) # Vermillion Accent
    else:
        ctx.set_source_rgba(0.95, 0.95, 0.9, 0.5) # Warm Cream

    ctx.move_to(cx, cy)
    for r in range(num_rings + 1):
        x, y = transform_coords(r, s, num_rings, num_sectors)
        
        # Line weight modulation based on radius (brutalist density)
        weight = 0.2 + (r / num_rings) * 1.5
        ctx.set_line_width(weight)
        ctx.line_to(x, y)
    ctx.stroke()

# 3. GENERATE STRUCTURAL BLOCKS (Geometric Hierarchy)
# These represent the "Swiss Grid" elements projected into the distorted field
random.seed(42) # Deterministic randomness for systematic design
for _ in range(30):
    start_r = random.randint(10, num_rings - 10)
    start_s = random.randint(0, num_sectors - 1)
    r_len = random.randint(2, 6)
    s_len = random.randint(5, 15)
    
    # Choose a palette color
    choice = random.random()
    if choice > 0.85:
        ctx.set_source_rgba(0.1, 0.6, 0.8, 0.7) # Sky Blue Highlight
    elif choice > 0.7:
        ctx.set_source_rgba(0.9, 0.7, 0.2, 0.7) # Ochre Highlight
    else:
        ctx.set_source_rgba(0.95, 0.95, 0.9, 0.2) # Transparent Cream

    # Draw the distorted "rectangle" block
    ctx.new_path()
    # Inner Arc
    for s in range(start_s, start_s + s_len + 1):
        x, y = transform_coords(start_r, s % num_sectors, num_rings, num_sectors)
        if s == start_s: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    # Side 1
    for r in range(start_r, start_r + r_len + 1):
        x, y = transform_coords(r, (start_s + s_len) % num_sectors, num_rings, num_sectors)
        ctx.line_to(x, y)
    # Outer Arc
    for s in range(start_s + s_len, start_s - 1, -1):
        x, y = transform_coords(start_r + r_len, s % num_sectors, num_rings, num_sectors)
        ctx.line_to(x, y)
    # Side 2
    for r in range(start_r + r_len, start_r - 1, -1):
        x, y = transform_coords(r, start_s % num_sectors, num_rings, num_sectors)
        ctx.line_to(x, y)
    
    ctx.close_path()
    if random.random() > 0.5:
        ctx.fill()
    else:
        ctx.set_line_width(0.8)
        ctx.stroke()

# 4. DATA MARKERS (Nodal points)
# Small precision dots at specific intersections to emphasize the grid system
ctx.set_source_rgb(1.0, 1.0, 1.0)
for r in range(5, num_rings, 8):
    for s in range(0, num_sectors, 10):
        x, y = transform_coords(r, s, num_rings, num_sectors)
        ctx.arc(x, y, 1.5, 0, 2 * math.pi)
        ctx.fill()

# 5. VIGNETTE OVERLAY
# To add depth and focus to the central emergence
radial_grad = cairo.RadialGradient(cx, cy, max_radius * 0.5, cx, cy, max_radius * 1.2)
radial_grad.add_color_stop_rgba(0, 0, 0, 0, 0)
radial_grad.add_color_stop_rgba(1, 0.05, 0.05, 0.07, 0.8)
ctx.set_source(radial_grad)
ctx.paint()

# End of composition
