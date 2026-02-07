import cairo
import math
import random

# Setup
width, height = 600, 600
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Swiss Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_swiss_module(ctx, x, y, size, angle, weight, color):
    """Draws a minimalist geometric unit inspired by Swiss typography blocks."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    
    # Primary bar
    ctx.rectangle(-size/2, -size/8, size, size/4)
    ctx.fill()
    
    # Accent line
    ctx.move_to(-size/2, size/2)
    ctx.line_to(size/2, size/2)
    ctx.stroke()
    
    ctx.restore()

# Parameters
center_x, center_y = width / 2, height / 2
rings = 14
segments = 40
golden_ratio = (1 + 5**0.5) / 2

# LAYER 1: The Underlying Ghost Grid (Atmospheric)
ctx.set_line_width(0.5)
for i in range(rings):
    r = (i / rings) * (width * 0.45)
    ctx.set_source_rgba(0.3, 0.3, 0.3, 0.2)
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()

# LAYER 2: Harmonic Divergence Logic
for i in range(1, rings):
    # Progressive scaling of radius using a power function for "decaying" periphery
    r_base = math.pow(i / rings, 0.8) * (width * 0.45)
    
    # Divergence Factor: Increases as we move outward
    divergence = (i / rings) * 0.5
    
    for j in range(segments):
        theta_base = (j / segments) * 2 * math.pi
        
        # Radial Distortion: Grid struggles against a fluid force
        # Modulate theta based on a sine wave influenced by radius
        distortion = math.sin(theta_base * 3 + (i * 0.2)) * divergence
        theta = theta_base + distortion
        
        # Calculate dynamic position
        x, y = polar_to_cartesian(center_x, center_y, r_base, theta)
        
        # Geometric Logic: Modular sizing
        module_size = (1.0 - (i / rings)) * 25 + 5
        
        # Color Interaction: Accented neutrals with vibrancy based on "velocity" (distortion)
        if random.random() > 0.92:
            # Vibrant Accent: International Orange / Vermillion
            color = (0.89, 0.24, 0.15, 0.9)
            line_w = 2.0
        else:
            # Swiss Neutral: Off-white to Light Grey
            val = 0.7 + (random.random() * 0.3)
            alpha = 0.4 + (0.5 * (1.0 - i/rings))
            color = (val, val, val, alpha)
            line_w = 0.7
            
        # Orientation: Tangential to the circle with slight jitter
        angle = theta + math.pi/2 + (random.uniform(-0.1, 0.1) * divergence)
        
        draw_swiss_module(ctx, x, y, module_size, angle, line_w, color)

# LAYER 3: High-Frequency Linear Connectors (The "Flow Field")
ctx.set_line_width(0.3)
for j in range(0, segments, 2):
    ctx.move_to(center_x, center_y)
    curr_theta = (j / segments) * 2 * math.pi
    
    # Draw a "distorted" ray
    points = 20
    for p in range(1, points):
        dist_ratio = p / points
        r_p = dist_ratio * (width * 0.5)
        # Apply the same distortion field to lines
        theta_p = curr_theta + math.sin(curr_theta * 3 + (p * 0.1)) * (dist_ratio * 0.4)
        px, py = polar_to_cartesian(center_x, center_y, r_p, theta_p)
        
        ctx.set_source_rgba(1, 1, 1, 0.15 * (1.0 - dist_ratio))
        ctx.line_to(px, py)
        
    ctx.stroke()

# LAYER 4: Focal Depth (Center Cluster)
# A high-density recursive core to anchor the composition
for k in range(12):
    r_core = k * 3
    ctx.set_source_rgba(0.9, 0.9, 0.9, 0.8)
    ctx.set_line_width(1.5)
    ctx.arc(center_x, center_y, r_core, 0, 2 * math.pi)
    if k % 3 == 0:
        ctx.stroke()
    else:
        # Subtle "Ticks"
        for tick in range(8):
            ta = (tick / 8) * 2 * math.pi
            tx, ty = polar_to_cartesian(center_x, center_y, r_core, ta)
            ctx.rectangle(tx-1, ty-1, 2, 2)
            ctx.fill()

# Final Texture: Random noise-like fine dots
for _ in range(400):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.3))
    ctx.rectangle(tx, ty, 0.5, 0.5)
    ctx.fill()

