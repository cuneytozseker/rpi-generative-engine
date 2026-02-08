import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Warm, neutral "paper" ground
ctx.set_source_rgb(0.96, 0.95, 0.92)
ctx.paint()

# Constants
center_x, center_y = width // 2, height // 2
num_rings = 45
num_spokes = 80
max_radius = min(width, height) * 0.45

def get_polar_pos(r, theta, distortion=0):
    """Calculates x, y with a radial distortion based on harmonic frequencies."""
    # Radial distortion mimics "organic erosion" or wave interference
    r_mod = r + distortion * math.sin(theta * 5 + r * 0.05) * 15
    r_mod += distortion * math.cos(theta * 12 - r * 0.02) * 5
    
    x = center_x + r_mod * math.cos(theta)
    y = center_y + r_mod * math.sin(theta)
    return x, y

# 1. THE RADIAL GRID (Swiss Structuralism)
# Layering multiple passes with varying line weights for depth
for pass_idx in range(3):
    ctx.set_line_width(0.2 if pass_idx == 0 else 0.5)
    
    # RINGS (Horizontal Grid Lines in Polar)
    for i in range(num_rings):
        r = (i / num_rings) * max_radius
        # Progressive alpha: clearer at the edges, denser in the center
        alpha = 0.1 + (i / num_rings) * 0.4
        ctx.set_source_rgba(0.1, 0.1, 0.1, alpha)
        
        ctx.move_to(*get_polar_pos(r, 0, distortion=pass_idx))
        steps = 200
        for s in range(steps + 1):
            theta = (s / steps) * 2 * math.pi
            # Systematic "Erosion": occasionally skip segments
            if random.random() > 0.02:
                ctx.line_to(*get_polar_pos(r, theta, distortion=pass_idx))
            else:
                ctx.move_to(*get_polar_pos(r, theta, distortion=pass_idx))
        ctx.stroke()

    # SPOKES (Vertical Grid Lines in Polar)
    for j in range(num_spokes):
        theta = (j / num_spokes) * 2 * math.pi
        ctx.set_source_rgba(0.1, 0.1, 0.1, 0.2)
        
        ctx.move_to(*get_polar_pos(0, theta))
        # Draw spokes with segmented distortion
        for r_step in range(0, int(max_radius), 5):
            # Directional momentum: spokes curve slightly
            local_theta = theta + (r_step / max_radius) * 0.5
            ctx.line_to(*get_polar_pos(r_step, local_theta, distortion=pass_idx * 0.5))
        ctx.stroke()

# 2. SPECTRAL NOISE (Accents)
# Small geometric primitives mapped to the field
colors = [(0.9, 0.2, 0.2), (0.1, 0.4, 0.8), (0.9, 0.7, 0.1)] # Red, Blue, Gold
for _ in range(120):
    r = random.uniform(20, max_radius)
    theta = random.uniform(0, 2 * math.pi)
    x, y = get_polar_pos(r, theta, distortion=1.0)
    
    # Choose a "spectral" color
    ctx.set_source_rgba(*random.choice(colors), random.uniform(0.6, 0.9))
    
    # Draw "glyphs" (small rectangles or dots)
    size = random.uniform(1, 4)
    if random.random() > 0.5:
        ctx.rectangle(x - size/2, y - size/2, size, size)
    else:
        ctx.arc(x, y, size/2, 0, 2 * math.pi)
    ctx.fill()

# 3. EMERGENT CONNECTIVITY (Digital Fabric)
# Connect random nodes within the grid to create skeletal networks
ctx.set_line_width(0.3)
for _ in range(60):
    r_start = random.uniform(50, max_radius)
    theta_start = random.uniform(0, 2 * math.pi)
    
    ctx.set_source_rgba(0, 0, 0, 0.4)
    x1, y1 = get_polar_pos(r_start, theta_start, distortion=1.5)
    ctx.move_to(x1, y1)
    
    # Connect to a nearby "attractor"
    r_end = r_start + random.uniform(-30, 30)
    theta_end = theta_start + random.uniform(-0.2, 0.2)
    x2, y2 = get_polar_pos(r_end, theta_end, distortion=1.5)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 4. TYPOGRAPHIC ANCHOR (Swiss Hierarchy)
# Simulating block text as a grounding element
def draw_block(x, y, w, h):
    ctx.set_source_rgb(0.1, 0.1, 0.1)
    ctx.rectangle(x, y, w, h)
    ctx.fill()

# Small visual "ID" blocks in the corner
margin = 40
draw_block(margin, height - margin - 20, 40, 8)
draw_block(margin, height - margin - 8, 25, 4)
draw_block(margin + 45, height - margin - 20, 10, 8)

# Subtle border/frame to emphasize the composition
ctx.set_source_rgba(0.1, 0.1, 0.1, 1.0)
ctx.set_line_width(1.0)
ctx.rectangle(margin/2, margin/2, width-margin, height-margin)
ctx.stroke()

# Final atmospheric layer: very fine texture
for _ in range(1000):
    ctx.set_source_rgba(0, 0, 0, 0.03)
    ctx.rectangle(random.random() * width, random.random() * height, 1, 1)
    ctx.fill()
