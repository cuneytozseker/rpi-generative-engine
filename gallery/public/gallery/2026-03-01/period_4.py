import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Cobalt/Black base
ctx.set_source_rgb(0.02, 0.03, 0.1)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width * 0.45, height * 0.55
MAX_RADIUS = min(width, height) * 0.8
COBALT = (0.0, 0.4, 0.9)
WHITE = (0.95, 0.95, 0.98)
ACCENT_RED = (0.9, 0.1, 0.2)

def polar_to_cartesian(r, theta, dist_freq=0, dist_amp=0):
    """Converts polar coordinates with an optional radial distortion."""
    # Radial distortion based on frequency modulation
    r_offset = math.sin(theta * dist_freq) * dist_amp
    effective_r = r + r_offset
    x = CENTER_X + effective_r * math.cos(theta)
    y = CENTER_Y + effective_r * math.sin(theta)
    return x, y

def draw_dithered_sector(r_start, r_end, a_start, a_end, density=0.4):
    """Simulates a bitmask/dithered texture within a polar segment."""
    ctx.set_source_rgba(*WHITE, 0.3)
    steps_r = int((r_end - r_start) / 4)
    steps_a = int((a_end - a_start) * r_start / 4)
    
    for i in range(max(1, steps_r)):
        for j in range(max(1, steps_a)):
            if random.random() < density:
                r = r_start + (i / max(1, steps_r)) * (r_end - r_start)
                a = a_start + (j / max(1, steps_a)) * (a_end - a_start)
                x, y = polar_to_cartesian(r, a)
                ctx.rectangle(x, y, 1.2, 1.2)
                ctx.fill()

def recursive_polar_grid(r_min, r_max, a_min, a_max, depth):
    """Recursive subdivision of polar space following Swiss grid principles."""
    if depth <= 0 or (random.random() < 0.2 and depth < 3):
        # Draw final element
        style = random.random()
        
        # Hairline strokes for "technical schematic" look
        ctx.set_line_width(0.4 if random.random() > 0.2 else 1.5)
        
        if style < 0.4:
            # Concentric Arcs
            ctx.set_source_rgba(*WHITE, 0.8)
            ctx.new_sub_path()
            ctx.arc(CENTER_X, CENTER_Y, r_min, a_min, a_max)
            ctx.stroke()
        elif style < 0.7:
            # Radial Segments
            ctx.set_source_rgba(*COBALT, 0.6)
            x1, y1 = polar_to_cartesian(r_min, a_min)
            x2, y2 = polar_to_cartesian(r_max, a_min)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()
        elif style < 0.9:
            # Dithered Masses
            draw_dithered_sector(r_min, r_max, a_min, a_max, density=0.2 * (4-depth))
        return

    # Subdivide
    split_r = random.random() > 0.4
    if split_r:
        mid_r = r_min + (r_max - r_min) * random.uniform(0.3, 0.7)
        recursive_polar_grid(r_min, mid_r, a_min, a_max, depth - 1)
        recursive_polar_grid(mid_r, r_max, a_min, a_max, depth - 1)
    else:
        mid_a = a_min + (a_max - a_min) * random.uniform(0.3, 0.7)
        recursive_polar_grid(r_min, r_max, a_min, mid_a, depth - 1)
        recursive_polar_grid(r_min, r_max, mid_a, a_max, depth - 1)

# --- 1. Draw Background Flow Field ---
# Fragmented line segments following a modulated trajectory
for _ in range(120):
    r_base = random.uniform(50, MAX_RADIUS * 1.2)
    a_base = random.uniform(0, math.pi * 2)
    length = random.uniform(0.1, 0.5)
    
    ctx.set_source_rgba(*COBALT, 0.15)
    ctx.set_line_width(0.3)
    
    ctx.move_to(*polar_to_cartesian(r_base, a_base, 8, 10))
    # Draw segment as a distorted arc
    for step in range(10):
        a = a_base + (step/10.0) * length
        ctx.line_to(*polar_to_cartesian(r_base, a, 8, 10))
    ctx.stroke()

# --- 2. Draw Main Recursive Structure ---
# Higher depth in a specific quadrant for asymmetric tension
recursive_polar_grid(40, MAX_RADIUS, 0, math.pi * 1.5, 6)
recursive_polar_grid(40, MAX_RADIUS * 0.5, math.pi * 1.5, math.pi * 2, 4)

# --- 3. Geometric Accents (The "Precise" Layer) ---
# Large circular frame with scale indicators
ctx.set_source_rgba(*WHITE, 0.2)
ctx.set_line_width(0.5)
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS, 0, math.pi * 2)
ctx.stroke()

for i in range(72):
    angle = (i / 72.0) * math.pi * 2
    inner = MAX_RADIUS if i % 6 != 0 else MAX_RADIUS - 15
    outer = MAX_RADIUS + 5
    x1, y1 = polar_to_cartesian(inner, angle)
    x2, y2 = polar_to_cartesian(outer, angle)
    
    ctx.set_source_rgba(*WHITE, 0.4 if i % 6 == 0 else 0.2)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# --- 4. Brutalist Red Accents ---
# Random blocks of color following the grid's logic
for _ in range(5):
    r = random.uniform(60, MAX_RADIUS * 0.8)
    a = random.uniform(0, math.pi * 2)
    ctx.set_source_rgba(*ACCENT_RED, 0.8)
    x, y = polar_to_cartesian(r, a)
    ctx.rectangle(x, y, 8, 2)
    ctx.fill()

# --- 5. Data-Density Clusters ---
# Small "bit" markers in a tight grid
for i in range(3):
    start_r = random.uniform(100, 200)
    start_a = random.uniform(0, math.pi)
    ctx.set_source_rgb(*WHITE)
    for row in range(4):
        for col in range(4):
            x, y = polar_to_cartesian(start_r + row*6, start_a + (col*0.02))
            ctx.rectangle(x, y, 1.5, 1.5)
            ctx.fill()

# --- 6. Focal Distortion Lines ---
# High-frequency radial lines
ctx.set_source_rgba(*WHITE, 0.05)
for i in range(180):
    a = (i / 180.0) * math.pi * 2
    r_start = MAX_RADIUS * 0.9
    r_end = MAX_RADIUS * (0.95 + 0.1 * math.sin(a * 20))
    x1, y1 = polar_to_cartesian(r_start, a)
    x2, y2 = polar_to_cartesian(r_end, a)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Clean up / Fine tuning
ctx.set_source_rgba(*WHITE, 0.9)
ctx.arc(CENTER_X, CENTER_Y, 2, 0, 7)
ctx.fill() # Small central datum point
