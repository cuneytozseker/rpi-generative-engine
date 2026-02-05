import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Midnight/Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
cx, cy = width / 2, height / 2
max_radius = min(width, height) * 0.45
rings = 18
segments = 72

def get_distorted_polar(r_norm, theta_norm, noise_factor=0.15):
    """
    Maps normalized radius and angle to distorted screen coordinates.
    r_norm: 0 to 1
    theta_norm: 0 to 1
    """
    # Base polar transformation
    angle = theta_norm * 2 * math.pi
    
    # Introduce non-linear perturbations (Kinetic Cartography principle)
    # The distortion is higher at the edges, creating a "flow" effect
    distortion = math.sin(theta_norm * math.pi * 6 + r_norm * 4) * (r_norm * 25)
    distortion += math.cos(r_norm * math.pi * 3) * 15
    
    r = r_norm * max_radius + distortion
    
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    return x, y

# --- Layer 1: The Underlying "Technical" Web ---
ctx.set_line_width(0.3)
ctx.set_source_rgba(0.8, 0.8, 0.9, 0.2)

for i in range(rings):
    r_n = (i + 1) / rings
    ctx.new_path()
    for j in range(segments + 1):
        t_n = j / segments
        x, y = get_distorted_polar(r_n, t_n)
        if j == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

for j in range(0, segments, 4):
    t_n = j / segments
    ctx.new_path()
    for i in range(rings + 1):
        r_n = i / rings
        x, y = get_distorted_polar(r_n, t_n)
        if i == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

# --- Layer 2: Kinetic Flow Lines (Dashed paths with variable weight) ---
for k in range(40):
    # Randomly select a starting arc
    start_theta = random.random()
    length = random.uniform(0.1, 0.4)
    r_n = random.uniform(0.2, 0.9)
    
    ctx.set_line_width(random.uniform(0.5, 1.8))
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.4, 0.8))
    
    # Precise dashed patterns for "hand-plotted" technical feel
    dash_len = random.uniform(2, 10)
    ctx.set_dash([dash_len, dash_len * 0.5])
    
    ctx.new_path()
    steps = 40
    for s in range(steps + 1):
        t_n = start_theta + (s / steps) * length
        x, y = get_distorted_polar(r_n, t_n)
        if s == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

# --- Layer 3: Nested Grid Subdivision & Markers ---
ctx.set_dash([]) # Reset dash
for _ in range(12):
    r_n = random.uniform(0.3, 0.8)
    t_n = random.uniform(0, 1)
    x, y = get_distorted_polar(r_n, t_n)
    
    # Swiss-style cross markers
    size = 4
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.set_line_width(0.8)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# --- Layer 4: Primary Color Accents (Swiss Design Nodes) ---
# High-contrast primary colors at specific intersections
accents = [(0.9, 0.1, 0.1), (0.1, 0.4, 0.9), (0.9, 0.8, 0.1)] # Red, Blue, Yellow

for _ in range(15):
    r_n = random.choice([0.4, 0.6, 0.8])
    t_n = random.randint(0, segments) / segments
    x, y = get_distorted_polar(r_n, t_n)
    
    color = random.choice(accents)
    ctx.set_source_rgb(*color)
    
    # Draw small geometric data points
    shape_type = random.choice(['circle', 'rect', 'line'])
    if shape_type == 'circle':
        ctx.arc(x, y, 2.5, 0, 2 * math.pi)
        ctx.fill()
    elif shape_type == 'rect':
        ctx.rectangle(x-2, y-2, 4, 4)
        ctx.fill()
    else:
        # Segmented vector path
        ctx.set_line_width(2)
        x2, y2 = get_distorted_polar(r_n + 0.05, t_n + 0.02)
        ctx.move_to(x, y)
        ctx.line_to(x2, y2)
        ctx.stroke()

# --- Layer 5: Peripheral Gestural Flows ---
# Long, thin recursive lines following the vector field at the boundaries
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.2)
for i in range(100):
    t_n = i / 100
    r_start = 0.85
    ctx.new_path()
    for j in range(20):
        r_n = r_start + (j * 0.01)
        # Add slight wobble to the spiral
        curr_t = t_n + math.sin(j * 0.5) * 0.005
        x, y = get_distorted_polar(r_n, curr_t)
        if j == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

# --- Typography-Inspired Visual Elements ---
# Simulated data annotations using small geometric blocks
for i in range(5):
    angle = random.uniform(0, 2 * math.pi)
    r = max_radius * 1.1
    tx = cx + r * math.cos(angle)
    ty = cy + r * math.sin(angle)
    
    ctx.set_source_rgba(0.8, 0.8, 0.8, 0.5)
    # Vertical "serial number" bars
    for b in range(4):
        ctx.rectangle(tx + (b*3), ty, 1.5, random.uniform(5, 15))
        ctx.fill()

# Finish
