import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format works best for polar transformations
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal/Midnight Blue
ctx.set_source_rgb(0.05, 0.07, 0.1) 
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
num_rings = 80
num_spokes = 120
phi = (1 + 5**0.5) / 2 # Golden ratio for spacing

def get_distorted_point(r, theta, intensity=1.0):
    """Applies radial distortion based on trigonometric harmonics."""
    # Create a topographical 'ripple' effect
    ripple = math.sin(theta * 3) * 15 * intensity
    wave = math.cos(theta * 7 + (r * 0.05)) * 10 * intensity
    
    distorted_r = r + ripple + wave
    
    x = center_x + distorted_r * math.cos(theta)
    y = center_y + distorted_r * math.sin(theta)
    return x, y

# 1. LAYER: Ultra-fine filament moiré
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.15) # Faint white

for i in range(num_rings):
    r = (i / num_rings) * max_radius
    ctx.new_path()
    for step in range(361):
        angle = math.radians(step)
        # Higher frequency distortion for outer rings
        distortion_scale = (i / num_rings) ** 2
        px, py = get_distorted_point(r, angle, distortion_scale)
        if step == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.stroke()

# 2. LAYER: Structural Radial Spokes (Informational Asymmetry)
# We only draw spokes in specific angular sectors to create 'voids'
ctx.set_line_width(0.5)
for j in range(num_spokes):
    angle = (j / num_spokes) * 2 * math.pi
    
    # Use probability and sine modulation to create clusters of data
    density_mask = math.sin(angle * 3) * math.cos(angle * 2)
    if density_mask > -0.2:
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.4)
        
        # Draw fragmented lines instead of continuous spokes
        start_r = max_radius * 0.1
        segments = 5
        for s in range(segments):
            r1 = start_r + (max_radius * 0.85 / segments) * s
            r2 = r1 + (max_radius * 0.2 / segments) * random.random()
            
            p1x, p1y = get_distorted_point(r1, angle, (r1/max_radius))
            p2x, p2y = get_distorted_point(r2, angle, (r2/max_radius))
            
            ctx.move_to(p1x, p1y)
            ctx.line_to(p2x, p2y)
            ctx.stroke()

# 3. LAYER: Technical Glyphs (Nodes)
# Placing small markers at intersections of the Swiss-Polar grid
ctx.set_line_width(1.0)
for i in range(0, num_rings, 8):
    for j in range(0, num_spokes, 12):
        r = (i / num_rings) * max_radius
        angle = (j / num_spokes) * 2 * math.pi
        
        px, py = get_distorted_point(r, angle, (r/max_radius))
        
        # Systematic variation of glyphs
        glyph_type = (i + j) % 3
        ctx.set_source_rgba(1, 1, 1, 0.8)
        
        if glyph_type == 0: # Small Cross
            size = 2
            ctx.move_to(px - size, py)
            ctx.line_to(px + size, py)
            ctx.move_to(px, py - size)
            ctx.line_to(px, py + size)
            ctx.stroke()
        elif glyph_type == 1: # Open Circle
            ctx.arc(px, py, 1.5, 0, 2 * math.pi)
            ctx.stroke()
        else: # Highlighted Node
            ctx.arc(px, py, 0.8, 0, 2 * math.pi)
            ctx.fill()

# 4. LAYER: Peripheral Accents (Swiss Typography/Data Logic)
# Draw tiny concentric dashed rings at the edge to frame the topography
ctx.set_dash([1, 4])
ctx.set_line_width(0.3)
ctx.set_source_rgba(1, 1, 1, 0.5)
for r_ext in [max_radius * 1.05, max_radius * 1.08]:
    ctx.arc(center_x, center_y, r_ext, 0, 2 * math.pi)
    ctx.stroke()

# Reset dash
ctx.set_dash([])

# 5. LAYER: Golden Ratio Guides (Implicit Structure)
# Faint arcs following a fibonacci progression
ctx.set_source_rgba(0.4, 0.5, 1.0, 0.2) # Tech Blue tint
curr_r = 10
for _ in range(8):
    ctx.arc(center_x, center_y, curr_r, 0, math.pi * 0.5)
    ctx.stroke()
    curr_r *= phi

# Final Touch: A subtle "radar" sweep line
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.move_to(center_x, center_y)
ctx.line_to(center_x + max_radius * 1.2, center_y - max_radius * 0.3)
ctx.stroke()
