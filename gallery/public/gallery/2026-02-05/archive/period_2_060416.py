import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Monolithic Ebony
ctx.set_source_rgb(0.01, 0.01, 0.02)
ctx.paint()

# Constants
center_x, center_y = width // 2, height // 2
max_radius = min(width, height) * 0.45
rings = 42
spokes = 64
accent_color = (1.0, 0.1, 0.2)  # Surgical Red/Orange
white = (0.95, 0.95, 1.0)

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    # Radial distortion based on harmonic resonance
    r_distorted = r * (1 + distortion_factor * math.sin(theta * 6))
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

# 1. Non-Uniform Grid Subdivisions (Radial Rings)
# Using power-law distribution to increase frequency toward the center (centripetal focus)
for i in range(rings):
    # Normalized index (0 to 1)
    t = i / rings
    # Power function shifts density: t^0.5 clusters near 0 (center)
    r = max_radius * math.pow(t, 0.6)
    
    # Surgical line weight: thinner toward the center
    ctx.set_line_width(0.3 + (t * 0.5))
    ctx.set_source_rgba(*white, 0.15 + (1-t)*0.3)
    
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Iterative Linear Segmentation (Spokes with distortion)
for j in range(spokes):
    theta = (j / spokes) * 2 * math.pi
    
    # Create gaps in the grid for rhythmic "negative space"
    if (j % 8) == 0:
        ctx.set_source_rgba(*white, 0.6)
        ctx.set_line_width(0.8)
    else:
        ctx.set_source_rgba(*white, 0.1)
        ctx.set_line_width(0.2)
        
    # Segmented lines instead of continuous strokes
    for k in range(10):
        r_start = max_radius * math.pow(k/10, 0.6)
        r_end = max_radius * math.pow((k+0.7)/10, 0.6)
        
        x1, y1 = polar_to_cartesian(r_start, theta, 0.02)
        x2, y2 = polar_to_cartesian(r_end, theta, 0.02)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

# 3. Symbolic Frequency (Glyphs at Intersections)
random.seed(42) # Deterministic randomness for systematic feel
for i in range(0, rings, 2):
    for j in range(0, spokes, 2):
        t = i / rings
        r = max_radius * math.pow(t, 0.6)
        theta = (j / spokes) * 2 * math.pi
        
        # Only draw at certain logic-based thresholds
        if random.random() > 0.85 - (t * 0.5):
            x, y = polar_to_cartesian(r, theta, 0.02)
            
            # Intersection Highlight
            if random.random() > 0.96:
                # Functional Palette: Vibrant data node
                ctx.set_source_rgb(*accent_color)
                ctx.arc(x, y, 1.5, 0, 2*math.pi)
                ctx.fill()
                
                # Extended node crosshair
                ctx.set_line_width(0.4)
                ctx.move_to(x - 5, y)
                ctx.line_to(x + 5, y)
                ctx.move_to(x, y - 5)
                ctx.line_to(x, y + 5)
                ctx.stroke()
            else:
                # Minimalist Primitive Glyph (Tiny Cross)
                ctx.set_source_rgba(*white, 0.4)
                ctx.set_line_width(0.3)
                size = 1.2
                ctx.move_to(x - size, y - size)
                ctx.line_to(x + size, y + size)
                ctx.move_to(x + size, y - size)
                ctx.line_to(x - size, y + size)
                ctx.stroke()

# 4. Global Structural Overlay (The "Swiss" Frame)
ctx.set_source_rgba(*white, 0.05)
ctx.set_line_width(0.5)
grid_size = 40
for x in range(0, width, grid_size):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
for y in range(0, height, grid_size):
    ctx.move_to(0, y)
    ctx.line_to(width, y)
    ctx.stroke()

# 5. Perimeter "Technical" Markings
for i in range(180):
    angle = (i / 180) * 2 * math.pi
    length = 5 if i % 10 == 0 else 2
    r_outer = max_radius + 15
    
    x1 = center_x + r_outer * math.cos(angle)
    y1 = center_y + r_outer * math.sin(angle)
    x2 = center_x + (r_outer + length) * math.cos(angle)
    y2 = center_y + (r_outer + length) * math.sin(angle)
    
    ctx.set_source_rgba(*white, 0.3)
    ctx.set_line_width(0.5)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

