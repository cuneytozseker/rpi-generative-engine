import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)  # Deep near-black
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = min(width, height) * 0.45
NUM_RINGS = 12
NUM_SECTORS = 24

def get_polar_coords(r, theta, distortion_factor=0.15):
    """Applies a radial distortion to polar coordinates."""
    # Distort radius based on angle to create a 'pulsing' Swiss grid
    r_distorted = r * (1 + distortion_factor * math.sin(theta * 5 + r * 0.02))
    # Apply a subtle spiral twist
    theta_distorted = theta + (r / MAX_RADIUS) * 0.5
    
    x = CENTER_X + r_distorted * math.cos(theta_distorted)
    y = CENTER_Y + r_distorted * math.sin(theta_distorted)
    return x, y

def draw_subdivided_cell(r1, r2, a1, a2, depth):
    """Recursively partitions polar cells to create 'Recursive Entropy'."""
    # Entropy logic: Randomly decide to subdivide based on depth
    if depth < 4 and random.random() > 0.4 / (depth + 1):
        mid_r = (r1 + r2) / 2
        mid_a = (a1 + a2) / 2
        
        # Quadrants
        draw_subdivided_cell(r1, mid_r, a1, mid_a, depth + 1)
        draw_subdivided_cell(mid_r, r2, a1, mid_a, depth + 1)
        draw_subdivided_cell(r1, mid_r, mid_a, a2, depth + 1)
        draw_subdivided_cell(mid_r, r2, mid_a, a2, depth + 1)
    else:
        # Draw the primitive element for this cell
        draw_cell_element(r1, r2, a1, a2, depth)

def draw_cell_element(r1, r2, a1, a2, depth):
    """Renders the geometric content of a single subdivided cell."""
    choice = random.random()
    
    # Emissive color palette
    colors = [
        (0.9, 0.9, 0.9, 0.8), # White
        (1.0, 0.1, 0.2, 0.9), # Swiss Red
        (0.0, 0.8, 1.0, 0.7), # Cyan Emissive
    ]
    color = random.choice(colors)
    ctx.set_source_rgba(*color)
    
    if choice < 0.4:
        # Arc segment (The concentric grid lines)
        ctx.set_line_width(0.5 + (4 / (depth + 1)))
        steps = 10
        for i in range(steps + 1):
            t = i / steps
            curr_a = a1 + (a2 - a1) * t
            x, y = get_polar_coords(r1, curr_a)
            if i == 0: ctx.move_to(x, y)
            else: ctx.line_to(x, y)
        ctx.stroke()
        
    elif choice < 0.7:
        # Radial subdivision line
        ctx.set_line_width(0.3)
        x1, y1 = get_polar_coords(r1, a1)
        x2, y2 = get_polar_coords(r2, a1)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
    elif choice < 0.9:
        # Technical marker (Small square or dot)
        ctx.set_line_width(1.0)
        px, py = get_polar_coords((r1 + r2)/2, (a1 + a2)/2)
        size = 2 / (depth + 1)
        ctx.rectangle(px - size, py - size, size*2, size*2)
        if random.random() > 0.5: ctx.fill()
        else: ctx.stroke()

# --- Main Generation Logic ---

# 1. Background Grid Underlay
ctx.set_line_width(0.15)
ctx.set_source_rgba(1, 1, 1, 0.1)
for r in range(0, int(MAX_RADIUS * 1.5), 20):
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Polar Quadtree Partitioning
# We loop through a base grid and let recursion handle the entropy
for i in range(NUM_RINGS):
    r_start = (i / NUM_RINGS) * MAX_RADIUS
    r_end = ((i + 1) / NUM_RINGS) * MAX_RADIUS
    
    # Exponential expansion for radial depth
    r_start = math.pow(i / NUM_RINGS, 1.5) * MAX_RADIUS
    r_end = math.pow((i + 1) / NUM_RINGS, 1.5) * MAX_RADIUS

    for j in range(NUM_SECTORS):
        a_start = (j / NUM_SECTORS) * 2 * math.pi
        a_end = ((j + 1) / NUM_SECTORS) * 2 * math.pi
        
        # Increase complexity as we move outwards
        draw_subdivided_cell(r_start, r_end, a_start, a_end, depth=0)

# 3. Add Global "Swiss" Structural Accents
ctx.set_operator(cairo.OPERATOR_ADD) # Additive blending for light effect
ctx.set_source_rgba(0.1, 0.4, 1.0, 0.2)
ctx.set_line_width(2.0)

# Main axes lines
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    x1, y1 = get_polar_coords(0, angle)
    x2, y2 = get_polar_coords(MAX_RADIUS * 1.2, angle)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 4. Focal Ring (Golden Ratio point)
golden_r = MAX_RADIUS * 0.618
ctx.set_source_rgba(1.0, 1.0, 1.0, 0.4)
ctx.set_line_width(0.8)
ctx.arc(CENTER_X, CENTER_Y, golden_r, 0, 2 * math.pi)
ctx.stroke()

# 5. Fine Texture: Grain/Noise
random.seed(42)
ctx.set_operator(cairo.OPERATOR_OVER)
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0, 0.15))
    rx = random.uniform(0, width)
    ry = random.uniform(0, height)
    ctx.rectangle(rx, ry, 1, 1)
    ctx.fill()

# IMPORTANT: No surface.write_to_png()
