import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep void for contrast
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def get_spectral_color(t, alpha=1.0):
    """Returns a thermal-map inspired color based on a 0.0-1.0 input."""
    # Transitions: Deep Purple -> Cyan -> Green -> Yellow -> Red
    r = math.pow(t, 1.5) * 1.2
    g = 0.5 * math.sin(t * math.pi) + (0.2 if t > 0.5 else 0.0)
    b = math.cos(t * math.pi * 0.5)
    return (min(r, 1.0), min(g, 1.0), min(b, 1.0), alpha)

def draw_symbol(ctx, x, y, size, type_roll, color):
    ctx.set_source_rgba(*color)
    ctx.set_line_width(0.5)
    if type_roll < 0.7:  # Staccato Dot
        ctx.arc(x, y, size * 0.15, 0, 2 * math.pi)
        ctx.fill()
    elif type_roll < 0.9:  # Precision Cross
        ext = size * 0.3
        ctx.move_to(x - ext, y)
        ctx.line_to(x + ext, y)
        ctx.move_to(x, y - ext)
        ctx.line_to(x, y + ext)
        ctx.stroke()
    else:  # Open Circle
        ctx.arc(x, y, size * 0.4, 0, 2 * math.pi)
        ctx.stroke()

# Parameters
cx, cy = width / 2, height / 2
rings = 24
sectors = 72
max_radius = min(width, height) * 0.45

# Create a distorted polar grid
points = []
for r_idx in range(rings):
    ring_points = []
    # Progressive scaling of radius (logarithmic expansion)
    norm_r = r_idx / rings
    base_radius = math.pow(norm_r, 1.2) * max_radius
    
    for s_idx in range(sectors):
        # Angular distortion: push points based on a harmonic function
        angle = (s_idx / sectors) * 2 * math.pi
        distortion = 15 * math.sin(angle * 6 + norm_r * 5)
        
        curr_r = base_radius + distortion
        x = cx + curr_r * math.cos(angle)
        y = cy + curr_r * math.sin(angle)
        ring_points.append((x, y, norm_r, angle))
    points.append(ring_points)

# 1. Atmospheric Blur Layer (Thermal Underglow)
ctx.set_operator(cairo.OPERATOR_ADD)
for r_idx in range(1, rings):
    for s_idx in range(sectors):
        x, y, norm_r, angle = points[r_idx][s_idx]
        color = get_spectral_color(norm_r, 0.05)
        ctx.set_source_rgba(*color)
        ctx.arc(x, y, norm_r * 25, 0, 2 * math.pi)
        ctx.fill()
ctx.set_operator(cairo.OPERATOR_OVER)

# 2. Filigree Networking (Radial point-to-point)
ctx.set_line_width(0.3)
for r_idx in range(rings - 1):
    for s_idx in range(sectors):
        p1 = points[r_idx][s_idx]
        p2 = points[r_idx + 1][s_idx] # Radial connection
        p3 = points[r_idx][(s_idx + 1) % sectors] # Circumferential connection
        
        color = get_spectral_color(p1[2], 0.4)
        ctx.set_source_rgba(*color)
        
        # Draw mesh
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p2[0], p2[1])
        ctx.move_to(p1[0], p1[1])
        ctx.line_to(p3[0], p3[1])
        ctx.stroke()
        
        # Create "Long Vectors" - networking across gaps
        if (r_idx + s_idx) % 17 == 0:
            p_far = points[min(r_idx + 4, rings-1)][(s_idx + 3) % sectors]
            ctx.set_source_rgba(*get_spectral_color(p1[2], 0.2))
            ctx.move_to(p1[0], p1[1])
            ctx.line_to(p_far[0], p_far[1])
            ctx.stroke()

# 3. Micro-level Symbol Grid
random.seed(42) # Deterministic randomness for structure
for r_idx in range(0, rings, 2):
    for s_idx in range(0, sectors, 2):
        x, y, norm_r, _ = points[r_idx][s_idx]
        
        # Scale symbols by their distance from center
        symbol_size = 4 + (norm_r * 12)
        type_roll = random.random()
        
        # Highlight color for the symbols
        symbol_color = get_spectral_color(norm_r, 0.8)
        draw_symbol(ctx, x, y, symbol_size, type_roll, symbol_color)

# 4. Global Swiss Accents (Horizontal and Vertical "Scanners")
ctx.set_line_width(0.5)
for i in range(5):
    y_pos = (height / 6) * (i + 1)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(40, y_pos)
    ctx.line_to(width - 40, y_pos)
    ctx.stroke()
    
    # Small tick marks on the axis
    for x_tick in range(50, width-40, 40):
        ctx.move_to(x_tick, y_pos - 3)
        ctx.line_to(x_tick, y_pos + 3)
        ctx.stroke()

# Final Polish: Center Core
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.arc(cx, cy, 2, 0, 2 * math.pi)
ctx.fill()

# Border frame for Swiss aesthetic
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.rectangle(20, 20, width - 40, height - 40)
ctx.stroke()

