import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Systematic Navy
ctx.set_source_rgb(0.02, 0.03, 0.08)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
rings = 18
segments = 42
phi = (1 + math.sqrt(5)) / 2  # Golden ratio for harmonic spacing

def draw_glyph(x, y, size, style=0):
    """Draws technical/data-viz glyphs at specific coordinates."""
    ctx.set_line_width(0.6)
    if style == 0: # Crosshair
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
    elif style == 1: # Tiny box
        ctx.rectangle(x - size/2, y - size/2, size, size)
        ctx.fill()
    elif style == 2: # Binary-like tick
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()

def get_polar_coords(r_idx, s_idx, total_rings, total_segments):
    """Calculates distorted polar coordinates with radial expansion."""
    # Radial distortion: exponential growth for 'centripetal' focus
    normalized_r = (r_idx / total_rings) ** 1.4
    r = normalized_r * (width * 0.45)
    
    # Angular modulation: introduces subtle waves in the grid
    theta = (s_idx / total_segments) * 2 * math.pi
    theta += 0.1 * math.sin(r * 0.02) 
    
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return x, y

# 1. LAYER: Underlying Radial Grid (Hairlines)
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.4)

for r in range(rings):
    for s in range(segments):
        x1, y1 = get_polar_coords(r, s, rings, segments)
        x2, y2 = get_polar_coords(r + 1, s, rings, segments)
        x3, y3 = get_polar_coords(r, s + 1, rings, segments)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        ctx.move_to(x1, y1)
        ctx.line_to(x3, y3)
        ctx.stroke()

# 2. LAYER: Data Connections (Asymmetric Network)
ctx.set_source_rgba(0.0, 0.8, 1.0, 0.4) # Cyan highlight
ctx.set_line_width(0.8)
for _ in range(12):
    r_start, s_start = random.randint(2, rings-1), random.randint(0, segments-1)
    r_end, s_end = r_start + random.randint(-2, 2), s_start + random.randint(5, 10)
    
    x_s, y_s = get_polar_coords(r_start, s_start, rings, segments)
    x_e, y_e = get_polar_coords(r_end, s_end, rings, segments)
    
    ctx.move_to(x_s, y_s)
    # Quadratic curve to simulate technical drafting
    ctx.curve_to(center_x, center_y, (x_s+x_e)/2, (y_s+y_e)/2, x_e, y_e)
    ctx.stroke()

# 3. LAYER: Glyphs and "Numeric" Anchors
random.seed(42) # Deterministic randomness for layout stability
for r in range(1, rings):
    for s in range(segments):
        if random.random() > 0.85:
            x, y = get_polar_coords(r, s, rings, segments)
            
            # Draw glyph
            ctx.set_source_rgba(1, 1, 1, 0.8)
            draw_glyph(x, y, 3, style=random.randint(0, 2))
            
            # Draw fake numeric labels (small ticks)
            if random.random() > 0.7:
                ctx.set_source_rgba(1, 1, 1, 0.4)
                ctx.set_line_width(1.5)
                ctx.move_to(x + 5, y)
                ctx.line_to(x + 12, y)
                ctx.stroke()
                ctx.set_line_width(0.5)
                ctx.move_to(x + 5, y + 3)
                ctx.line_to(x + 10, y + 3)
                ctx.stroke()

# 4. LAYER: Focal Points (Solid Blocks)
ctx.set_source_rgba(1, 1, 1, 0.9)
for i in range(4):
    angle = i * (math.pi / 2) + 0.5
    dist = 180
    fx = center_x + math.cos(angle) * dist
    fy = center_y + math.sin(angle) * dist
    
    # High-contrast solid block
    ctx.rectangle(fx - 4, fy - 4, 8, 8)
    ctx.fill()
    
    # Secondary stroke for depth
    ctx.set_line_width(1)
    ctx.arc(fx, fy, 12, 0, math.pi * 1.5)
    ctx.stroke()

# 5. LAYER: The Peripheral "Annotation" Ring
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(20)
ctx.arc(center_x, center_y, width * 0.42, 0, 2 * math.pi)
ctx.stroke()

# Fine hairlines across the whole composition to tie it together
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(0.2)
for i in range(0, width, 40):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()

# Final Polish: Central Core
ctx.set_source_rgb(1, 1, 1)
ctx.arc(center_x, center_y, 2, 0, 2 * math.pi)
ctx.fill()
