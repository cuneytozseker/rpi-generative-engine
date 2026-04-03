import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

# Constants for the Polar Grid
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
COLOR_IVORY = (0.92, 0.94, 0.88)
COLOR_COBALT = (0.2, 0.4, 0.8)

def project(r, theta, distortion=0):
    """Transforms polar coordinates to cartesian with radial distortion."""
    # Apply a harmonic radial distortion
    r_distorted = r + (distortion * math.sin(theta * 6 + r * 0.02))
    x = CENTER_X + r_distorted * math.cos(theta)
    y = CENTER_Y + r_distorted * math.sin(theta)
    return x, y

def draw_glyph(x, y, size, type="cross"):
    """Draws a technical marker at the specified point."""
    ctx.set_line_width(0.5)
    if type == "cross":
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
    elif type == "box":
        ctx.rectangle(x - size/2, y - size/2, size, size)
    ctx.stroke()

def recursive_subdivide(r1, r2, a1, a2, depth, max_depth):
    """Recursive partition of polar space mimicking a radial quadtree."""
    
    # Decide whether to split or render based on depth and pseudo-random chance
    # Higher chance to split at lower radii to create focal density
    split_chance = 0.85 if r1 < MAX_RADIUS * 0.6 else 0.4
    
    if depth < max_depth and random.random() < split_chance:
        mid_r = (r1 + r2) / 2
        mid_a = (a1 + a2) / 2
        
        # Quadrant logic
        recursive_subdivide(r1, mid_r, a1, mid_a, depth + 1, max_depth)
        recursive_subdivide(mid_r, r2, a1, mid_a, depth + 1, max_depth)
        recursive_subdivide(r1, mid_r, mid_a, a2, depth + 1, max_depth)
        recursive_subdivide(mid_r, r2, mid_a, a2, depth + 1, max_depth)
    else:
        # Render the cell boundary
        render_cell(r1, r2, a1, a2, depth)

def render_cell(r1, r2, a1, a2, depth):
    """Draws the geometry of a single grid cell."""
    distortion_amt = 15.0
    
    # Set color and weight based on depth (hierarchy)
    opacity = 0.3 + (depth * 0.15)
    ctx.set_source_rgba(COLOR_IVORY[0], COLOR_IVORY[1], COLOR_IVORY[2], opacity)
    ctx.set_line_width(0.8 / (depth + 1))
    
    # Draw arc segment (Outer Radius)
    steps = 10
    for i in range(steps + 1):
        a = a1 + (a2 - a1) * (i / steps)
        x, y = project(r2, a, distortion_amt)
        if i == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

    # Draw radial segment (Left Edge)
    x_start, y_start = project(r1, a1, distortion_amt)
    x_end, y_end = project(r2, a1, distortion_amt)
    ctx.move_to(x_start, y_start)
    ctx.line_to(x_end, y_end)
    ctx.stroke()

    # Probability-based technical detailing
    if random.random() > 0.7:
        # Technical Glyph at corner
        gx, gy = project(r1, a1, distortion_amt)
        ctx.set_source_rgba(COLOR_COBALT[0], COLOR_COBALT[1], COLOR_COBALT[2], 0.8)
        draw_glyph(gx, gy, 2, "cross")
        
    if depth > 3 and random.random() > 0.8:
        # Interior hatching
        ctx.set_source_rgba(COLOR_IVORY[0], COLOR_IVORY[1], COLOR_IVORY[2], 0.1)
        for i in range(1, 4):
            r_hatch = r1 + (r2 - r1) * (i / 4)
            for j in range(5):
                a_hatch = a1 + (a2 - a1) * (j / 5)
                hx, hy = project(r_hatch, a_hatch, distortion_amt)
                ctx.arc(hx, hy, 0.5, 0, 2 * math.pi)
                ctx.fill()

# --- Main Composition Execution ---

# 1. Background Harmonic Rings (Faint)
ctx.set_line_width(0.2)
for r in range(0, int(MAX_RADIUS * 1.5), 20):
    ctx.set_source_rgba(0.2, 0.3, 0.4, 0.2)
    for a_idx in range(120):
        a = (a_idx / 120) * 2 * math.pi
        x, y = project(r, a, 10)
        if a_idx == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.close_path()
    ctx.stroke()

# 2. Primary Recursive Polar Grid
random.seed(42) # Deterministic for layout stability
num_sectors = 8
for s in range(num_sectors):
    angle_start = (s / num_sectors) * 2 * math.pi
    angle_end = ((s + 1) / num_sectors) * 2 * math.pi
    recursive_subdivide(20, MAX_RADIUS, angle_start, angle_end, 0, 5)

# 3. High-Contrast Overlay Elements (Graph Nodes)
ctx.set_line_width(1.0)
nodes = []
for _ in range(12):
    r = random.uniform(50, MAX_RADIUS)
    a = random.uniform(0, 2 * math.pi)
    nodes.append(project(r, a, 15))

# Draw connections
ctx.set_source_rgba(0.9, 0.2, 0.2, 0.4) # Accent color: technical red
ctx.set_dash([4.0, 2.0])
for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        dist = math.sqrt((nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2)
        if dist < 120:
            ctx.move_to(*nodes[i])
            ctx.line_to(*nodes[j])
            ctx.stroke()

# Draw node markers
ctx.set_dash([])
for nx, ny in nodes:
    ctx.set_source_rgb(1, 1, 1)
    ctx.arc(nx, ny, 2, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.arc(nx, ny, 5, 0, 2*math.pi)
    ctx.stroke()

# 4. Perimeter Typography/Ticks (Swiss aesthetic)
ctx.set_source_rgba(COLOR_IVORY[0], COLOR_IVORY[1], COLOR_IVORY[2], 0.6)
for i in range(36):
    a = (i / 36) * 2 * math.pi
    x1, y1 = project(MAX_RADIUS + 5, a, 0)
    x2, y2 = project(MAX_RADIUS + 15, a, 0)
    ctx.set_line_width(1.5 if i % 9 == 0 else 0.5)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Final Polish: Central Data Core
ctx.set_source_rgb(0.9, 0.9, 1.0)
ctx.arc(CENTER_X, CENTER_Y, 3, 0, 2 * math.pi)
ctx.fill()
ctx.set_line_width(0.5)
ctx.arc(CENTER_X, CENTER_Y, 8, 0, 2 * math.pi)
ctx.stroke()

