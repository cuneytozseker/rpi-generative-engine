import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Black for Binary Tension
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 45
segments = 120
max_radius = min(width, height) * 0.45

def polar_to_cartesian(r, theta, distortion_factor=0):
    """Maps polar coordinates to cartesian with radial modulation."""
    # Apply a non-linear radial distortion (Harmonic oscillation)
    r_mod = r + (math.sin(theta * 6) * distortion_factor)
    x = center_x + r_mod * math.cos(theta)
    y = center_y + r_mod * math.sin(theta)
    return x, y

# --- LAYER 1: The Underlying Lattice (Vector Interconnectivity) ---
ctx.set_line_width(0.15)
ctx.set_source_rgba(0.8, 0.8, 0.9, 0.3)

for i in range(rings):
    r = (i / rings) * max_radius
    # Variable distortion based on depth
    distort = math.sin(i * 0.2) * 15
    
    ctx.new_path()
    for j in range(segments + 1):
        theta = (j / segments) * 2 * math.pi
        px, py = polar_to_cartesian(r, theta, distort)
        if j == 0:
            ctx.move_to(px, py)
        else:
            ctx.line_to(px, py)
    ctx.stroke()

# --- LAYER 2: Radial Dispersion & Density Gradients ---
# Drawing "spokes" that modulate width to create visual weight
for j in range(0, segments, 2):
    theta = (j / segments) * 2 * math.pi
    
    # Logical fragmentation: some spokes are solid, some are dashed/systematic
    style_seed = random.random()
    
    ctx.new_path()
    for i in range(rings):
        r = (i / rings) * max_radius
        distort = math.sin(i * 0.2) * 15
        px, py = polar_to_cartesian(r, theta, distort)
        
        if i == 0:
            ctx.move_to(px, py)
        else:
            # High-density optical interference: modulate line weight by radius
            ctx.set_line_width(0.2 + (i / rings) * 0.8)
            ctx.line_to(px, py)
            
    if style_seed > 0.4:
        ctx.set_source_rgba(1, 1, 1, 0.6)
        ctx.stroke()
    else:
        # Binary Tension: Leaving gaps or using dots
        ctx.set_dash([1, 4])
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.stroke()
        ctx.set_dash([])

# --- LAYER 3: Conditional Primitive Replacement (The "Digital Brutalism") ---
# Adding structural glyphs at intersection points based on mathematical triggers
for i in range(5, rings, 4):
    r = (i / rings) * max_radius
    distort = math.sin(i * 0.2) * 15
    
    for j in range(0, segments, 6):
        theta = (j / segments) * 2 * math.pi
        px, py = polar_to_cartesian(r, theta, distort)
        
        # Systematic variation: Golden ratio logic for scale
        phi = (1 + 5**0.5) / 2
        size = (i / rings) * 6 * phi
        
        ctx.save()
        ctx.translate(px, py)
        ctx.rotate(theta)
        
        # Binary selection of geometric primitives
        if (i + j) % 3 == 0:
            # Sharp Rectangles (Swiss precision)
            ctx.set_source_rgb(1, 1, 1)
            ctx.rectangle(-size/2, -0.5, size, 1)
            ctx.fill()
        elif (i * j) % 7 == 0:
            # Concentric Optical Interference Ticks
            ctx.set_source_rgb(0.9, 0.9, 1.0)
            ctx.set_line_width(0.5)
            ctx.move_to(0, -size)
            ctx.line_to(0, size)
            ctx.stroke()
            
        ctx.restore()

# --- LAYER 4: Topo-Mapping Shadows & Moire Effects ---
# A secondary offset grid to create perceived depth
ctx.set_source_rgba(0.5, 0.6, 1.0, 0.1) # Subtle blue tint
ctx.set_line_width(0.1)
for i in range(10, rings, 2):
    r = (i / rings) * max_radius * 1.02 # Slight expansion
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

# --- FINAL ACCENT: Centrifugal Focus ---
# Highlight the core where the system originates
ctx.set_source_rgb(1, 1, 1)
ctx.arc(center_x, center_y, 2, 0, 2 * math.pi)
ctx.fill()

# Draw a framing border to emphasize the grid-based construction
ctx.set_line_width(20)
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Subtle Swiss-style framing lines (the 'Technical' border)
ctx.set_line_width(0.5)
ctx.set_source_rgb(0.4, 0.4, 0.4)
ctx.move_to(40, 40)
ctx.line_to(width-40, 40)
ctx.move_to(40, height-40)
ctx.line_to(width-40, height-40)
ctx.stroke()

