import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian Void
ctx.set_source_rgb(0.01, 0.01, 0.02)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_distorted_grid(cx, cy, num_rings, num_rays, rotation_offset):
    """Generates a polar grid with non-linear radial distortion."""
    
    # Mathematical Constants for the 'Field'
    distortion_strength = 25.0
    frequency = 6.0
    
    # 1. Subtle Radial Glow (Atmospheric Diffusion)
    for i in range(5):
        alpha = 0.03 - (i * 0.005)
        ctx.set_source_rgba(0.2, 0.4, 1.0, alpha)
        ctx.arc(cx, cy, 100 + i * 40, 0, 2 * math.pi)
        ctx.fill()

    # 2. Parametric Rings (The 'Rigidity')
    for i in range(num_rings):
        r_base = (i + 1) * (max(width, height) / (num_rings * 1.2))
        
        ctx.new_path()
        points = 200
        for p in range(points + 1):
            theta = (p / points) * 2 * math.pi
            # Apply distortion: r varies based on angle and distance
            r_distorted = r_base + math.sin(theta * frequency + rotation_offset) * distortion_strength
            # Secondary interference
            r_distorted += math.cos(theta * 3 - rotation_offset * 2) * (distortion_strength * 0.5)
            
            x, y = polar_to_cartesian(cx, cy, r_distorted, theta)
            if p == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        
        # Swiss Precision: Varying line weights
        if i % 4 == 0:
            ctx.set_line_width(0.8)
            ctx.set_source_rgba(0.7, 0.8, 1.0, 0.6)
        else:
            ctx.set_line_width(0.2)
            ctx.set_source_rgba(0.4, 0.5, 0.7, 0.3)
        ctx.stroke()

    # 3. Intersecting Vectors (The 'Rays')
    for i in range(num_rays):
        angle = (i / num_rays) * 2 * math.pi + rotation_offset
        
        ctx.new_path()
        steps = 50
        for s in range(steps):
            r_curr = (s / steps) * (width * 0.8)
            # Rays bend slightly towards the 'gravity' of the distortion
            angle_distorted = angle + math.sin(r_curr * 0.01) * 0.1
            x, y = polar_to_cartesian(cx, cy, r_curr, angle_distorted)
            if s == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        
        ctx.set_line_width(0.15)
        ctx.set_source_rgba(0.0, 0.8, 1.0, 0.4)
        ctx.stroke()

    # 4. Saturated Hotspots (The 'Spectral Data')
    # Placing points where specific mathematical thresholds are met
    random.seed(42)
    for _ in range(12):
        r_rand = random.uniform(50, 220)
        a_rand = random.uniform(0, 2 * math.pi)
        hx, hy = polar_to_cartesian(cx, cy, r_rand, a_rand)
        
        # Draw glowing point
        for layer in range(6):
            rad = 8 - layer
            alpha = 0.1 + (layer * 0.15)
            # Alternating between Cyan and Hot Magenta
            if _ % 2 == 0:
                ctx.set_source_rgba(0.0, 1.0, 0.9, alpha)
            else:
                ctx.set_source_rgba(1.0, 0.1, 0.4, alpha)
            ctx.arc(hx, hy, rad * 0.8, 0, 2 * math.pi)
            ctx.fill()
            
        # Add tiny technical 'labels' (Swiss Minimalist)
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.set_line_width(0.5)
        ctx.move_to(hx + 5, hy - 5)
        ctx.line_to(hx + 15, hy - 15)
        ctx.line_to(hx + 30, hy - 15)
        ctx.stroke()

def draw_brutalist_accents():
    """Adds sharp, high-contrast geometric interruptions."""
    # Vertical Swiss scale on the right
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.rectangle(width - 40, 40, 2, height - 80)
    ctx.fill()
    
    for i in range(0, height - 80, 20):
        ctx.set_source_rgba(1, 1, 1, 0.4)
        ctx.move_to(width - 40, 40 + i)
        ctx.line_to(width - 30, 40 + i)
        ctx.set_line_width(0.5)
        ctx.stroke()

    # Asymmetric Focal Block
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.rectangle(60, 60, 4, 4)
    ctx.fill()
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(0.5)
    ctx.move_to(62, 0)
    ctx.line_to(62, height)
    ctx.stroke()

# Main Execution
# Off-center focal point for Swiss asymmetry
center_x, center_y = width * 0.45, height * 0.55

# Multiple layers for depth
draw_distorted_grid(center_x, center_y, num_rings=30, num_rays=72, rotation_offset=0.2)
draw_brutalist_accents()

# Final subtle overlay texture: noise-like grain using tiny arcs
for _ in range(400):
    nx = random.uniform(0, width)
    ny = random.uniform(0, height)
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.arc(nx, ny, 0.3, 0, 2 * math.pi)
    ctx.fill()

