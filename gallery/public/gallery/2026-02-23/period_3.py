import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_DEPTH = 5
SUBDIVISION_CHANCE = 0.7
INNER_RADIUS = 40
OUTER_RADIUS = 280

# Colors: Swiss-inspired Palette
COLORS = [
    (0.95, 0.95, 0.95, 0.8),  # Stark White
    (0.95, 0.95, 0.95, 0.4),  # Faded White
    (0.12, 0.47, 0.49, 0.7),  # Muted Teal
    (0.82, 0.58, 0.23, 0.7),  # Ochre
    (0.45, 0.52, 0.58, 0.6),  # Slate
]

def project(u, v, distortion_factor=1.0):
    """
    Maps normalized coordinates (u, v) [0, 1] to a polar space with radial distortion.
    u: corresponds to angular position
    v: corresponds to radial distance
    """
    # Map u to 0-2π with a slight twist
    angle = u * 2 * math.pi
    
    # Map v to radius with an exponential push for "explosive" center
    base_r = INNER_RADIUS + (v ** 1.2) * (OUTER_RADIUS - INNER_RADIUS)
    
    # Radial distortion based on harmonics
    distortion = math.sin(angle * 8) * 5 * distortion_factor
    distortion += math.cos(angle * 3 + v * 10) * 8 * distortion_factor
    
    r = base_r + distortion
    
    x = CENTER_X + r * math.cos(angle)
    y = CENTER_Y + r * math.sin(angle)
    return x, y

def draw_distorted_rect(u, v, uw, vh, color):
    """Draws a 'rectangle' in polar space by interpolating its edges."""
    ctx.set_source_rgba(*color)
    ctx.set_line_width(0.5 + (1.0 - v) * 1.5)
    
    segments = 15
    
    # Draw path
    # Top edge
    p1 = project(u, v)
    ctx.move_to(*p1)
    for i in range(1, segments + 1):
        ctx.line_to(*project(u + (i/segments)*uw, v))
    
    # Right edge
    for i in range(1, segments + 1):
        ctx.line_to(*project(u + uw, v + (i/segments)*vh))
        
    # Bottom edge
    for i in range(1, segments + 1):
        ctx.line_to(*project(u + uw - (i/segments)*uw, v + vh))
        
    # Left edge
    for i in range(1, segments + 1):
        ctx.line_to(*project(u, v + vh - (i/segments)*vh))
    
    ctx.close_path()
    
    # High frequency repetition for texture
    if random.random() > 0.4:
        ctx.stroke()
    else:
        ctx.fill()

def subdivide(u, v, uw, vh, depth):
    """Recursive quadtree subdivision creating a hierarchical grid."""
    # Determine subdivision based on depth and proximity to "focal" radius
    dist_to_mid = abs(v - 0.5)
    local_chance = SUBDIVISION_CHANCE - (depth * 0.1) + (0.3 * (1.0 - dist_to_mid))
    
    if depth < MAX_DEPTH and random.random() < local_chance:
        half_uw = uw / 2
        half_vh = vh / 2
        subdivide(u, v, half_uw, half_vh, depth + 1)
        subdivide(u + half_uw, v, half_uw, half_vh, depth + 1)
        subdivide(u, v + half_vh, half_uw, half_vh, depth + 1)
        subdivide(u + half_uw, v + half_vh, half_uw, half_vh, depth + 1)
    else:
        # Choose color based on radial distance v
        if random.random() > 0.85:
            color = random.choice(COLORS[2:]) # Accents
        else:
            color = COLORS[0] if random.random() > 0.5 else COLORS[1]
            
        draw_distorted_rect(u, v, uw, vh, color)

# --- Execution ---

# 1. Background Grid - Low contrast filigree
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.05)
for i in range(40):
    r = INNER_RADIUS + (i/40) * (OUTER_RADIUS - INNER_RADIUS)
    ctx.arc(CENTER_X, CENTER_Y, r, 0, 2 * math.pi)
    ctx.stroke()

# 2. Main Recursive Structure
# We start with 8 primary segments to ensure a circular base
num_sectors = 12
for i in range(num_sectors):
    subdivide(i/num_sectors, 0.1, 1/num_sectors, 0.8, 0)

# 3. Vector Field "Debris" 
# Adding digital grain/filigree through scattered tiny segments
for _ in range(200):
    u = random.random()
    v = random.uniform(0.1, 0.9)
    x, y = project(u, v, distortion_factor=2.0)
    
    length = random.uniform(2, 15)
    angle = math.atan2(y - CENTER_Y, x - CENTER_X) + math.pi/2
    
    ctx.set_source_rgba(0.9, 0.9, 0.9, random.uniform(0.1, 0.5))
    ctx.set_line_width(random.uniform(0.1, 0.8))
    
    ctx.move_to(x, y)
    ctx.line_to(x + math.cos(angle) * length, y + math.sin(angle) * length)
    ctx.stroke()

# 4. Final Polish: Central "Structural" Core
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.arc(CENTER_X, CENTER_Y, INNER_RADIUS - 5, 0, 2 * math.pi)
ctx.fill()

ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.set_line_width(1.0)
ctx.arc(CENTER_X, CENTER_Y, INNER_RADIUS - 5, 0, 2 * math.pi)
ctx.stroke()

# Crosshair / Swiss mark in center
cs = 5
ctx.move_to(CENTER_X - cs, CENTER_Y)
ctx.line_to(CENTER_X + cs, CENTER_Y)
ctx.move_to(CENTER_X, CENTER_Y - cs)
ctx.line_to(CENTER_X, CENTER_Y + cs)
ctx.stroke()

# Final border to emphasize the frame
ctx.set_source_rgb(0.95, 0.95, 0.95)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
