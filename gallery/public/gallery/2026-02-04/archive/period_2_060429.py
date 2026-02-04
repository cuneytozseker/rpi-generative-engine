import cairo
import math
import random

# Setup
width, height = 600, 600  # Square format suits polar better
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Bauhaus Black
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
MIN_RADIUS = 20
SUBDIVISION_STEPS = 5
ACCENT_COLOR = (1, 0.1, 0.1) # Swiss Red

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to screen space."""
    x = CENTER_X + r * math.cos(theta)
    y = CENTER_Y + r * math.sin(theta)
    return x, y

def draw_polar_arc(r1, r2, theta1, theta2, fill=False):
    """Draws a 'rectangle' segment in polar space."""
    ctx.arc(CENTER_X, CENTER_Y, r1, theta1, theta2)
    ctx.line_to(*polar_to_cartesian(r2, theta2))
    ctx.arc_negative(CENTER_X, CENTER_Y, r2, theta2, theta1)
    ctx.close_path()
    if fill:
        ctx.fill()
    else:
        ctx.stroke()

def draw_module(r1, r2, theta1, theta2, depth):
    """Draws a specific Swiss-inspired graphic based on location and randomness."""
    mid_r = (r1 + r2) / 2
    mid_theta = (theta1 + theta2) / 2
    
    # Selection logic based on 'centripetal density' and depth
    dist_factor = 1.0 - (mid_r / MAX_RADIUS) # 1.0 at center, 0 at edge
    rand = random.random()
    
    ctx.set_line_width(0.5 + (depth * 0.2))
    ctx.set_source_rgba(0.9, 0.9, 0.9, 0.8)

    # Primitive A: Radial Hatching (Topographic feel)
    if rand < 0.3:
        steps = int(5 + dist_factor * 10)
        for i in range(steps):
            t = theta1 + (theta2 - theta1) * (i / steps)
            p1 = polar_to_cartesian(r1, t)
            p2 = polar_to_cartesian(r2, t)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
        ctx.stroke()

    # Primitive B: Concentric Arcs
    elif rand < 0.5:
        steps = int(3 + dist_factor * 8)
        for i in range(steps):
            r = r1 + (r2 - r1) * (i / steps)
            ctx.arc(CENTER_X, CENTER_Y, r, theta1, theta2)
            ctx.stroke()

    # Primitive C: Solid Blocks (Brutalist hierarchy)
    elif rand < 0.7:
        if dist_factor > 0.4:
            ctx.set_source_rgba(0.95, 0.95, 0.95, 1.0)
            draw_polar_arc(r1 + 2, r2 - 2, theta1 + 0.02, theta2 - 0.02, fill=True)
        else:
            ctx.set_line_width(2)
            draw_polar_arc(r1 + 4, r2 - 4, theta1 + 0.05, theta2 - 0.05, fill=False)

    # Primitive D: Data Points/Nodes
    elif rand < 0.9:
        num_points = int(2 + dist_factor * 5)
        for _ in range(num_points):
            pr = random.uniform(r1, r2)
            pt = random.uniform(theta1, theta2)
            px, py = polar_to_cartesian(pr, pt)
            ctx.arc(px, py, 1.2, 0, math.pi * 2)
            ctx.fill()

    # Rare Accent: The Swiss Red Line
    if random.random() < 0.02:
        ctx.set_source_rgb(*ACCENT_COLOR)
        ctx.set_line_width(3)
        ctx.arc(CENTER_X, CENTER_Y, mid_r, theta1, theta2)
        ctx.stroke()

def recursive_subdivide(r1, r2, theta1, theta2, depth):
    """Quadtree-like subdivision in polar coordinates."""
    # Probability of subdivision increases toward the center
    mid_r = (r1 + r2) / 2
    dist_factor = 1.0 - (mid_r / MAX_RADIUS)
    
    subdivide_prob = 0.7 * dist_factor + 0.2
    
    if depth < SUBDIVISION_STEPS and random.random() < subdivide_prob:
        mid_theta = (theta1 + theta2) / 2
        # Split into 4 quadrants
        recursive_subdivide(r1, mid_r, theta1, mid_theta, depth + 1)
        recursive_subdivide(mid_r, r2, theta1, mid_theta, depth + 1)
        recursive_subdivide(r1, mid_r, mid_theta, theta2, depth + 1)
        recursive_subdivide(mid_r, r2, mid_theta, theta2, depth + 1)
    else:
        draw_module(r1, r2, theta1, theta2, depth)

# --- Execution ---

# 1. Background Grid (Subtle)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
for r in range(0, int(MAX_RADIUS), 40):
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.stroke()
for i in range(12):
    angle = i * (math.pi / 6)
    ctx.move_to(CENTER_X, CENTER_Y)
    ctx.line_to(*polar_to_cartesian(MAX_RADIUS, angle))
    ctx.stroke()

# 2. Main Recursive System
# Start with 8 primary segments
rings = 4
slices = 8
for i in range(rings):
    for j in range(slices):
        r_start = MIN_RADIUS + (i * (MAX_RADIUS - MIN_RADIUS) / rings)
        r_end = MIN_RADIUS + ((i + 1) * (MAX_RADIUS - MIN_RADIUS) / rings)
        # Apply non-linear radial scaling for "topographical" expansion
        r_start = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * math.pow(i/rings, 1.2)
        r_end = MIN_RADIUS + (MAX_RADIUS - MIN_RADIUS) * math.pow((i+1)/rings, 1.2)
        
        t_start = j * (2 * math.pi / slices)
        t_end = (j + 1) * (2 * math.pi / slices)
        
        recursive_subdivide(r_start, r_end, t_start, t_end, 0)

# 3. Final Polish: Mathematical Frame
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.set_line_width(1)
# Circular frame
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS + 10, 0, 2 * math.pi)
ctx.stroke()

# Crosshairs
ch_size = 15
for x, y in [(20, 20), (width-20, 20), (20, height-20), (width-20, height-20)]:
    ctx.move_to(x - ch_size, y)
    ctx.line_to(x + ch_size, y)
    ctx.move_to(x, y - ch_size)
    ctx.line_to(x, y + ch_size)
    ctx.stroke()

# Small Label (Aesthetic Typography substitute)
ctx.set_source_rgba(1, 1, 1, 0.5)
ctx.select_font_face("monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(width - 120, height - 15)
ctx.show_text("POLAR_SYS // R.TOPOGRAPHY_04")

# Cleanup / finalize
