import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Indigo/Black for "Digital Entropy"
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width // 2, height // 2
rings = 14
segments = 36
phi = (1 + math.sqrt(5)) / 2  # Golden ratio for rhythmic spacing

def polar_to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

def draw_glitch_rect(x, y, w, h, angle, color, alpha):
    """Draws a Swiss-style rectangle with rotational alignment and alpha."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.rectangle(-w/2, -h/2, w, h)
    ctx.fill()
    ctx.restore()

# 1. LAYER ONE: Atmospheric Diffused Gradient (The "Spectral" base)
# Simulating a soft-masking volume transition
for i in range(100):
    radius = random.uniform(50, 250)
    angle = random.uniform(0, math.pi * 2)
    px, py = polar_to_cartesian(radius, angle)
    
    # Transition between warm (orange-red) and cool (cyan) based on distance
    dist_norm = radius / 250
    ctx.set_source_rgba(1.0 - dist_norm, 0.2, dist_norm, 0.03)
    ctx.arc(px, py, 40 * (1 - dist_norm), 0, 2 * math.pi)
    ctx.fill()

# 2. LAYER TWO: The Progressive Grid (Swiss Structure)
# Transformation of a Cartesian grid into Polar space with radial distortion
for r_idx in range(1, rings):
    # Logarithmic spacing for "rhythmic progression"
    base_radius = 40 * math.pow(r_idx, 0.85)
    
    # Entropy increases with radius
    entropy_factor = (r_idx / rings) ** 2
    
    for s_idx in range(segments):
        theta = (s_idx / segments) * 2 * math.pi
        
        # Stochastic displacement (jitter)
        jitter_r = random.uniform(-10, 10) * entropy_factor
        jitter_theta = random.uniform(-0.1, 0.1) * entropy_factor
        
        r = base_radius + jitter_r
        current_theta = theta + jitter_theta
        
        px, py = polar_to_cartesian(r, current_theta)
        
        # Geometric unit: A thin vertical bar, rotated to point toward center
        # following the "Polar coordinate transformation of Swiss grid"
        bar_w = 2 + (5 * (1 - entropy_factor))
        bar_h = 10 + (20 * entropy_factor)
        
        # Color logic: Monochromatic white with varying alpha for depth
        alpha = 0.8 - (entropy_factor * 0.5)
        draw_glitch_rect(px, py, bar_w, bar_h, current_theta + math.pi/2, (1, 1, 1), alpha)
        
        # 3. LAYER THREE: "Echoes" and Connections
        # Draw occasional radial lines to suggest a skeletal structure
        if s_idx % 4 == 0 and r_idx > 2:
            ctx.set_line_width(0.5)
            ctx.set_source_rgba(0.8, 0.9, 1.0, 0.2 * (1 - entropy_factor))
            prev_r = 40 * math.pow(r_idx - 1, 0.85)
            x_prev, y_prev = polar_to_cartesian(prev_r, current_theta)
            ctx.move_to(x_prev, y_prev)
            ctx.line_to(px, py)
            ctx.stroke()

# 4. LAYER FOUR: Fragmented Disintegration (Glitch Bits)
# High-frequency clusters near the "edges" of the system
for _ in range(120):
    r = random.uniform(150, 300)
    theta = random.uniform(0, math.pi * 2)
    # Concentration along certain "glitch" axes
    if random.random() > 0.7:
        px, py = polar_to_cartesian(r, theta)
        size = random.uniform(1, 4)
        
        # Bitmapped precision look (square fragments)
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.3, 0.9))
        ctx.rectangle(px, py, size, size)
        ctx.fill()

# 5. FINAL ACCENT: The "Seed"
# A precise, central geometric hierarchy
ctx.set_line_width(1.5)
ctx.set_source_rgba(1, 1, 1, 1)
ctx.arc(center_x, center_y, 5, 0, 2 * math.pi)
ctx.stroke()

# Subtle crosshairs for Swiss precision
ctx.set_line_width(0.5)
ctx.move_to(center_x - 20, center_y)
ctx.line_to(center_x + 20, center_y)
ctx.move_to(center_x, center_y - 20)
ctx.line_to(center_x, center_y + 20)
ctx.stroke()

