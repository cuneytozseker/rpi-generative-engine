import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

def polar_to_cartesian(cx, cy, r, angle):
    """Converts polar coordinates to screen space."""
    return cx + r * math.cos(angle), cy + r * math.sin(angle)

def draw_cross(x, y, size, weight):
    """Draws a Swiss-style cross node."""
    ctx.set_line_width(weight)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# Parameters for the Structured Entropy system
center_x, center_y = width * 0.45, height * 0.5  # Slightly off-center for asymmetric balance
rings = 36
segments = 72
max_radius = min(width, height) * 0.8
entropy_threshold = 0.4  # At what radius the 'order' begins to fragment

# --- LAYER 1: The Underlying Web (Structural Hairlines) ---
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.3)

for r_idx in range(rings):
    r = (r_idx / rings) * max_radius
    
    # Calculate radial distortion based on distance from center
    # Greater distance = higher stochastic displacement
    distortion_factor = math.pow(r_idx / rings, 2.5) * 40
    
    for s_idx in range(segments):
        angle = (s_idx / segments) * (2 * math.pi)
        
        # Stochastic displacement
        off_r = r + (random.uniform(-1, 1) * distortion_factor)
        off_a = angle + (random.uniform(-0.02, 0.02) * distortion_factor * 0.1)
        
        x, y = polar_to_cartesian(center_x, center_y, off_r, off_a)
        
        if s_idx == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
            
    ctx.close_path()
    ctx.stroke()

# --- LAYER 2: Recursive Displacement Nodes ---
# Building perceived volume through high-frequency primitives
for r_idx in range(0, rings, 2):
    r = (r_idx / rings) * max_radius
    density_mod = 1.0 - (r_idx / rings) # Denser at the core
    
    for s_idx in range(segments):
        # Skip some segments randomly to create negative space "cracks"
        if random.random() > (0.2 + density_mod * 0.6):
            continue
            
        angle = (s_idx / segments) * (2 * math.pi)
        
        # Apply a "glitch" shift to certain coordinates
        shift = 0
        if random.random() > 0.92:
            shift = random.uniform(10, 30)
            
        # Recursive mapping: distort the position based on its own angle
        distorted_r = r + (math.sin(angle * 8) * 10) + shift
        x, y = polar_to_cartesian(center_x, center_y, distorted_r, angle)
        
        # Visual Hierarchy: Inner elements are sharper/thicker
        opacity = 0.2 + (density_mod * 0.6)
        line_w = 0.5 + (density_mod * 1.5)
        
        ctx.set_source_rgba(1, 1, 1, opacity)
        
        # Draw technical markers (ticks and crosses)
        draw_cross(x, y, 2 + (1-density_mod)*3, line_w)
        
        # Connect to neighbor with a faint "mapping" line
        if random.random() > 0.7:
            x2, y2 = polar_to_cartesian(center_x, center_y, distorted_r + 20, angle + 0.1)
            ctx.set_line_width(0.2)
            ctx.move_to(x, y)
            ctx.line_to(x2, y2)
            ctx.stroke()

# --- LAYER 3: Focal Accents (The "Brutalist" Weight) ---
ctx.set_source_rgba(1, 1, 1, 0.9)
for _ in range(12):
    # Select a random sector to emphasize
    rand_r = random.uniform(0.1, 0.5) * max_radius
    rand_a = random.uniform(0, 2 * math.pi)
    x, y = polar_to_cartesian(center_x, center_y, rand_r, rand_a)
    
    # Heavy rectangular modules representing "information clusters"
    ctx.rectangle(x, y, random.uniform(5, 15), 1)
    ctx.fill()
    
    # Vertical "signal" lines
    ctx.set_line_width(0.5)
    ctx.move_to(x, y - 40)
    ctx.line_to(x, y + 40)
    ctx.stroke()

# --- LAYER 4: The Outer Dissolve (Optical Mixing) ---
ctx.set_source_rgba(1, 1, 1, 0.4)
for i in range(400):
    # Scatter dots and tiny strokes in the outer reaches
    dist = random.uniform(0.6, 1.1) * max_radius
    ang = random.uniform(0, 2 * math.pi)
    x, y = polar_to_cartesian(center_x, center_y, dist, ang)
    
    size = random.uniform(0.5, 1.5)
    ctx.arc(x, y, size, 0, 2 * math.pi)
    ctx.fill()

# --- FINISHING: Global Grid Overlay (Swiss Precision) ---
# A very faint subtle primary grid to ground the chaos
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.5)
grid_size = 40
for i in range(0, width, grid_size):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
for j in range(0, height, grid_size):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
ctx.stroke()

