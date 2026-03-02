import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for high contrast
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
max_radius = min(width, height) * 0.45
radial_steps = 60    # Number of "spokes"
concentric_steps = 45 # Number of "rings"
accent_color = (1.0, 0.2, 0.1) # Vibrant Swiss Red-Orange

def ease_in_quad(t):
    return t * t

def transform_coords(r_norm, theta_norm, twist=0.5):
    """
    Transforms normalized grid coordinates (0-1) into distorted polar space.
    r_norm: distance from center (0 to 1)
    theta_norm: rotation (0 to 1)
    """
    # Apply exponential easing to radius to create focal compression toward the center
    r = ease_in_quad(r_norm) * max_radius
    
    # Introduce a mathematical "twist" based on radius (logarithmic spiral influence)
    angle = theta_norm * 2 * math.pi + (r_norm * twist)
    
    # Radial distortion: subtle wave interference
    r += math.sin(theta_norm * 12) * (10 * r_norm)
    
    x = center_x + r * math.cos(angle)
    y = center_y + r * math.sin(angle)
    return x, y

# 1. Draw Subtle Background Connectivity (The "System")
ctx.set_line_width(0.3)
for i in range(radial_steps):
    theta_n = i / radial_steps
    ctx.move_to(*transform_coords(0, theta_n))
    
    # Draw radial lines with micro-segments for distortion fidelity
    for j in range(1, concentric_steps + 1):
        r_n = j / concentric_steps
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
        ctx.line_to(*transform_coords(r_n, theta_n))
    ctx.stroke()

# 2. Draw Concentric Rings with Optical Density
for j in range(1, concentric_steps + 1):
    r_n = j / concentric_steps
    # Variation in line weight based on distance (structural hierarchy)
    ctx.set_line_width(0.2 + (r_n * 0.8))
    
    first_pt = transform_coords(r_n, 0)
    ctx.move_to(*first_pt)
    
    for i in range(1, radial_steps + 1):
        theta_n = i / radial_steps
        # Higher alpha at specific intervals to create visual rhythm
        alpha = 0.4 if j % 5 == 0 else 0.15
        ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
        ctx.line_to(*transform_coords(r_n, theta_n))
    
    ctx.stroke()

# 3. Structural Anomalies & Data Markers (The "Logic")
# We highlight intersections that satisfy a specific mathematical modulo
for i in range(radial_steps):
    for j in range(concentric_steps):
        if (i * j) % 31 == 0 or (i == j):
            r_n = j / concentric_steps
            theta_n = i / radial_steps
            x, y = transform_coords(r_n, theta_n)
            
            # Draw primary marker
            ctx.set_source_rgb(*accent_color)
            ctx.arc(x, y, 1.5, 0, 2 * math.pi)
            ctx.fill()
            
            # Draw "Relational Logic" connector
            # Connect some markers back to a central focal point or neighbor
            if r_n > 0.5:
                nx, ny = transform_coords(r_n - 0.1, theta_n + 0.05)
                ctx.set_source_rgba(1.0, 0.2, 0.1, 0.4)
                ctx.set_line_width(0.5)
                ctx.move_to(x, y)
                ctx.line_to(nx, ny)
                ctx.stroke()

# 4. Global Structural Overlay (Brutalist Framing)
# Adds a layer of architectural precision
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(1.0)
for radius in [max_radius * 0.5, max_radius * 0.8, max_radius]:
    ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
    ctx.stroke()

# 5. Fine Moiré Texture (Noise/Density)
# Thousands of tiny dots scattered along the mathematical paths
for _ in range(1500):
    r_n = random.uniform(0.1, 1.0)
    theta_n = random.uniform(0, 1.0)
    x, y = transform_coords(r_n, theta_n)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.5))
    ctx.rectangle(x, y, 0.5, 0.5)
    ctx.fill()

# 6. Typography Elements (Abstracted)
# Representing data labels in a Swiss layout style
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
for i in range(0, 360, 45):
    angle = math.radians(i)
    tx = center_x + (max_radius + 20) * math.cos(angle)
    ty = center_y + (max_radius + 20) * math.sin(angle)
    
    ctx.save()
    ctx.translate(tx, ty)
    ctx.rotate(angle + math.pi/2)
    ctx.set_source_rgba(0.7, 0.7, 0.8, 0.8)
    ctx.show_text(f"SYS_REF_{i:03d}")
    ctx.restore()

# Final Polish: Center crosshair
ctx.set_source_rgb(*accent_color)
ctx.set_line_width(1)
ctx.move_to(center_x - 10, center_y)
ctx.line_to(center_x + 10, center_y)
ctx.move_to(center_x, center_y - 10)
ctx.line_to(center_x, center_y + 10)
ctx.stroke()
