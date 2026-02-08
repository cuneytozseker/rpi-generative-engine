import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
center_x, center_y = width // 2, height // 2

# Colors - Technical Cobalt and Stark White on Deep Black
BG_COLOR = (0.02, 0.02, 0.03)
PRIMARY_COLOR = (0.95, 0.95, 0.98)
ACCENT_COLOR = (0.0, 0.3, 0.8)
HAIRLINE = 0.5
THICK = 2.5

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def polar_to_cartesian(r, theta):
    """Converts polar coordinates to cartesian with center offset."""
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return x, y

def draw_glitch_marker(x, y, size, color):
    """Draws a technical marker (cross or square) at a specific coordinate."""
    ctx.set_source_rgba(*color, 0.8)
    ctx.set_line_width(0.8)
    if random.random() > 0.5:
        # Cross
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
    else:
        # Block
        ctx.rectangle(x - size/2, y - size/2, size, size)
        ctx.fill()

# --- 1. RADIAL GRID SYSTEM ---
# Number of concentric rings and radial subdivisions
rings = 18
divisions = 64
max_radius = min(width, height) * 0.45

for i in range(rings):
    # Determine visual hierarchy of the ring
    r_base = (i / rings) * max_radius
    
    # Mathematical modulation: warp radius based on division to create "topography"
    # Uses a harmonic sin wave to create a structured distortion
    harmonic = math.sin(i * 0.5) * 10 
    
    ctx.set_line_width(HAIRLINE if i % 4 != 0 else THICK/2)
    
    for j in range(divisions):
        theta1 = (j / divisions) * 2 * math.pi
        theta2 = ((j + 1) / divisions) * 2 * math.pi
        
        # Warp the radius at this specific angle
        warp1 = math.sin(theta1 * 4 + i) * 8
        warp2 = math.sin(theta2 * 4 + i) * 8
        
        r1 = r_base + warp1 + harmonic
        r2 = r_base + warp2 + harmonic
        
        x1, y1 = polar_to_cartesian(r1, theta1)
        x2, y2 = polar_to_cartesian(r2, theta2)
        
        # Draw arc segment
        ctx.set_source_rgba(*PRIMARY_COLOR, 0.4 if i % 2 == 0 else 0.15)
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()
        
        # Occasional "Data Blobs" (rectangular substitutions)
        if (i + j) % 27 == 0:
            ctx.set_source_rgba(*ACCENT_COLOR, 0.6)
            ctx.rectangle(x1-2, y1-2, 4, 15)
            ctx.fill()

# --- 2. VECTOR FIELDS ---
# Drawing the radial "spokes" with frequency modulation
for j in range(divisions):
    if j % 2 != 0: continue # Skip every other for cleaner hierarchy
    
    theta = (j / divisions) * 2 * math.pi
    # The length of the spoke is determined by a pseudo-random but repeatable sequence
    length_mod = 0.7 + 0.3 * math.cos(j * 0.2)
    
    ctx.set_source_rgba(*PRIMARY_COLOR, 0.1)
    ctx.set_line_width(HAIRLINE)
    
    x_start, y_start = polar_to_cartesian(max_radius * 0.1, theta)
    x_end, y_end = polar_to_cartesian(max_radius * length_mod, theta)
    
    ctx.move_to(x_start, y_start)
    ctx.line_to(x_end, y_end)
    ctx.stroke()
    
    # Add coordinates/dots at the ends of spokes
    if j % 8 == 0:
        draw_glitch_marker(x_end, y_end, 3, PRIMARY_COLOR)

# --- 3. OVERLAY: ASYMMETRICAL DATA BLOCKS ---
# Creating 'brutalist' noise clusters
for _ in range(12):
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(max_radius * 0.3, max_radius * 1.1)
    bx, by = polar_to_cartesian(dist, angle)
    
    # Create horizontal/vertical emphasis typical of Swiss Design
    w = random.choice([20, 40, 80])
    h = 2
    ctx.set_source_rgba(*ACCENT_COLOR, 0.4)
    ctx.rectangle(bx, by, w, h)
    ctx.fill()
    
    # Smaller technical dots
    ctx.set_source_rgb(*PRIMARY_COLOR)
    ctx.arc(bx, by, 1, 0, 2*math.pi)
    ctx.fill()

# --- 4. CENTERPIECE ---
# High contrast core
ctx.set_source_rgb(*BG_COLOR)
ctx.arc(center_x, center_y, 15, 0, 2*math.pi)
ctx.fill()
ctx.set_source_rgb(*ACCENT_COLOR)
ctx.set_line_width(2)
ctx.arc(center_x, center_y, 15, 0, 2*math.pi)
ctx.stroke()

# Crosshair
ctx.set_source_rgb(*PRIMARY_COLOR)
ctx.set_line_width(0.5)
ctx.move_to(center_x - 30, center_y)
ctx.line_to(center_x + 30, center_y)
ctx.move_to(center_x, center_y - 30)
ctx.line_to(center_x, center_y + 30)
ctx.stroke()

# Border framing (Swiss precision)
ctx.set_source_rgba(*PRIMARY_COLOR, 0.1)
ctx.set_line_width(1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Corner accents
for (cx, cy) in [(margin, margin), (width-margin, margin), (margin, height-margin), (width-margin, height-margin)]:
    ctx.set_source_rgb(*ACCENT_COLOR)
    ctx.rectangle(cx-5, cy-1, 10, 2)
    ctx.rectangle(cx-1, cy-5, 2, 10)
    ctx.fill()

