import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for a Swiss-industrial feel
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Constants for the composition
center_x, center_y = width / 2, height / 2
rings = 60
slices = 90
max_radius = min(width, height) * 0.45

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to cartesian, applying a systemic distortion field."""
    # Modulate radius based on angular position to create 'valleys' and 'peaks'
    # Frequency interference creates rhythmic distortion
    distortion = 15 * math.sin(theta * 6) * math.cos(theta * 3)
    # Secondary wave for organic emergence
    distortion += 8 * math.sin(theta * 12 + r * 0.05)
    
    adjusted_r = r + distortion
    x = center_x + adjusted_r * math.cos(theta)
    y = center_y + adjusted_r * math.sin(theta)
    return x, y

# 1. LAYER ONE: The Underlying Grid Structure (Low contrast, structural)
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.4, 0.4, 0.4, 0.3)

for r_idx in range(rings):
    r = (r_idx / rings) * max_radius
    ctx.new_path()
    for s_idx in range(slices + 1):
        theta = (s_idx / slices) * (2 * math.pi)
        x, y = polar_to_cartesian(r, theta)
        if s_idx == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# 2. LAYER TWO: Radial Progression and Optical Mixing
# This creates the "directional progression" from the core outward
for s_idx in range(slices):
    theta = (s_idx / slices) * (2 * math.pi)
    
    # Line width increases with radius to simulate kinetic expansion
    for r_idx in range(0, rings - 5, 2):
        r1 = (r_idx / rings) * max_radius
        r2 = ((r_idx + 4) / rings) * max_radius
        
        x1, y1 = polar_to_cartesian(r1, theta)
        x2, y2 = polar_to_cartesian(r2, theta)
        
        # Modulation of weight based on angular position (Brutalist hierarchy)
        weight = 0.3 + (math.sin(theta * 4) + 1) * 0.5
        ctx.set_line_width(weight)
        
        # Color gradient: White to a technical Blue/Cyan
        intensity = (r_idx / rings)
        ctx.set_source_rgba(0.8 + 0.2 * intensity, 0.8 + 0.1 * intensity, 0.9, 0.6)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

# 3. LAYER THREE: Emergent Interference (Moiré pattern logic)
# A slightly offset grid creates visual vibration
ctx.set_source_rgba(1.0, 0.2, 0.1, 0.7) # Swiss Red accent
ctx.set_line_width(1.2)

for s_idx in range(0, slices, 10):
    theta = (s_idx / slices) * (2 * math.pi)
    # Only draw specific 'emergent' nodes
    for r_idx in [rings // 3, rings // 2, (rings * 2) // 3]:
        r = (r_idx / rings) * max_radius
        x, y = polar_to_cartesian(r, theta)
        
        # Draw technical cross-hairs at intersection points
        size = 4
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()

# 4. LAYER FOUR: Recursive Outer Edge
# Dense, high-frequency lines at the perimeter to anchor the composition
ctx.set_source_rgba(1, 1, 1, 0.15)
for s_idx in range(slices * 2):
    theta = (s_idx / (slices * 2)) * (2 * math.pi)
    r_start = max_radius * 0.95
    r_end = max_radius * (1.0 + 0.05 * math.sin(theta * 20))
    
    x1, y1 = polar_to_cartesian(r_start, theta)
    x2, y2 = polar_to_cartesian(r_end, theta)
    
    ctx.set_line_width(0.5)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 5. FINAL TOUCH: Negative Space Management
# Centered geometric punch-out to enforce the radial hierarchy
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.arc(center_x, center_y, 20, 0, 2 * math.pi)
ctx.fill()

ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.arc(center_x, center_y, 5, 0, 2 * math.pi)
ctx.stroke()

# Add a subtle "data" line (Swiss design element)
ctx.set_source_rgba(1, 1, 1, 0.5)
ctx.set_line_width(0.5)
ctx.move_to(width * 0.05, height * 0.9)
ctx.line_to(width * 0.95, height * 0.9)
ctx.stroke()

# Small coordinate ticks
for i in range(10):
    tx = width * 0.05 + (i * width * 0.1)
    ctx.move_to(tx, height * 0.9)
    ctx.line_to(tx, height * 0.91)
    ctx.stroke()

