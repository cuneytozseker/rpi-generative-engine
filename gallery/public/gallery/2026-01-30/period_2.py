import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deepest Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Helper: Polar Transformation with Radial Distortion
def get_point(r, theta, distortion_factor=0.15):
    # Center of the composition
    cx, cy = width / 2, height / 2
    
    # Apply a harmonic radial distortion to simulate "temporal flux"
    # This creates the "wobble" that deviates from perfect circles
    d = math.sin(theta * 6) * math.cos(r * 0.02) * distortion_factor * r
    r_distorted = r + d
    
    x = cx + r_distorted * math.cos(theta)
    y = cy + r_distorted * math.sin(theta)
    return x, y

def draw_curved_rect(r1, r2, a1, a2, steps=20):
    """Draws a polar 'rectangle' (an arc segment) using line segments."""
    # Outer arc
    x, y = get_point(r2, a1)
    ctx.move_to(x, y)
    for i in range(1, steps + 1):
        angle = a1 + (a2 - a1) * (i / steps)
        ctx.line_to(*get_point(r2, angle))
    
    # Side edge
    ctx.line_to(*get_point(r1, a2))
    
    # Inner arc
    for i in range(steps, -1, -1):
        angle = a1 + (a2 - a1) * (i / steps)
        ctx.line_to(*get_point(r1, angle))
    
    ctx.close_path()

def get_chromatic_color(r, theta):
    """Generates a spectral 'heat-map' color based on position."""
    # Base frequencies for RGB channels
    r_val = 0.5 + 0.5 * math.sin(r * 0.01 + theta)
    g_val = 0.3 + 0.4 * math.cos(theta * 2 - r * 0.005)
    b_val = 0.7 + 0.3 * math.sin(theta - r * 0.02)
    return r_val, g_val, b_val

def recursive_subdivide(r1, r2, a1, a2, depth):
    # Probability of subdividing decreases with depth
    if depth < 4 and random.random() > (0.2 + depth * 0.15):
        # Decide whether to split radially or angularly
        if random.random() > 0.5:
            # Radial split (Golden Ratio influence)
            mid_r = r1 + (r2 - r1) * 0.618
            recursive_subdivide(r1, mid_r, a1, a2, depth + 1)
            recursive_subdivide(mid_r, r2, a1, a2, depth + 1)
        else:
            # Angular split
            mid_a = (a1 + a2) / 2
            recursive_subdivide(r1, r2, a1, mid_a, depth + 1)
            recursive_subdivide(r1, r2, mid_a, a2, depth + 1)
    else:
        # Draw the leaf cell
        
        # 1. Draw Chromatic "Latent Volume" Slices
        # We draw multiple transparent layers with slight radius offsets
        slices = 6
        for i in range(slices):
            offset = i * 1.5
            alpha = (slices - i) / (slices * 3)
            rgb = get_chromatic_color(r1, a1)
            
            ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
            draw_curved_rect(r1 + offset, r2 - offset, a1, a2)
            ctx.fill()

        # 2. Draw Sharp Swiss Boundary
        # High contrast white/grey lines to anchor the grid
        ctx.set_source_rgba(0.9, 0.9, 0.95, 0.8)
        ctx.set_line_width(0.7)
        draw_curved_rect(r1, r2, a1, a2)
        ctx.stroke()
        
        # 3. Subtle internal accent
        if random.random() > 0.7:
            ctx.set_source_rgba(1, 1, 1, 0.4)
            ctx.set_line_width(0.3)
            # Draw a cross-hair or center line in the cell
            mr = (r1 + r2) / 2
            ma = (a1 + a2) / 2
            p1 = get_point(r1, ma)
            p2 = get_point(r2, ma)
            ctx.move_to(*p1)
            ctx.line_to(*p2)
            ctx.stroke()

# --- Execution ---

# Initialize parameters for the polar grid
rings = 5
angle_segments = 8
max_radius = 280
inner_radius = 40

# Create the initial grid cells and trigger recursion
for i in range(rings):
    for j in range(angle_segments):
        r_start = inner_radius + (i * (max_radius - inner_radius) / rings)
        r_end = inner_radius + ((i + 1) * (max_radius - inner_radius) / rings)
        
        a_start = j * (2 * math.pi / angle_segments)
        a_end = (j + 1) * (2 * math.pi / angle_segments)
        
        # Add a bit of padding for the Swiss modular feel
        padding_a = 0.02
        recursive_subdivide(r_start, r_end, a_start + padding_a, a_end - padding_a, 0)

# Add a final high-precision overlay
# Radial "ticks" like a technical instrument
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.5)
for angle in [n * (math.pi / 12) for n in range(24)]:
    p1 = get_point(inner_radius - 10, angle, 0)
    p2 = get_point(max_radius + 20, angle, 0)
    ctx.move_to(*p1)
    ctx.line_to(*p2)
    ctx.stroke()

# Central "void" structure
ctx.set_source_rgb(0, 0, 0)
ctx.arc(width/2, height/2, inner_radius - 5, 0, 2 * math.pi)
ctx.fill()
ctx.set_source_rgb(0.5, 0.5, 0.5)
ctx.set_line_width(1)
ctx.arc(width/2, height/2, inner_radius - 5, 0, 2 * math.pi)
ctx.stroke()

# Signature Swiss dot at center
ctx.set_source_rgb(1, 1, 1)
ctx.arc(width/2, height/2, 2, 0, 2 * math.pi)
ctx.fill()

