import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Constants
CX, CY = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
SIDES = 12  # Base grid divisions
RINGS = 10  # Radial subdivisions

def get_polar_coords(r, theta, entropy=0):
    """Calculates coordinates with a distortion factor based on radius."""
    # Entropy increases as we move away from the center
    distort = (r / MAX_RADIUS) ** 2 * entropy
    r_distorted = r + random.uniform(-distort, distort) * 10
    theta_distorted = theta + random.uniform(-distort, distort) * 0.2
    
    x = CX + r_distorted * math.cos(theta_distorted)
    y = CY + r_distorted * math.sin(theta_distorted)
    return x, y

def draw_subdivided_arc(r, theta, dr, dt, depth, entropy):
    """Recursively draws blocks or subdivisions to create geometric hierarchy."""
    if depth > 0 and (random.random() > 0.4 or depth > 2):
        # Subdivide into 4 quadrants
        half_r = dr / 2
        half_t = dt / 2
        for i in range(2):
            for j in range(2):
                draw_subdivided_arc(r + i * half_r, theta + j * half_t, half_r, half_t, depth - 1, entropy)
    else:
        # Render the leaf cell
        # Calculate corners with distortion
        points = [
            get_polar_coords(r, theta, entropy),
            get_polar_coords(r + dr, theta, entropy),
            get_polar_coords(r + dr, theta + dt, entropy),
            get_polar_coords(r, theta + dt, entropy)
        ]
        
        # Chromatic Interference: slight shifts in RGB based on position
        interference = (r / MAX_RADIUS)
        r_col = 0.9 + 0.1 * math.sin(theta * 3)
        g_col = 0.9 + 0.1 * math.cos(r * 0.05)
        b_col = 1.0
        
        # Base alpha modulated by entropy
        alpha = max(0.1, 0.8 - (r / MAX_RADIUS) * 0.5)
        
        # Draw the main block
        ctx.move_to(points[0][0], points[0][1])
        for p in points[1:]:
            ctx.line_to(p[0], p[1])
        ctx.close_path()
        
        # Fill with volumetric gradient look
        if random.random() > 0.3:
            ctx.set_source_rgba(r_col, g_col, b_col, alpha * 0.2)
            ctx.fill_preserve()
            
        # Stroke with "data-point" precision
        ctx.set_line_width(0.4 if r < MAX_RADIUS * 0.5 else 0.2)
        ctx.set_source_rgba(r_col, g_col, b_col, alpha)
        ctx.stroke()
        
        # Spectral Dispersion (the "Chromatic Interference")
        if entropy > 0.5 and random.random() > 0.8:
            offset = 2 * entropy
            ctx.set_source_rgba(1, 0, 0.4, alpha * 0.4) # Magenta shift
            ctx.move_to(points[0][0] + offset, points[0][1])
            for p in points[1:]:
                ctx.line_to(p[0] + offset, p[1])
            ctx.stroke()

# --- Execution ---

# 1. Background Grid (The rigid Swiss foundation)
ctx.set_line_width(0.1)
ctx.set_source_rgba(1, 1, 1, 0.1)
for i in range(24):
    angle = (i / 24) * math.pi * 2
    ctx.move_to(CX, CY)
    ctx.line_to(CX + MAX_RADIUS * 1.2 * math.cos(angle), CY + MAX_RADIUS * 1.2 * math.sin(angle))
    ctx.stroke()

# 2. Recursive Polar Composition
random.seed(42) # For consistent entropy patterns
dr = MAX_RADIUS / RINGS
dt = (math.pi * 2) / SIDES

for ring in range(RINGS):
    for sector in range(SIDES):
        r_start = ring * dr
        t_start = sector * dt
        
        # Increase entropy as we move outwards
        entropy_level = (ring / RINGS) ** 1.5
        
        # The core logic: recursive subdivision of the polar grid
        draw_subdivided_arc(r_start, t_start, dr, dt, depth=3, entropy=entropy_level)

# 3. Floating "Data Points" / Staccato Punctuation
for _ in range(200):
    r = random.uniform(0, MAX_RADIUS * 1.1)
    theta = random.uniform(0, math.pi * 2)
    entropy = (r / MAX_RADIUS) ** 2
    x, y = get_polar_coords(r, theta, entropy)
    
    size = random.uniform(0.5, 2.0)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.2, 0.8))
    ctx.arc(x, y, size, 0, math.pi * 2)
    ctx.fill()

# 4. Central Core - The point of absolute rigidity
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.arc(CX, CY, 3, 0, math.pi * 2)
ctx.fill()

# 5. Overlapping Spectral Wash (Volumetric Depth)
# Create a subtle radial gradient to simulate light dispersion
lg = cairo.RadialGradient(CX, CY, 0, CX, CY, MAX_RADIUS * 1.2)
lg.add_color_stop_rgba(0, 0, 0, 0, 0)
lg.add_color_stop_rgba(0.7, 0.1, 0.3, 0.5, 0.05) # Subtle cyan/magenta haze
lg.add_color_stop_rgba(1, 0, 0, 0, 0.2)
ctx.set_source(lg)
ctx.paint()

