import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def polar_to_cartesian(r, theta, cx, cy):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_swiss_cross(ctx, x, y, size):
    half = size / 2
    thick = size / 3
    ctx.move_to(x - half, y)
    ctx.line_to(x + half, y)
    ctx.move_to(x, y - half)
    ctx.line_to(x, y + half)
    ctx.set_line_width(thick)
    ctx.stroke()

# Parameters for the Procedural System
center_x, center_y = width / 2, height / 2
rings = 18
segments = 72
max_radius = min(width, height) * 0.45
distortion_factor = 1.2
phi = (1 + 5**0.5) / 2  # Golden ratio for harmonic spacing

# 1. Create a "Radial Swiss Grid" with additive transparency
ctx.set_operator(cairo.OPERATOR_ADD)

for i in range(rings):
    # Use golden ratio for non-uniform ring spacing (Progressive Growth)
    r = max_radius * math.pow(i / rings, 0.8)
    
    # Modulate transparency based on radius
    alpha = 0.1 + 0.4 * (1 - i / rings)
    
    for j in range(segments):
        # Base angle
        theta = (j / segments) * 2 * math.pi
        
        # Apply radial distortion: the "twist" and "wobble"
        # Distortion is tied to the proximity to the center and the angle
        angle_distortion = math.sin(i * 0.5 + theta * 3) * 0.1
        radial_distortion = math.cos(theta * 5) * (i * 1.5)
        
        curr_r = r + radial_distortion
        curr_theta = theta + angle_distortion + (i * 0.05) # Spiral twist
        
        x, y = polar_to_cartesian(curr_r, curr_theta, center_x, center_y)
        
        # Nodal Logic: Connect nodes to neighbors to create moiré patterns
        if i > 0:
            # Connect to previous ring
            prev_r = max_radius * math.pow((i-1) / rings, 0.8) + math.cos(theta * 5) * ((i-1) * 1.5)
            prev_theta = theta + math.sin((i-1) * 0.5 + theta * 3) * 0.1 + ((i-1) * 0.05)
            px, py = polar_to_cartesian(prev_r, prev_theta, center_x, center_y)
            
            ctx.set_source_rgba(0.8, 0.8, 0.9, alpha * 0.5)
            ctx.set_line_width(0.4)
            ctx.move_to(x, y)
            ctx.line_to(px, py)
            ctx.stroke()

        # Connect to adjacent segment
        next_theta_base = ((j + 1) / segments) * 2 * math.pi
        next_r = r + math.cos(next_theta_base * 5) * (i * 1.5)
        next_theta = next_theta_base + math.sin(i * 0.5 + next_theta_base * 3) * 0.1 + (i * 0.05)
        nx, ny = polar_to_cartesian(next_r, next_theta, center_x, center_y)
        
        ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
        ctx.set_line_width(0.6)
        ctx.move_to(x, y)
        ctx.line_to(nx, ny)
        ctx.stroke()

# 2. Emergent Symbols and High-Chroma Accents
ctx.set_operator(cairo.OPERATOR_OVER)
random.seed(42) # Deterministic randomness for systematic feel

for i in range(rings):
    r = max_radius * math.pow(i / rings, 0.8)
    for j in range(segments):
        if random.random() < 0.04: # Sparse density modulation
            theta = (j / segments) * 2 * math.pi
            curr_r = r + math.cos(theta * 5) * (i * 1.5)
            curr_theta = theta + math.sin(i * 0.5 + theta * 3) * 0.1 + (i * 0.05)
            x, y = polar_to_cartesian(curr_r, curr_theta, center_x, center_y)
            
            # High-chroma accent (Swiss Red)
            if random.random() > 0.7:
                ctx.set_source_rgb(1.0, 0.1, 0.2)
                draw_swiss_cross(ctx, x, y, 6)
            else:
                # Precision markers (white squares)
                ctx.set_source_rgb(1, 1, 1)
                size = 2 if i < rings/2 else 1
                ctx.rectangle(x - size/2, y - size/2, size, size)
                ctx.fill()

# 3. Topographical Annotation (Sequential Repetition)
ctx.set_source_rgba(1, 1, 1, 0.6)
ctx.set_line_width(0.5)
for i in range(5):
    # Small tick marks on an outer axis
    angle = (i / 5) * 0.2 + math.pi * 1.2
    dist = max_radius * 1.1
    x1, y1 = polar_to_cartesian(dist, angle, center_x, center_y)
    x2, y2 = polar_to_cartesian(dist + 20, angle, center_x, center_y)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 4. Subtle Radial Gradient Overlay for depth
grad = cairo.RadialGradient(center_x, center_y, 10, center_x, center_y, max_radius * 1.5)
grad.add_color_stop_rgba(0, 1, 1, 1, 0)
grad.add_color_stop_rgba(0.7, 0, 0, 0, 0)
grad.add_color_stop_rgba(1, 0, 0, 0, 0.4)
ctx.set_source(grad)
ctx.paint()

# Final Polish: Fine Grain/Structure
for _ in range(100):
    ctx.set_source_rgba(1, 1, 1, 0.05)
    rx, ry = random.uniform(0, width), random.uniform(0, height)
    ctx.rectangle(rx, ry, 0.5, 0.5)
    ctx.fill()
