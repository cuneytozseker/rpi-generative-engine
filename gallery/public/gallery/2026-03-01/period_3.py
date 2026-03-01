import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Neutral "Void"
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

# Constants
CX, CY = width / 2, height / 2
MAX_RADIUS = 260
GOLDEN_RATIO = (1 + 5**0.5) / 2

def transform_polar(r, theta, distortion_factor=1.0):
    """
    Transforms polar coordinates into a distorted Cartesian space.
    Uses harmonic interference to warp the 'Swiss' grid.
    """
    # Radial distortion using nested sine waves
    r_warp = r + (12 * math.sin(theta * 8) * (r / MAX_RADIUS)) * distortion_factor
    # Angular torsion relative to distance from center
    theta_warp = theta + (0.15 * math.cos(r * 0.04)) * distortion_factor
    
    x = CX + r_warp * math.cos(theta_warp)
    y = CY + r_warp * math.sin(theta_warp)
    return x, y

def draw_distorted_arc(r, a1, a2, steps=40):
    """Draws a line segment following the distorted polar grid."""
    for i in range(steps + 1):
        angle = a1 + (a2 - a1) * (i / steps)
        x, y = transform_polar(r, angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

def draw_distorted_radial(r1, r2, angle, steps=20):
    """Draws a radial line segment following the distorted polar grid."""
    for i in range(steps + 1):
        radius = r1 + (r2 - r1) * (i / steps)
        x, y = transform_polar(radius, angle)
        if i == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)

def recursive_subdivide(r1, r2, a1, a2, depth):
    """Recursive subdivision of polar cells based on Swiss hierarchy."""
    if depth > 5:
        return

    # Probability of stopping subdivision
    stop_prob = 0.2 + (depth * 0.1)
    if depth > 2 and random.random() < stop_prob:
        # Render cell content
        render_cell_content(r1, r2, a1, a2, depth)
    else:
        # Choose to split radially or angularly based on aspect ratio
        if (r2 - r1) > (a2 - a1) * r1:
            split = r1 + (r2 - r1) * (1 / GOLDEN_RATIO)
            recursive_subdivide(r1, split, a1, a2, depth + 1)
            recursive_subdivide(split, r2, a1, a2, depth + 1)
        else:
            split = a1 + (a2 - a1) * (1 / GOLDEN_RATIO)
            recursive_subdivide(r1, r2, a1, split, depth + 1)
            recursive_subdivide(r1, r2, split, a2, depth + 1)

def render_cell_content(r1, r2, a1, a2, depth):
    """Fills cells with structured 'digital grain' and chromatic vibration."""
    
    # Choose color based on depth and radial position (Chromatic Vibration)
    # Transitions from deep blues to fiery oranges/magentas
    t = r1 / MAX_RADIUS
    if random.random() > 0.4:
        # High contrast monochromatic line
        ctx.set_source_rgba(0.9, 0.9, 0.95, 0.6 / depth)
    else:
        # Spectral transition
        r_col = 0.5 + 0.5 * math.sin(t * 3 + 0.5)
        g_col = 0.2 * math.cos(t * 10)
        b_col = 0.6 + 0.4 * math.sin(t * 5)
        ctx.set_source_rgba(r_col, g_col, b_col, 0.8 / depth)

    ctx.set_line_width(0.4)
    
    # 1. Draw Cell Boundaries
    draw_distorted_arc(r1, a1, a2)
    ctx.stroke()
    draw_distorted_radial(r1, r2, a1)
    ctx.stroke()

    # 2. Binary Density: Stippled hatchings
    hatch_count = int(10 / (depth + 1))
    for i in range(hatch_count):
        sub_r = r1 + (r2 - r1) * (i / max(1, hatch_count))
        ctx.set_line_width(0.2 if random.random() > 0.2 else 1.2)
        draw_distorted_arc(sub_r, a1, a2)
        ctx.stroke()

    # 3. Typography-like Glyphs (Binary marks)
    if depth % 2 == 0:
        gx, gy = transform_polar((r1 + r2) / 2, (a1 + a2) / 2)
        ctx.rectangle(gx - 1, gy - 1, 2, 2)
        ctx.fill()

# --- Execution ---

# Draw background glow (Atmospheric Emergence)
for i in range(40, 0, -1):
    alpha = 0.01
    size = i * 8
    ctx.set_source_rgba(0.2, 0.1, 0.3, alpha)
    ctx.arc(CX, CY, size, 0, 2 * math.pi)
    ctx.fill()

# Create the systematic grid structure
num_sectors = 8
for s in range(num_sectors):
    start_angle = (s / num_sectors) * 2 * math.pi
    end_angle = ((s + 1) / num_sectors) * 2 * math.pi
    recursive_subdivide(40, MAX_RADIUS, start_angle, end_angle, 0)

# Apply a final "High Frequency" noise layer
ctx.set_line_width(0.3)
for _ in range(1200):
    noise_r = random.uniform(20, MAX_RADIUS + 20)
    noise_a = random.uniform(0, 2 * math.pi)
    nx, ny = transform_polar(noise_r, noise_a, distortion_factor=1.2)
    
    # Small tick marks
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.4))
    ctx.move_to(nx, ny)
    ctx.line_to(nx + random.uniform(-2, 2), ny + random.uniform(-2, 2))
    ctx.stroke()

# Central focus (The Seed)
ctx.set_source_rgb(1, 0.2, 0.1) # Firey orange
ctx.arc(CX, CY, 3, 0, 2 * math.pi)
ctx.fill()

# Finish
