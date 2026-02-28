import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.05)  # Deep indigo-black
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
CELLS = []
ITERATIONS = 5

def get_thermal_color(t):
    """Returns a color based on a thermal gradient: Indigo -> Violet -> Cinnabar -> White"""
    # t is 0.0 to 1.0
    colors = [
        (0.11, 0.0, 0.32),  # Deep Indigo
        (0.56, 0.0, 1.0),   # Violet
        (0.89, 0.26, 0.2),  # Cinnabar
        (1.0, 0.9, 0.8)     # Warm White
    ]
    
    if t <= 0: return colors[0]
    if t >= 1: return colors[-1]
    
    # Interpolation logic
    idx = t * (len(colors) - 1)
    i = int(idx)
    f = idx - i
    r = colors[i][0] + (colors[i+1][0] - colors[i][0]) * f
    g = colors[i][1] + (colors[i+1][1] - colors[i][1]) * f
    b = colors[i][2] + (colors[i+1][2] - colors[i][2]) * f
    return (r, g, b)

def subdivide(x, y, w, h, depth):
    """Recursive subdivision to create a Swiss-style hierarchical grid."""
    if depth > 0 and (random.random() > 0.2 or depth > 3):
        split_vertical = random.random() > 0.5
        if split_vertical:
            mid = w * random.uniform(0.3, 0.7)
            subdivide(x, y, mid, h, depth - 1)
            subdivide(x + mid, y, w - mid, h, depth - 1)
        else:
            mid = h * random.uniform(0.3, 0.7)
            subdivide(x, y, w, mid, depth - 1)
            subdivide(x, y + mid, w, h - mid, depth - 1)
    else:
        CELLS.append((x, y, w, h, depth))

# 1. Generate the initial Grid Logic (normalized 0-1 space)
subdivide(0, 0, 1, 1, ITERATIONS)

def project(norm_x, norm_y, entropy_factor):
    """Transforms normalized grid coordinates into a distorted polar space."""
    # Polar Mapping
    angle = norm_x * math.pi * 2.0
    radius = norm_y * MAX_RADIUS
    
    # Displacement logic (Structured Dissipation)
    # The further from the center (radius), the more entropy we introduce
    distortion = math.sin(angle * 8 + norm_y * 10) * (norm_y ** 2) * 25 * entropy_factor
    radius += distortion
    
    # Subtle rotation shift
    angle += math.cos(radius * 0.05) * 0.2 * entropy_factor

    px = CENTER_X + math.cos(angle) * radius
    py = CENTER_Y + math.sin(angle) * radius
    return px, py

# 2. Draw the logic
for x, y, w, h, depth in CELLS:
    # Use multiple layers for "temporal trails" and "vivid gradients"
    layers = 4
    for layer in range(layers):
        # Calculate entropy: increases per layer and per distance from center
        layer_dist = (layer / layers)
        entropy = layer_dist * 1.5
        
        # Color based on normalized radius (y) and layer
        color_val = (y + layer_dist * 0.5) % 1.0
        r, g, b = get_thermal_color(color_val)
        
        ctx.set_source_rgba(r, g, b, 0.8 - (layer * 0.15))
        ctx.set_line_width(0.4 if layer == 0 else 0.2)
        
        # Draw the cell as a warped path
        steps = 10
        # Move to top-left
        px, py = project(x, y, entropy)
        ctx.move_to(px, py)
        
        # Top edge
        for s in range(1, steps + 1):
            px, py = project(x + (w * s / steps), y, entropy)
            ctx.line_to(px, py)
            
        # Right edge
        for s in range(1, steps + 1):
            px, py = project(x + w, y + (h * s / steps), entropy)
            ctx.line_to(px, py)
            
        # Bottom edge
        for s in range(1, steps + 1):
            px, py = project(x + w - (w * s / steps), y + h, entropy)
            ctx.line_to(px, py)
            
        # Left edge
        for s in range(1, steps + 1):
            px, py = project(x, y + h - (h * s / steps), entropy)
            ctx.line_to(px, py)
            
        ctx.close_path()
        
        if random.random() > 0.1:
            ctx.stroke()
        else:
            ctx.fill()

# 3. Add Architectural Details (Fine dots and radial markers)
ctx.set_line_width(0.5)
for i in range(12):
    angle = (i / 12) * math.pi * 2
    r_start = MAX_RADIUS * 1.05
    r_end = MAX_RADIUS * 1.2
    
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.move_to(CENTER_X + math.cos(angle) * r_start, CENTER_Y + math.sin(angle) * r_start)
    ctx.line_to(CENTER_X + math.cos(angle) * r_end, CENTER_Y + math.sin(angle) * r_end)
    ctx.stroke()

# 4. Center Core "Precision"
ctx.set_source_rgb(1, 1, 1)
ctx.arc(CENTER_X, CENTER_Y, 2, 0, math.pi * 2)
ctx.fill()

# 5. Strategic "Mathematical" Glitch Lines
for _ in range(20):
    t = random.random()
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(MAX_RADIUS * 0.2, MAX_RADIUS * 0.9)
    length = random.uniform(10, 40)
    
    ctx.set_source_rgba(0.9, 0.3, 0.2, 0.6) # Cinnabar highlight
    x1 = CENTER_X + math.cos(angle) * dist
    y1 = CENTER_Y + math.sin(angle) * dist
    x2 = CENTER_X + math.cos(angle + 0.05) * (dist + length)
    y2 = CENTER_Y + math.sin(angle + 0.05) * (dist + length)
    
    ctx.set_line_width(0.3)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()
    
    # Tiny terminal dots
    ctx.arc(x2, y2, 0.8, 0, math.pi * 2)
    ctx.fill()

