import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width // 2, height // 2
MAX_RADIUS = 260
ACCENT_COLOR = (1.0, 0.31, 0.0)  # International Orange (Swiss Accent)
WHITE = (0.95, 0.95, 0.95)

def to_cartesian(r, theta):
    """Converts polar to cartesian with a slight radial distortion."""
    # Radial distortion: distance modulates based on angle to create a 'swelling' effect
    distortion = 1.0 + 0.05 * math.sin(theta * 4) * math.cos(r * 0.01)
    x = CENTER_X + (r * distortion) * math.cos(theta)
    y = CENTER_Y + (r * distortion) * math.sin(theta)
    return x, y

def draw_technical_mark(r, theta, size):
    """Draws a small crosshair or glyph at a polar coordinate."""
    x, y = to_cartesian(r, theta)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

def recursive_sector(r1, r2, t1, t2, depth):
    """Recursive partitioning of a polar sector."""
    # Base case or random stop to create variable density
    if depth > 4 or (depth > 1 and random.random() < 0.25):
        # Draw the content of the leaf node
        draw_node_content(r1, r2, t1, t2, depth)
        return

    # Split logic: alternating between radial and angular splits
    if depth % 2 == 0:
        # Split angularly
        mid_t = (t1 + t2) / 2
        recursive_sector(r1, r2, t1, mid_t, depth + 1)
        recursive_sector(r1, r2, mid_t, t2, depth + 1)
    else:
        # Split radially using golden ratio for non-linear spacing
        mid_r = r1 + (r2 - r1) * 0.618
        recursive_sector(r1, mid_r, t1, t2, depth + 1)
        recursive_sector(mid_r, r2, t1, t2, depth + 1)

def draw_node_content(r1, r2, t1, t2, depth):
    """Visualizes an individual data cell within the grid."""
    # Density modulation
    density = random.random()
    
    # 1. Outline the cell
    ctx.set_line_width(0.4)
    ctx.set_source_rgba(*WHITE, 0.3)
    
    # Draw arc segments
    steps = 10
    for r in [r1, r2]:
        ctx.move_to(*to_cartesian(r, t1))
        for i in range(1, steps + 1):
            t = t1 + (t2 - t1) * (i / steps)
            ctx.line_to(*to_cartesian(r, t))
        ctx.stroke()
    
    # Draw radial edges
    for t in [t1, t2]:
        ctx.move_to(*to_cartesian(r1, t))
        ctx.line_to(*to_cartesian(r2, t))
        ctx.stroke()

    # 2. Add "Digital Noise" / Binary Stippling
    if density > 0.6:
        ctx.set_source_rgba(*WHITE, 0.8)
        num_dots = int((r2 - r1) * (t2 - t1) * 5)
        for _ in range(min(num_dots, 20)):
            dot_r = random.uniform(r1, r2)
            dot_t = random.uniform(t1, t2)
            dx, dy = to_cartesian(dot_r, dot_t)
            ctx.rectangle(dx, dy, 1, 1)
            ctx.fill()

    # 3. Functional Accent Tags
    if density > 0.92:
        ctx.set_source_rgb(*ACCENT_COLOR)
        ctx.set_line_width(1.5)
        # Highlight the inner corner
        ax, ay = to_cartesian(r1, t1)
        ctx.arc(ax, ay, 2, 0, 2 * math.pi)
        ctx.fill()
        
        # Tiny technical line
        ctx.move_to(ax, ay)
        lx, ly = to_cartesian(r1 - 10, t1)
        ctx.line_to(lx, ly)
        ctx.stroke()

# --- Execution ---

# 1. Draw Global Radial Guides (Systematic Hierarchy)
ctx.set_source_rgba(*WHITE, 0.1)
ctx.set_line_width(0.2)
for i in range(1, 12):
    r = (MAX_RADIUS / 11) * i
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Draw Recursive Information Architecture
# Using 8 main sectors as the root of the transformation
sectors = 8
for i in range(sectors):
    t_start = (2 * math.pi / sectors) * i
    t_end = (2 * math.pi / sectors) * (i + 1)
    recursive_sector(40, MAX_RADIUS, t_start, t_end, 0)

# 3. Overlay Mathematical Cadence (Non-linear intervals)
ctx.set_source_rgba(*WHITE, 0.5)
for i in range(40):
    # Logarithmic distribution of technical ticks
    angle = (i / 40.0) * 2 * math.pi
    r_tick = 30 + (math.log(i + 1) * 60)
    draw_technical_mark(r_tick, angle, 3)

# 4. Focal Compression Line
# A singular bold stroke that breaks the circularity, representing an axis
ctx.set_source_rgba(*WHITE, 0.15)
ctx.set_line_width(1)
ctx.move_to(0, CENTER_Y)
ctx.line_to(width, CENTER_Y)
ctx.stroke()

# 5. Final Swiss Detail: Title/Metadata block logic (abstracted)
ctx.set_source_rgb(*WHITE)
for i in range(5):
    y_off = height - 40 + (i * 6)
    ctx.move_to(40, y_off)
    ctx.set_line_width(2 if i == 0 else 0.5)
    ctx.line_to(40 + (100 if i == 0 else 60), y_off)
    ctx.stroke()

# Clean up
ctx.stroke()
