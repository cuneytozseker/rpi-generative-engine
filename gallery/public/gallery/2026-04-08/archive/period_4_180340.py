import cairo
import math
import random

# Setup: Systematic Radiance - Polar Swiss Grid Distortion
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep neutral field
ctx.set_source_rgb(0.02, 0.02, 0.03) 
ctx.paint()

def polar_to_cartesian(r, theta, center_x, center_y):
    x = center_x + r * math.cos(theta)
    y = center_y + r * math.sin(theta)
    return x, y

def draw_systematic_radiance():
    cx, cy = width / 2, height / 2
    
    # Configuration
    rings = 45
    segments = 72
    max_radius = min(width, height) * 0.45
    
    # 1. Subtle Radial Underlay (Atmospheric depth)
    ctx.set_line_width(0.3)
    for i in range(rings):
        # Non-linear spacing for the rings (exponential progression)
        r = max_radius * math.pow(i / rings, 1.5)
        alpha = 0.1 + (0.3 * (1 - i / rings))
        ctx.set_source_rgba(0.4, 0.5, 0.7, alpha)
        ctx.arc(cx, cy, r, 0, 2 * math.pi)
        ctx.stroke()

    # 2. Distorted Swiss Grid Logic
    # We treat the polar space as a Cartesian grid (r, theta) and apply distortions
    for i in range(rings):
        # Parametric progression for radius
        r_base = max_radius * math.pow(i / rings, 1.2)
        
        for j in range(segments):
            theta_base = (j / segments) * 2 * math.pi
            
            # Apply Sinusoidal Distortion to create the "wave-like" repetition
            # Frequency increases toward the periphery
            distortion = math.sin(i * 0.2 + j * 0.1) * (i * 0.5)
            r = r_base + distortion
            
            # Polar Mapping
            px, py = polar_to_cartesian(r, theta_base, cx, cy)
            
            # Draw Radial Hairlines
            if i < rings - 1:
                r_next = max_radius * math.pow((i + 1) / rings, 1.2) + math.sin((i+1) * 0.2 + j * 0.1) * ((i+1) * 0.5)
                nx, ny = polar_to_cartesian(r_next, theta_base, cx, cy)
                
                ctx.set_source_rgba(0.9, 0.9, 1.0, 0.15)
                ctx.set_line_width(0.4)
                ctx.move_to(px, py)
                ctx.line_to(nx, ny)
                ctx.stroke()

            # Draw Circumferential Segments
            if j < segments:
                theta_next = ((j + 1) / segments) * 2 * math.pi
                distortion_next = math.sin(i * 0.2 + (j + 1) * 0.1) * (i * 0.5)
                rx, ry = polar_to_cartesian(r_base + distortion_next, theta_next, cx, cy)
                
                ctx.set_source_rgba(1.0, 1.0, 1.0, 0.2)
                ctx.set_line_width(0.3)
                ctx.move_to(px, py)
                ctx.line_to(rx, ry)
                ctx.stroke()

            # 3. Geometric Intersections (The "Swiss" technical markers)
            # Only draw on specific intervals to create hierarchy
            if i % 4 == 0 and j % 6 == 0:
                # Luminous Accents at intersections
                intensity = 1.0 - (i / rings)
                
                # Draw a technical "cross" marker
                size = 2 + (i * 0.05)
                ctx.set_source_rgba(1.0, 1.0, 1.0, 0.8 * intensity)
                ctx.set_line_width(0.5)
                ctx.move_to(px - size, py); ctx.line_to(px + size, py)
                ctx.move_to(px, py - size); ctx.line_to(px, py + size)
                ctx.stroke()
                
                # Chroma-Saturated Gradient effect (stochastic density)
                if random.random() > 0.7:
                    # Choose a vibrant accent color (Cyan or Magenta)
                    if j % 12 == 0:
                        ctx.set_source_rgba(0.0, 0.8, 1.0, 0.6) # Cyan
                    else:
                        ctx.set_source_rgba(1.0, 0.0, 0.4, 0.6) # Magenta
                    
                    ctx.arc(px, py, 1.5, 0, 2 * math.pi)
                    ctx.fill()

    # 4. Central Core (The "Nucleus")
    # High-density stochastic cluster at the center
    for _ in range(120):
        ang = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0, 25)
        # Non-linear distribution toward center
        dist = math.pow(dist/25, 2) * 25 
        xx, yy = polar_to_cartesian(dist, ang, cx, cy)
        
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.6))
        ctx.arc(xx, yy, random.uniform(0.2, 0.8), 0, 2 * math.pi)
        ctx.fill()

    # 5. Framing: Bilateral Symmetry Elements
    # Minimalist bars for Swiss alignment
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.rectangle(30, 20, 1, height - 40)
    ctx.rectangle(width - 31, 20, 1, height - 40)
    ctx.fill()
    
    # Typography simulation (Technical labels)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    for i in range(4):
        y_pos = 50 + i * 100
        ctx.set_line_width(1)
        ctx.move_to(25, y_pos)
        ctx.line_to(40, y_pos)
        ctx.stroke()

draw_systematic_radiance()
