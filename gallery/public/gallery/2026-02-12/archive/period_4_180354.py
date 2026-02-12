import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: High-contrast Void
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Constants
PHI = (1 + 5**0.5) / 2
CENTER_X, CENTER_Y = width / 2, height / 2
ACCENT_COLOR = (1.0, 0.1, 0.2)  # Surgical Red

def get_distance_factor(x, y, w, h):
    """Calculates proximity to center to drive centripetal density."""
    cx, cy = x + w/2, y + h/2
    dist = math.sqrt((cx - CENTER_X)**2 + (cy - CENTER_Y)**2)
    max_dist = math.sqrt(CENTER_X**2 + CENTER_Y**2)
    return 1.0 - (dist / max_dist)

def draw_data_glyph(x, y, w, h, weight):
    """Draws microscopic symbolic mappings within a cell."""
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(1, 1, 1, weight * 0.8)
    
    margin = w * 0.2
    inner_w = w - (margin * 2)
    inner_h = h - (margin * 2)
    
    # Draw a technical crosshair or rect
    if weight > 0.6:
        ctx.rectangle(x + margin, y + margin, inner_w, inner_h)
        ctx.stroke()
        # Binary 'bit' indicator
        if random.random() > 0.5:
            ctx.rectangle(x + margin + 2, y + margin + 2, 2, 2)
            ctx.fill()

def draw_recursive_system(x, y, w, h, depth):
    # Centripetal logic: Increase depth based on proximity to center
    factor = get_distance_factor(x, y, w, h)
    max_depth = 4 + int(factor * 6)
    
    # Base Case
    if depth > max_depth or w < 5 or h < 5:
        # Draw the "Cell"
        ctx.set_line_width(0.3)
        ctx.set_source_rgba(1, 1, 1, 0.1 + (factor * 0.4))
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        
        # Chromatic Shrapnel: Random high-frequency data points
        if factor > 0.7 and random.random() > 0.92:
            ctx.set_source_rgb(*ACCENT_COLOR)
            ctx.rectangle(x, y, w, h)
            ctx.fill()
            
        # Internal Logarithmic Detail
        if w > 15 and h > 15:
            draw_data_glyph(x, y, w, h, factor)
        return

    # Golden Ratio Subdivision
    split = 1 / PHI
    # Controlled jitter to simulate "algorithmic entropy"
    jitter = (random.random() - 0.5) * 0.05
    split += jitter

    if w > h:
        # Vertical Split
        w1 = w * split
        draw_recursive_system(x, y, w1, h, depth + 1)
        draw_recursive_system(x + w1, y, w - w1, h, depth + 1)
    else:
        # Horizontal Split
        h1 = h * split
        draw_recursive_system(x, y, w, h1, depth + 1)
        draw_recursive_system(x, y + h1, w, h - h1, depth + 1)

def draw_flow_lines():
    """Adds a layer of atmospheric interference (orthogonal paths)."""
    for i in range(40):
        factor = random.random()
        ctx.set_line_width(0.2 if factor < 0.8 else 1.2)
        ctx.set_source_rgba(1, 1, 1, 0.05 + (factor * 0.1))
        
        if random.random() > 0.5:
            # Horizontal interference
            py = random.uniform(0, height)
            ctx.move_to(0, py)
            ctx.line_to(width, py)
        else:
            # Vertical interference
            px = random.uniform(0, width)
            ctx.move_to(px, 0)
            ctx.line_to(px, height)
        ctx.stroke()

# Execution Sequence
# 1. Background Grid/Atmosphere
draw_flow_lines()

# 2. Primary Recursive Data Structure
# Centered start for symmetry
draw_recursive_system(20, 20, width - 40, height - 40, 0)

# 3. Focal Interference Overlays
ctx.set_operator(cairo.OPERATOR_ADD)
for _ in range(5):
    # Radial "Light" modulation at the core
    r = random.uniform(20, 80)
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.fill()

# 4. Final Branding/Swiss Elements (Minimalist markers)
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(2)
# Corner marks
size = 10
corners = [(10, 10), (width-10, 10), (10, height-10), (width-10, height-10)]
for cx, cy in corners:
    ctx.move_to(cx - size/2, cy)
    ctx.line_to(cx + size/2, cy)
    ctx.move_to(cx, cy - size/2)
    ctx.line_to(cx, cy + size/2)
    ctx.stroke()

