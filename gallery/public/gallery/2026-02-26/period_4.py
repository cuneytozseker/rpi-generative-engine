import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.02, 0.02, 0.03)  # Deep Charcoal
ctx.paint()

# Constants for the Polar Transformation
CENTER_X, CENTER_Y = width / 2, height / 2
MAX_RADIUS = min(width, height) * 0.45
GOLDEN_RATIO = (1 + 5**0.5) / 2

def polar_transform(x, y, distortion_factor=0.0):
    """
    Maps Cartesian coordinates (x: 0..width, y: 0..height) 
    to a Polar system with radial distortion.
    """
    # Normalize inputs
    nx = x / width
    ny = y / height
    
    # Non-linear radial distribution (logarithmic-ish spacing)
    r = math.pow(ny, 1.2) * MAX_RADIUS
    
    # Angle with a slight spiral twist
    theta = nx * 2 * math.pi + (ny * math.pi * 0.2)
    
    # Radial distortion (wavy interference)
    r += math.sin(theta * 8) * distortion_factor * 15
    
    px = CENTER_X + r * math.cos(theta)
    py = CENTER_Y + r * math.sin(theta)
    return px, py

def draw_subdivided_quad(x, y, w, h, depth):
    """
    Recursively subdivides space and draws the polar-mapped result.
    """
    # Dynamic split probability based on distance from center (y-axis in Cartesian)
    # Higher density towards the "rim" or "core"
    split_prob = 0.75 - (depth * 0.1)
    
    # Threshold for stopping recursion
    if depth < 6 and (random.random() < split_prob or depth < 2):
        # Determine split direction
        if random.random() > 0.5:
            # Horizontal split
            draw_subdivided_quad(x, y, w, h/2, depth + 1)
            draw_subdivided_quad(x, y + h/2, w, h/2, depth + 1)
        else:
            # Vertical split
            draw_subdivided_quad(x, y, w/2, h, depth + 1)
            draw_subdivided_quad(x + w/2, y, w/2, h, depth + 1)
    else:
        # Drawing logic for the leaf nodes
        render_cell(x, y, w, h, depth)

def render_cell(x, y, w, h, depth):
    # Get the four corners of the quad in polar space
    # We sample intermediate points to make the arcs smooth
    steps = 8
    points = []
    
    # Top edge
    for i in range(steps + 1):
        points.append(polar_transform(x + (w * i / steps), y, 2.0))
    # Right edge
    for i in range(1, steps + 1):
        points.append(polar_transform(x + w, y + (h * i / steps), 2.0))
    # Bottom edge
    for i in range(1, steps + 1):
        points.append(polar_transform(x + w - (w * i / steps), y + h, 2.0))
    # Left edge
    for i in range(1, steps):
        points.append(polar_transform(x, y + h - (h * i / steps), 2.0))

    # 1. Draw "Ghost" Glow (Soft Diffusion)
    ctx.move_to(points[0][0], points[0][1])
    for p in points[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    
    alpha = 0.05 + (1.0 / (depth + 1)) * 0.1
    ctx.set_source_rgba(0.4, 0.6, 1.0, alpha) # Spectral Blue
    ctx.fill()

    # 2. Draw Precision Hairlines
    ctx.set_line_width(0.4)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.move_to(points[0][0], points[0][1])
    for p in points[1:]:
        ctx.line_to(p[0], p[1])
    ctx.close_path()
    ctx.stroke()

    # 3. Add Chromatic Data Points at specific intersections
    if depth > 4 and random.random() > 0.7:
        ctx.set_source_rgb(1.0, 0.2, 0.3) # Swiss Red
        dot_x, dot_y = points[0]
        ctx.arc(dot_x, dot_y, 1.2, 0, 2 * math.pi)
        ctx.fill()

# --- Execution ---

# Draw a concentric background rhythm first
ctx.set_line_width(0.2)
for i in range(1, 15):
    ctx.set_source_rgba(1, 1, 1, 0.1)
    radius = (i / 15.0) * MAX_RADIUS * 1.2
    ctx.arc(CENTER_X, CENTER_Y, radius, 0, 2 * math.pi)
    ctx.stroke()

# Seed for reproducibility of systematic variation
random.seed(42)

# Start the recursive grid subdivision
# The grid is mapped from a virtual 600x480 space to the polar circle
draw_subdivided_quad(0, 0, width, height, 0)

# Final Overlay: High-contrast crosshair (Swiss alignment)
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.set_line_width(0.5)
# Vertical
ctx.move_to(CENTER_X, CENTER_Y - 20)
ctx.line_to(CENTER_X, CENTER_Y + 20)
# Horizontal
ctx.move_to(CENTER_X - 20, CENTER_Y)
ctx.line_to(CENTER_X + 20, CENTER_Y)
ctx.stroke()

# Outermost border circle (structural boundary)
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(1.0)
ctx.arc(CENTER_X, CENTER_Y, MAX_RADIUS, 0, 2 * math.pi)
ctx.stroke()

