import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def project(r, theta, center_x, center_y, distortion_factor):
    """Maps polar coordinates to Cartesian with a radial wave distortion."""
    # Radial distortion based on frequency harmonics
    r_distorted = r * (1 + 0.08 * math.sin(theta * 6 + r * 0.02) * distortion_factor)
    x = center_x + r_distorted * math.cos(theta)
    y = center_y + r_distorted * math.sin(theta)
    return x, y

def draw_subdivided_cell(r1, r2, a1, a2, depth, max_depth):
    """Recursively subdivides polar cells based on distance and depth."""
    center_x, center_y = width / 2, height / 2
    
    # Controlled randomness for subdivision logic
    threshold = 0.4 + (r1 / 300.0) * 0.5
    
    if depth < max_depth and random.random() > threshold:
        # Decide to split either radially or angularly
        if random.random() > 0.5:
            mid_a = (a1 + a2) / 2
            draw_subdivided_cell(r1, r2, a1, mid_a, depth + 1, max_depth)
            draw_subdivided_cell(r1, r2, mid_a, a2, depth + 1, max_depth)
        else:
            mid_r = (r1 + r2) / 2
            draw_subdivided_cell(r1, mid_r, a1, a2, depth + 1, max_depth)
            draw_subdivided_cell(mid_r, r2, a1, a2, depth + 1, max_depth)
    else:
        # Drawing the cell boundary with optical interference logic
        for i in range(2):
            # Layer offset for moiré/interference effect
            offset_dist = i * 1.2
            
            # Use chromatic diffusion - faint cyans and oranges
            if i == 0:
                ctx.set_source_rgba(0.9, 0.2, 0.3, 0.6) # Swiss Red/Magenta
            else:
                ctx.set_source_rgba(0.2, 0.8, 0.9, 0.4) # Cyan shift
                
            ctx.set_line_width(0.4 / (depth + 1))
            
            # Trace the polar arc
            steps = 10
            for s in range(steps + 1):
                t = a1 + (a2 - a1) * (s / steps)
                px, py = project(r1 + offset_dist, t, center_x, center_y, 1.0)
                if s == 0:
                    ctx.move_to(px, py)
                else:
                    ctx.line_to(px, py)
            
            for s in range(steps + 1):
                t = a2 - (a2 - a1) * (s / steps)
                px, py = project(r2 + offset_dist, t, center_x, center_y, 1.0)
                ctx.line_to(px, py)
                
            ctx.close_path()
            ctx.stroke()

# --- Main Composition ---

# 1. Establish the underlying Swiss Grid in polar space
rings = 12
sectors = 18
max_r = 320
center_x, center_y = width / 2, height / 2

random.seed(42) # Deterministic emergence

# Create multiple layers of the system to simulate depth
for layer in range(3):
    opacity = 0.15 + (layer * 0.2)
    distortion = 0.5 + (layer * 0.5)
    
    for i in range(rings):
        r_start = (i / rings) * max_r
        r_end = ((i + 1) / rings) * max_r
        
        for j in range(sectors):
            a_start = (j / sectors) * (2 * math.pi)
            a_end = ((j + 1) / sectors) * (2 * math.pi)
            
            # Recursive depth increases as we move outward or inward selectively
            target_depth = 2 if i % 3 == 0 else 4
            
            ctx.save()
            # Apply a slight rotation per layer for systemic misalignment
            ctx.translate(center_x, center_y)
            ctx.rotate(layer * 0.02)
            ctx.translate(-center_x, -center_y)
            
            draw_subdivided_cell(r_start, r_end, a_start, a_end, 0, target_depth)
            ctx.restore()

# 2. Geometric Focal Point (Swiss Hierarchy)
# Adding a high-contrast central axis to ground the composition
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(0.5)
for angle in [0, math.pi/2, math.pi, 3*math.pi/2]:
    x1, y1 = project(20, angle, center_x, center_y, 0)
    x2, y2 = project(max_r + 40, angle, center_x, center_y, 1.5)
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.stroke()

# 3. Fine Grain / Texture Layer
# Hair-thin concentric circles for structural rhythm
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(0.2)
for r in range(0, int(max_r + 50), 5):
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

# 4. Final Accent: Data Points
# Placing small technical markers at subdivision intersections
for _ in range(100):
    r = random.uniform(50, max_r)
    a = random.uniform(0, 2 * math.pi)
    px, py = project(r, a, center_x, center_y, 1.0)
    
    ctx.set_source_rgb(1, 1, 1)
    size = random.choice([0.5, 1.0, 1.5])
    ctx.rectangle(px - size/2, py - size/2, size, size)
    ctx.fill()

# Clean up / Vignette effect
gradient = cairo.RadialGradient(center_x, center_y, 100, center_x, center_y, max_r + 100)
gradient.add_color_stop_rgba(0, 1, 1, 1, 0)
gradient.add_color_stop_rgba(0.8, 0, 0, 0, 0.1)
gradient.add_color_stop_rgba(1, 0, 0, 0, 0.6)
ctx.set_source(gradient)
ctx.rectangle(0, 0, width, height)
ctx.fill()
