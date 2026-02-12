import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal for high contrast
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Constants for the Polar Transformation
CENTER_X, CENTER_Y = width / 2, height / 2
INNER_RADIUS = 60
OUTER_RADIUS = 220
CIRCUMFERENCE_FACTOR = 2 * math.pi

def project(u, v):
    """
    Maps normalized coordinates (u, v) [0, 1] to Polar Space with Radial Distortion.
    u: normalized angle
    v: normalized radius
    """
    # Radial distortion logic: interference patterns based on angle
    distortion = math.sin(u * 12 + v * 5) * 8 * (1 - v)
    angle = u * CIRCUMFERENCE_FACTOR - math.pi / 2
    radius = INNER_RADIUS + v * (OUTER_RADIUS - INNER_RADIUS) + distortion
    
    x = CENTER_X + radius * math.cos(angle)
    y = CENTER_Y + radius * math.sin(angle)
    return x, y

def draw_curved_line(u1, v1, u2, v2, steps=20):
    """Draws a line between two points in polar space by interpolating."""
    ctx.move_to(*project(u1, v1))
    for i in range(1, steps + 1):
        t = i / steps
        curr_u = u1 + (u2 - u1) * t
        curr_v = v1 + (v2 - v1) * t
        ctx.line_to(*project(curr_u, curr_v))

def recursive_partition(u, v, w, h, depth):
    """
    Swiss-inspired stochastic subdivision.
    Creates a hierarchical grid structure.
    """
    if depth > 5 or (depth > 2 and random.random() < 0.2):
        render_cell(u, v, w, h, depth)
        return

    # Randomly split horizontally or vertically
    split_horiz = random.random() > 0.5
    ratio = random.uniform(0.3, 0.7)

    if split_horiz:
        recursive_partition(u, v, w * ratio, h, depth + 1)
        recursive_partition(u + w * ratio, v, w * (1 - ratio), h, depth + 1)
    else:
        recursive_partition(u, v, w, h * ratio, depth + 1)
        recursive_partition(u, v + h * ratio, w, h * (1 - ratio), depth + 1)

def render_cell(u, v, w, h, depth):
    """
    Fills subdivided cells with structural flux: 
    fan-arrays, optical mixing, and vector networking.
    """
    style = random.choice(['fan', 'hatch', 'network', 'dots'])
    
    # Line weight gets thinner as depth increases
    ctx.set_line_width(0.4 if depth > 3 else 0.8)
    alpha = random.uniform(0.3, 0.8)
    ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)

    if style == 'fan':
        # Fan-like arrays from a corner
        corner_u, corner_v = u, v
        num_lines = int(15 * w * 10)
        for i in range(num_lines + 1):
            target_u = u + w
            target_v = v + (i / num_lines) * h
            draw_curved_line(corner_u, corner_v, target_u, target_v)
            ctx.stroke()

    elif style == 'hatch':
        # High-frequency horizontal lines for 'optical mixing'
        num_lines = int(10 * h * 10)
        for i in range(num_lines + 1):
            curr_v = v + (i / num_lines) * h
            draw_curved_line(u, curr_v, u + w, curr_v)
            ctx.stroke()

    elif style == 'network':
        # Stochastic point-to-point networking
        points = [(u + random.random() * w, v + random.random() * h) for _ in range(8)]
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                draw_curved_line(points[i][0], points[i][1], points[j][0], points[j][1])
                ctx.stroke()

    elif style == 'dots':
        # Dithered texture/stippling
        ctx.set_source_rgba(1.0, 1.0, 1.0, alpha * 1.5)
        num_dots = int(w * h * 500)
        for _ in range(num_dots):
            du = u + random.random() * w
            dv = v + random.random() * h
            dx, dy = project(du, dv)
            ctx.arc(dx, dy, 0.5, 0, 2 * math.pi)
            ctx.fill()

# Execution of the Generative Logic
random.seed(42) # For reproducibility of the specific rhythm

# Core structural pass
recursive_partition(0, 0, 1.0, 1.0, 0)

# Overlay: Mathematical "Ticks" (The Swiss Precision)
ctx.set_source_rgba(1, 1, 1, 0.2)
ctx.set_line_width(1.5)
for i in range(12):
    angle_u = i / 12
    x1, y1 = project(angle_u, 1.02)
    x2, y2 = project(angle_u, 1.1)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# Final subtle geometric anchor
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.arc(CENTER_X, CENTER_Y, INNER_RADIUS - 10, 0, 2 * math.pi)
ctx.stroke()
ctx.arc(CENTER_X, CENTER_Y, OUTER_RADIUS + 30, 0, 2 * math.pi)
ctx.stroke()

# IMPORTANT: No write_to_png call as per instructions.
