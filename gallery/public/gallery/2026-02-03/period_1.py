import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Swiss Black
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = min(width, height) * 0.45
NUM_RINGS = 8
MIN_SUBDIVISION_DEPTH = 2
MAX_SUBDIVISION_DEPTH = 5

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to Cartesian space relative to center."""
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

def draw_swiss_primitive(ctx, r_start, r_end, a_start, a_end, depth):
    """Draws a geometric glyph within a polar cell based on structural entropy."""
    
    # Calculate cell properties
    mid_r = (r_start + r_end) / 2
    mid_a = (a_start + a_end) / 2
    
    # Entropy factor: increases with distance from center and depth
    entropy = (mid_r / MAX_RADIUS) * (depth / MAX_SUBDIVISION_DEPTH)
    
    # Determine visual density (High depth = finer lines)
    ctx.set_line_width(0.5 + (MAX_SUBDIVISION_DEPTH - depth) * 0.8)
    ctx.set_source_rgb(0.95, 0.95, 0.95) # High contrast white

    # Decision logic based on entropy "noise"
    noise_val = random.random() + (entropy * 0.5)
    
    if noise_val < 0.4:
        # Systematic: Arc Segment
        ctx.arc(CENTER_X, CENTER_Y, mid_r, a_start, a_end)
        ctx.stroke()
    elif noise_val < 0.7:
        # Structural: Radial Spoke
        x1, y1 = polar_to_cartesian(r_start, mid_a)
        x2, y2 = polar_to_cartesian(r_end, mid_a)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
    elif noise_val < 0.9:
        # Fragmented: Dot grid / Vector Grain
        dot_r = 1.5 if entropy < 0.5 else 0.8
        for i in range(3):
            p_r = r_start + (r_end - r_start) * (i / 2)
            px, py = polar_to_cartesian(p_r, mid_a)
            ctx.arc(px, py, dot_r, 0, 2 * math.pi)
            ctx.fill()
    else:
        # Entropy: Deconstructed Cross
        # This creates the 'brutalist' feel of collapsing structures
        offset = (r_end - r_start) * 0.2
        x, y = polar_to_cartesian(mid_r, mid_a)
        ctx.move_to(x - offset, y)
        ctx.line_to(x + offset, y)
        ctx.move_to(x, y - offset)
        ctx.line_to(x, y + offset)
        ctx.stroke()

def subdivide_polar(r_start, r_end, a_start, a_end, depth):
    """Recursively divides space into a polar quadtree-like structure."""
    
    # Probability of subdivision increases with distance (radial distortion)
    # and decreases with depth to manage complexity.
    split_prob = 0.85 - (depth * 0.15) + (r_start / MAX_RADIUS) * 0.2
    
    if depth < MAX_SUBDIVISION_DEPTH and (depth < MIN_SUBDIVISION_DEPTH or random.random() < split_prob):
        # Decide whether to split Radially, Angularly, or Both
        split_r = random.choice([True, False])
        split_a = random.choice([True, False])
        if not split_r and not split_a: split_a = True # Ensure at least one split
        
        mid_r = (r_start + r_end) / 2
        mid_a = (a_start + a_end) / 2
        
        r_bounds = [(r_start, mid_r), (mid_r, r_end)] if split_r else [(r_start, r_end)]
        a_bounds = [(a_start, mid_a), (mid_a, a_end)] if split_a else [(a_start, a_end)]
        
        for rb in r_bounds:
            for ab in a_bounds:
                subdivide_polar(rb[0], rb[1], ab[0], ab[1], depth + 1)
    else:
        # Base case: draw the element
        draw_swiss_primitive(ctx, r_start, r_end, a_start, a_end, depth)

# --- Execution ---

# 1. Background Grid Layer (Subtle)
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(0.2)
for i in range(1, 12):
    r = (MAX_RADIUS / 10) * i
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Main Recursive Transformation
# Divide the circle into 4 primary quadrants to start the hierarchy
num_sectors = 4
angle_step = (2 * math.pi) / num_sectors

for i in range(num_sectors):
    start_angle = i * angle_step
    end_angle = (i + 1) * angle_step
    subdivide_polar(20, MAX_RADIUS, start_angle, end_angle, 0)

# 3. Structural Overlays: Centrifugal Tension
# Adding heavy "Swiss" bars at cardinal directions to anchor the entropy
ctx.set_source_rgb(0.9, 0.1, 0.1) # A single spot color: Swiss Red
ctx.set_line_width(4)
for i in range(4):
    angle = i * (math.pi / 2)
    # Draw a bold line cutting through the noise
    x1, y1 = polar_to_cartesian(MAX_RADIUS * 0.8, angle)
    x2, y2 = polar_to_cartesian(MAX_RADIUS * 1.1, angle)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 4. Global Grain Texture
# Finely scattered points to simulate paper or print texture
for _ in range(2000):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.15))
    ctx.rectangle(tx, ty, 1, 1)
    ctx.fill()

# Finish
