import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Cobalt/Black Foundation
ctx.set_source_rgb(0.02, 0.03, 0.1)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 18
segments = 48
radius_step = 18
entropy_factor = 1.2 # Increases with radius

def get_polar_coords(r, theta, distortion=0):
    """Calculates polar to cartesian with optional entropy displacement."""
    dist_x = random.uniform(-distortion, distortion)
    dist_y = random.uniform(-distortion, distortion)
    x = center_x + r * math.cos(theta) + dist_x
    y = center_y + r * math.sin(theta) + dist_y
    return x, y

def draw_spectral_glow(x, y, size, r_val, g_val, b_val):
    """Creates a soft-edge chromatic bleed effect."""
    gradient = cairo.RadialGradient(x, y, 0, x, y, size * 2)
    gradient.add_color_stop_rgba(0, r_val, g_val, b_val, 0.6)
    gradient.add_color_stop_rgba(1, r_val, g_val, b_val, 0)
    ctx.set_source(gradient)
    ctx.arc(x, y, size * 2, 0, 2 * math.pi)
    ctx.fill()

# 1. Atmospheric Layer: Recursive Subdivisions and Blurred Gradients
ctx.set_operator(cairo.OPERATOR_ADD)
for i in range(rings):
    r = (i + 1) * radius_step
    # Progressive entropy based on distance from center
    current_entropy = (i / rings) ** 2 * 15 
    
    for j in range(segments):
        angle = (j / segments) * 2 * math.pi
        
        # Spectral accents (warm-to-cool transition)
        hue_shift = i / rings
        red = 0.2 + 0.8 * math.sin(hue_shift * math.pi)
        blue = 0.5 + 0.5 * math.cos(hue_shift * math.pi)
        green = 0.2 + 0.3 * math.sin(angle)

        if random.random() > 0.7:
            x, y = get_polar_coords(r, angle, current_entropy)
            draw_spectral_glow(x, y, random.uniform(2, 6), red, green, blue)

# 2. Systematic Layer: The Distorted Swiss Grid
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_line_width(0.5)

for i in range(1, rings):
    r = i * radius_step
    
    # Draw Radial Lines (Connect nodes to center)
    for j in range(segments):
        if j % 4 == 0: # Selective precision
            angle = (j / segments) * 2 * math.pi
            x1, y1 = get_polar_coords(r, angle)
            x2, y2 = get_polar_coords(r + radius_step, angle)
            
            ctx.set_source_rgba(0.8, 0.9, 1.0, 0.3)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

    # Draw Concentric Rings (Path logic)
    ctx.new_path()
    for j in range(segments + 1):
        angle = (j / segments) * 2 * math.pi
        # Introduce "Glitch" displacement in the path
        r_distorted = r + (math.sin(angle * 8) * (i / 4))
        x, y = get_polar_coords(r_distorted, angle)
        
        if j == 0:
            ctx.move_to(x, y)
        else:
            ctx.line_to(x, y)
            
    ctx.set_source_rgba(0.6, 0.8, 1.0, 0.15)
    ctx.stroke()

# 3. Technical Constellation: Coordinate-mapped nodes
for i in range(3, rings, 2):
    r = i * radius_step
    for j in range(segments):
        angle = (j / segments) * 2 * math.pi
        
        # High-contrast sharp primitives
        if random.random() > 0.85:
            x, y = get_polar_coords(r, angle)
            
            # Draw Data-Viz Nodes
            ctx.set_source_rgba(1, 1, 1, 0.8)
            if j % 2 == 0:
                ctx.arc(x, y, 1.5, 0, 2 * math.pi)
                ctx.fill()
            else:
                # Vertical tick marks
                ctx.set_line_width(1.2)
                ctx.move_to(x, y - 4)
                ctx.line_to(x, y + 4)
                ctx.stroke()
                
            # Connect some nodes with high-contrast sharp vectors
            if random.random() > 0.5:
                next_angle = ((j + 1) / segments) * 2 * math.pi
                nx, ny = get_polar_coords(r, next_angle)
                ctx.set_line_width(0.3)
                ctx.set_source_rgba(1, 0.2, 0.4, 0.7) # Spectral red accent
                ctx.move_to(x, y)
                ctx.line_to(nx, ny)
                ctx.stroke()

# 4. Final Polish: Centralized density and visual hierarchy
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.arc(center_x, center_y, 3, 0, 2 * math.pi)
ctx.fill()

# Crosshair / Analytical overlay
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(0.5)
ctx.move_to(0, center_y)
ctx.line_to(width, center_y)
ctx.move_to(center_x, 0)
ctx.line_to(center_x, height)
ctx.stroke()

# Border framing (Brutalist touch)
ctx.set_line_width(20)
ctx.set_source_rgb(0, 0, 0)
ctx.rectangle(0, 0, width, height)
ctx.stroke()
