import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep monochromatic void
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = min(width, height) * 0.45
GOLDEN_RATIO = (1 + 5**0.5) / 2

def polar_to_cartesian(r, theta, distortion=0):
    """Converts polar to cartesian with an optional harmonic radial distortion."""
    # Apply a flow-field style distortion based on angle and radius harmonics
    flux = distortion * math.sin(theta * 5 + r * 0.02) * math.cos(r * 0.01)
    r_distorted = r + flux
    x = CENTER_X + r_distorted * math.cos(theta)
    y = CENTER_Y + r_distorted * math.sin(theta)
    return x, y

def draw_distorted_arc(ctx, r, a1, a2, steps=40, distortion=0):
    """Draws an arc as a series of distorted segments to simulate flux."""
    for i in range(steps + 1):
        angle = a1 + (a2 - a1) * (i / steps)
        x, y = polar_to_cartesian(r, angle, distortion)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

def draw_distorted_radial(ctx, r1, r2, angle, steps=20, distortion=0):
    """Draws a radial line with harmonic distortion."""
    for i in range(steps + 1):
        radius = r1 + (r2 - r1) * (i / steps)
        x, y = polar_to_cartesian(radius, angle, distortion)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

def recursive_subdivide(r_min, r_max, a_min, a_max, depth):
    """Recursive Quadtree-like subdivision in polar space."""
    if depth <= 0 or (random.random() < 0.2 and depth < 3):
        # Render the cell
        render_cell(r_min, r_max, a_min, a_max, depth)
        return

    # Decide split: Radial (0) or Angular (1)
    split_type = random.choice([0, 1])
    
    if split_type == 0: # Radial split
        mid_r = r_min + (r_max - r_min) * (0.4 + random.random() * 0.2)
        recursive_subdivide(r_min, mid_r, a_min, a_max, depth - 1)
        recursive_subdivide(mid_r, r_max, a_min, a_max, depth - 1)
    else: # Angular split
        mid_a = a_min + (a_max - a_min) * 0.5
        recursive_subdivide(r_min, r_max, a_min, mid_a, depth - 1)
        recursive_subdivide(r_min, r_max, mid_a, a_max, depth - 1)

def render_cell(r_min, r_max, a_min, a_max, depth):
    """Visualizes the terminal nodes of the subdivision."""
    # Logic for distortion intensity - higher at the edges
    dist = (r_max / MAX_RADIUS) * 15.0
    
    # Layer 1: The "Ghost" structure
    ctx.set_line_width(0.3)
    ctx.set_source_rgba(0.4, 0.6, 1.0, 0.15)
    draw_distorted_arc(ctx, r_min, a_min, a_max, distortion=dist)
    ctx.stroke()
    
    # Layer 2: Highlighted segments (Swiss Precision)
    if random.random() > 0.4:
        weight = random.uniform(0.5, 2.0)
        ctx.set_line_width(weight)
        # Randomly choose one edge to highlight
        edge = random.randint(0, 3)
        ctx.set_source_rgba(0.9, 0.95, 1.0, 0.8)
        
        if edge == 0: draw_distorted_arc(ctx, r_min, a_min, a_max, distortion=dist)
        elif edge == 1: draw_distorted_arc(ctx, r_max, a_min, a_max, distortion=dist)
        elif edge == 2: draw_distorted_radial(ctx, r_min, r_max, a_min, distortion=dist)
        else: draw_distorted_radial(ctx, r_min, r_max, a_max, distortion=dist)
        ctx.stroke()

    # Layer 3: Micro-dithering / Data Clusters
    if depth == 0 and random.random() > 0.6:
        ctx.set_source_rgba(0, 1, 1, 0.5)
        for _ in range(15):
            pr = random.uniform(r_min, r_max)
            pa = random.uniform(a_min, a_max)
            px, py = polar_to_cartesian(pr, pa, dist)
            ctx.arc(px, py, 0.8, 0, 2 * math.pi)
            ctx.fill()

# --- Execution ---

# 1. Background Grid (Systematic Foundation)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.2, 0.3, 0.5, 0.2)
for r in range(0, int(MAX_RADIUS), 40):
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2*math.pi)
    ctx.stroke()

# 2. Main Recursive Structure
# We divide the circle into 4 primary quadrants to ensure balance
for i in range(4):
    start_angle = i * (math.pi / 2)
    end_angle = (i + 1) * (math.pi / 2)
    recursive_subdivide(40, MAX_RADIUS, start_angle, end_angle, 5)

# 3. Superimposed Global Flux Lines (The "Interruption")
ctx.set_line_width(0.5)
for i in range(12):
    angle = (i / 12) * 2 * math.pi
    ctx.set_source_rgba(1, 0.2, 0.4, 0.4) # Vibrant accent
    draw_distorted_radial(ctx, 20, MAX_RADIUS * 1.1, angle, steps=100, distortion=30)
    ctx.stroke()

# 4. Focal Point (Center Hierarchy)
ctx.set_source_rgb(1, 1, 1)
ctx.arc(CENTER_X, CENTER_Y, 3, 0, 2 * math.pi)
ctx.fill()
ctx.set_line_width(1)
ctx.arc(CENTER_X, CENTER_Y, 12, 0, 2 * math.pi)
ctx.stroke()

# 5. Fine Marginalia (Data Strings)
ctx.set_source_rgba(1, 1, 1, 0.6)
for i in range(80):
    a = random.uniform(0, math.pi * 2)
    r = MAX_RADIUS + random.uniform(10, 40)
    x, y = polar_to_cartesian(r, a, distortion=0)
    ctx.rectangle(x, y, 1.5, 1.5)
    ctx.fill()

# Final atmospheric pass: radial vignette
grad = cairo.RadialGradient(CENTER_X, CENTER_Y, MAX_RADIUS * 0.5, CENTER_X, CENTER_Y, MAX_RADIUS * 1.5)
grad.add_color_stop_rgba(0, 0, 0, 0, 0)
grad.add_color_stop_rgba(1, 0.02, 0.03, 0.05, 0.8)
ctx.set_source(grad)
ctx.paint()

