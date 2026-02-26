import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep technical navy/black
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

# Constants
CENTER_X, CENTER_Y = width / 2, height / 2
RINGS = 18
RADIAL_DIVS = 72
MAX_RADIUS = min(width, height) * 0.42

def polar_to_cartesian(r, theta, distortion_factor=0.0):
    """Converts polar to cartesian with an optional radial distortion."""
    # Radial distortion based on frequency harmonics
    r_distorted = r + (math.sin(theta * 6) * distortion_factor * 15)
    r_distorted += (math.cos(theta * 12) * distortion_factor * 5)
    
    x = CENTER_X + r_distorted * math.cos(theta)
    y = CENTER_Y + r_distorted * math.sin(theta)
    return x, y

# --- Layer 1: The Underlying Technical Grid ---
ctx.set_source_rgba(0.2, 0.3, 0.4, 0.3)
ctx.set_line_width(0.5)

for i in range(1, RINGS + 1):
    r = (i / RINGS) * MAX_RADIUS
    ctx.new_path()
    for j in range(RADIAL_DIVS + 1):
        theta = (j / RADIAL_DIVS) * 2 * math.pi
        x, y = polar_to_cartesian(r, theta)
        if j == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
    ctx.stroke()

# --- Layer 2: Vector Fans & Connectivity (Informational Topology) ---
# Connecting nodes across the radial grid to create moiré interference
ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
ctx.set_line_width(0.3)

for j in range(0, RADIAL_DIVS, 2):
    theta_start = (j / RADIAL_DIVS) * 2 * math.pi
    # Every 4th radial line creates a fan-out to the opposite quadrant
    for i in range(5, RINGS, 3):
        r_start = (i / RINGS) * MAX_RADIUS
        x1, y1 = polar_to_cartesian(r_start, theta_start, distortion_factor=0.2)
        
        # Connect to a range of points on a different ring
        for offset in range(-5, 6):
            target_j = (j + RADIAL_DIVS // 2 + offset) % RADIAL_DIVS
            theta_end = (target_j / RADIAL_DIVS) * 2 * math.pi
            r_end = MAX_RADIUS * 0.9
            x2, y2 = polar_to_cartesian(r_end, theta_end, distortion_factor=0.5)
            
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
    ctx.stroke()

# --- Layer 3: Structural Distortion Arcs ---
# Heavy strokes that define the 'Swiss' hierarchy
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.8)
ctx.set_line_width(1.2)

for i in [RINGS // 3, (2 * RINGS) // 3, RINGS]:
    r = (i / RINGS) * MAX_RADIUS
    # Draw fragmented, distorted arcs
    for segment in range(4):
        start_angle = segment * (math.pi / 2) + 0.2
        end_angle = (segment + 1) * (math.pi / 2) - 0.2
        
        steps = 40
        for s in range(steps + 1):
            theta = start_angle + (s / steps) * (end_angle - start_angle)
            dist = 0.4 if i == RINGS else 0.1
            x, y = polar_to_cartesian(r, theta, distortion_factor=dist)
            if s == 0: ctx.move_to(x, y)
            else: ctx.line_to(x, y)
        ctx.stroke()

# --- Layer 4: Annotated Vertices (Primitive Glyphs) ---
# Adding small crosses and dots at grid intersections for "Tactile Surface"
for i in range(4, RINGS + 1, 4):
    r = (i / RINGS) * MAX_RADIUS
    for j in range(0, RADIAL_DIVS, 6):
        theta = (j / RADIAL_DIVS) * 2 * math.pi
        x, y = polar_to_cartesian(r, theta, distortion_factor=0.1)
        
        # Randomly choose between a small circle, a cross, or a dot
        choice = random.random()
        if choice > 0.7:
            # Cross
            sz = 3
            ctx.set_source_rgb(0.5, 0.7, 1.0)
            ctx.set_line_width(0.7)
            ctx.move_to(x - sz, y)
            ctx.line_to(x + sz, y)
            ctx.move_to(x, y - sz)
            ctx.line_to(x, y + sz)
            ctx.stroke()
        elif choice > 0.4:
            # Circle
            ctx.set_source_rgb(1, 1, 1)
            ctx.arc(x, y, 1.5, 0, 2 * math.pi)
            ctx.fill()
        else:
            # Square dot
            ctx.set_source_rgb(0.3, 0.4, 0.6)
            ctx.rectangle(x-1, y-1, 2, 2)
            ctx.fill()

# --- Layer 5: Peripheral "Noise" & Data Blocks ---
# Small technical annotations in the corners
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.set_line_width(0.5)
for _ in range(12):
    nx = random.choice([40, width - 60])
    ny = random.randint(40, height - 40)
    # Mini grid block
    for r_idx in range(3):
        for c_idx in range(4):
            if random.random() > 0.3:
                ctx.rectangle(nx + c_idx*4, ny + r_idx*4, 2, 2)
                ctx.fill()

# Final border accent
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Output is handled externally.
