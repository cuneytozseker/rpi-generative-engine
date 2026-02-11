import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI
COLORS = [
    (0.05, 0.05, 0.1),   # Deep Space
    (0.1, 0.4, 0.9),    # Electric Blue
    (1.0, 0.2, 0.4),    # Vibrant Magenta
    (0.95, 0.95, 0.95), # Swiss White
    (1.0, 0.8, 0.1)     # Golden Highlight
]

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_flow_angle(x, y, scale=0.005):
    """Generates a mathematical flow angle based on coordinates."""
    angle = math.sin(x * scale) * math.cos(y * scale) * math.pi * 2
    angle += math.sin((x + y) * scale * 0.5) * math.pi
    return angle

def draw_flow_lines(x, y, w, h, depth):
    """Draws granular, fluid lines within a bounding box."""
    ctx.save()
    # Masking the area
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    
    line_count = int((w * h) / (150 - depth * 15))
    for _ in range(max(5, line_count)):
        px, py = x + random.random() * w, y + random.random() * h
        
        # Color selection based on position and depth
        color_idx = (depth + int(px/100)) % len(COLORS)
        r, g, b = COLORS[color_idx]
        alpha = random.uniform(0.2, 0.7)
        ctx.set_source_rgba(r, g, b, alpha)
        
        ctx.set_line_width(random.uniform(0.5, 2.5) / (depth + 1))
        
        ctx.move_to(px, py)
        steps = random.randint(5, 15)
        step_len = random.uniform(2, 8)
        
        for _ in range(steps):
            angle = get_flow_angle(px, py)
            px += math.cos(angle) * step_len
            py += math.sin(angle) * step_len
            ctx.line_to(px, py)
        
        ctx.stroke()
    ctx.restore()

def recursive_subdivide(x, y, w, h, depth):
    """Recursive subdivision using golden ratio proportions."""
    if depth > 5 or (w * h < 4000 and depth > 2):
        draw_flow_lines(x, y, w, h, depth)
        # Draw subtle border for structural hierarchy
        ctx.set_source_rgba(1, 1, 1, 0.1)
        ctx.set_line_width(0.3)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        return

    # Decide split direction based on aspect ratio or depth
    split_vertically = w > h
    
    # Golden ratio split point
    if split_vertically:
        split_size = w * INV_PHI
        # Variation: occasionally flip the split
        if random.random() > 0.5:
            recursive_subdivide(x, y, split_size, h, depth + 1)
            recursive_subdivide(x + split_size, y, w - split_size, h, depth + 1)
        else:
            recursive_subdivide(x, y, w - split_size, h, depth + 1)
            recursive_subdivide(x + (w - split_size), y, split_size, h, depth + 1)
    else:
        split_size = h * INV_PHI
        if random.random() > 0.5:
            recursive_subdivide(x, y, w, split_size, depth + 1)
            recursive_subdivide(x, y + split_size, w, h - split_size, depth + 1)
        else:
            recursive_subdivide(x, y, w, h - split_size, depth + 1)
            recursive_subdivide(x, y + (h - split_size), w, split_size, depth + 1)

# Start recursion
recursive_subdivide(20, 20, width - 40, height - 40, 0)

# Add a "Swiss Grid" overlay for structural precision
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
grid_size = 40
for i in range(int(width/grid_size) + 1):
    ctx.move_to(i * grid_size, 0)
    ctx.line_to(i * grid_size, height)
    ctx.stroke()
for j in range(int(height/grid_size) + 1):
    ctx.move_to(0, j * grid_size)
    ctx.line_to(width, j * grid_size)
    ctx.stroke()

# Final atmospheric "Leaking" effect
for _ in range(12):
    cx, cy = random.random() * width, random.random() * height
    rad = random.uniform(50, 150)
    grad = cairo.RadialGradient(cx, cy, 0, cx, cy, rad)
    r, g, b = random.choice(COLORS)
    grad.add_color_stop_rgba(0, r, g, b, 0.15)
    grad.add_color_stop_rgba(1, r, g, b, 0)
    ctx.set_source(grad)
    ctx.arc(cx, cy, rad, 0, math.pi * 2)
    ctx.fill()

# Geometric Labeling (Swiss style)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgba(1, 1, 1, 0.6)
ctx.move_to(30, height - 30)
ctx.show_text("SYSTEM: RECURSIVE_FLUIDITY // SUBDIV: PHI_RATIO")
ctx.move_to(width - 160, 35)
ctx.show_text("COORD_FIELD_01_GEN")

