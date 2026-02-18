import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
COLORS = [
    (0.05, 0.1, 0.4, 0.3),  # Deep Indigo
    (0.1, 0.3, 0.7, 0.2),   # Bright Blue
    (0.9, 0.3, 0.1, 0.4),   # Burning Orange
    (1.0, 0.7, 0.1, 0.1),   # Incandescent Yellow
    (0.95, 0.95, 1.0, 0.8)  # Surgical White
]

# Background: Deep charcoal
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_dithered_line(x1, y1, x2, y2, color, weight):
    """Simulates a bitmapped/dithered line module."""
    ctx.set_source_rgba(*color)
    dist = math.hypot(x2 - x1, y2 - y1)
    steps = int(dist * 2)
    for i in range(steps):
        t = i / steps
        px = x1 + (x2 - x1) * t
        py = y1 + (y2 - y1) * t
        # Add jitter for 'bitmapped' feel
        jitter = random.uniform(-0.5, 0.5)
        ctx.rectangle(px + jitter, py + jitter, weight, weight)
    ctx.fill()

def draw_glow(x, y, w, h, color):
    """Creates a soft 'aura' or digital heat signature."""
    gradient = cairo.RadialGradient(x + w/2, y + h/2, 0, x + w/2, y + h/2, max(w, h))
    gradient.add_color_stop_rgba(0, color[0], color[1], color[2], color[3])
    gradient.add_color_stop_rgba(0.8, color[0], color[1], color[2], 0)
    
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.set_source(gradient)
    ctx.rectangle(x, y, w, h)
    ctx.fill()
    ctx.restore()

def subdivide(x, y, w, h, depth):
    """Recursive Golden Ratio subdivision with systematic interference."""
    if depth <= 0 or w < 5 or h < 5:
        return

    # Determine split orientation based on aspect ratio
    split_horizontally = w < h
    
    # Golden Ratio split
    if split_horizontally:
        split_point = h / PHI
        # Draw interference line
        draw_dithered_line(x, y + split_point, x + w, y + split_point, COLORS[depth % 4], 0.6)
        
        # Chance to trigger an 'aura'
        if random.random() > 0.7:
            draw_glow(x, y, w, split_point, COLORS[2])
            
        subdivide(x, y, w, split_point, depth - 1)
        subdivide(x, y + split_point, w, h - split_point, depth - 1)
    else:
        split_point = w / PHI
        draw_dithered_line(x + split_point, y, x + split_point, y + h, COLORS[depth % 4], 0.6)
        
        if random.random() > 0.8:
            draw_glow(x + split_point, y, w - split_point, h, COLORS[0])
            
        subdivide(x, y, split_point, h, depth - 1)
        subdivide(x + split_point, y, w - split_point, h, depth - 1)

# 1. Background Grid: Non-linear spacing (congestion towards center)
ctx.set_line_width(0.3)
grid_count = 40
for i in range(grid_count + 1):
    # Normalized position 0 to 1
    t = i / grid_count
    # Non-linear mapping to create "gravitational pull"
    # Mapping t from [0,1] to [0,1] with a bias towards 0.5
    dist_from_center = abs(t - 0.5) * 2
    offset = math.pow(dist_from_center, 1.8) * 0.5
    pos = 0.5 + (offset if t > 0.5 else -offset)
    
    # Vertical Lines
    ctx.set_source_rgba(0.2, 0.3, 0.5, 0.15)
    ctx.move_to(pos * width, 0)
    ctx.line_to(pos * width, height)
    ctx.stroke()
    
    # Horizontal Lines
    ctx.move_to(0, pos * height)
    ctx.line_to(width, pos * height)
    ctx.stroke()

# 2. Main Recursive Structure
subdivide(40, 40, width - 80, height - 80, 10)

# 3. Floating "Signal Interference" modules
# Discrete bitmapped modules
for _ in range(12):
    rx = random.uniform(50, width - 50)
    ry = random.uniform(50, height - 50)
    rw = random.uniform(10, 60)
    rh = random.uniform(2, 10)
    
    # Draw a "data packet" - a sequence of dithered blocks
    ctx.set_operator(cairo.OPERATOR_ADD)
    for j in range(5):
        alpha = (5 - j) / 10
        ctx.set_source_rgba(1.0, 0.5, 0.1, alpha)
        ctx.rectangle(rx + (j * 4), ry, 2, rh)
        ctx.fill()

# 4. Final layer: High-precision "Surgical" lines
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_line_width(0.2)
ctx.set_source_rgba(1, 1, 1, 0.6)
for i in range(5):
    y_pos = height * 0.15 + (i * PHI * 15)
    ctx.move_to(width * 0.1, y_pos)
    ctx.line_to(width * 0.9, y_pos)
    ctx.stroke()

# Add a small geometric "anchor" for Swiss precision
ctx.set_source_rgb(0.9, 0.9, 1.0)
ctx.rectangle(width - 60, height - 60, 20, 20)
ctx.set_line_width(1.0)
ctx.stroke()
ctx.move_to(width - 60, height - 50)
ctx.line_to(width - 40, height - 50)
ctx.stroke()

# Final Polish: Subtle global noise texture (simulated)
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.rectangle(random.random() * width, random.random() * height, 1, 1)
    ctx.fill()
