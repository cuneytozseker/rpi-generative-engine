import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Dark neutral field
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_structural_diffusion():
    cx, cy = width / 2, height / 2
    
    # Palette
    ultramarine = (0.07, 0.2, 0.9, 0.4)
    amber = (1.0, 0.65, 0.0, 0.7)
    white = (0.9, 0.9, 0.9, 0.8)
    
    # 1. UNDERLYING RECURSIVE NETWORK (ULTRAMARINE)
    # Creating a base of connectivity using non-linear radial progression
    rings = 15
    segments = 40
    ctx.set_line_width(0.5)
    
    for i in range(rings):
        # Golden ratio-ish expansion for the radius
        r = math.pow(i / rings, 1.2) * (width * 0.45)
        r_next = math.pow((i + 1) / rings, 1.2) * (width * 0.45)
        
        for s in range(segments):
            theta = (s / segments) * 2 * math.pi
            # Apply radial distortion (sinusoidal modulation of the grid)
            distortion = math.sin(theta * 5 + i * 0.5) * 15
            r_distorted = r + distortion
            
            x, y = polar_to_cartesian(cx, cy, r_distorted, theta)
            
            # Connect to next segment (arc)
            theta_next = ((s + 1) / segments) * 2 * math.pi
            x_n, y_n = polar_to_cartesian(cx, cy, r + math.sin(theta_next * 5 + i * 0.5) * 15, theta_next)
            
            ctx.set_source_rgba(*ultramarine)
            ctx.move_to(x, y)
            ctx.line_to(x_n, y_n)
            ctx.stroke()
            
            # Radial connections with probability (Recursive network feel)
            if random.random() > 0.6:
                x_outer, y_outer = polar_to_cartesian(cx, cy, r_next, theta)
                ctx.set_source_rgba(0.07, 0.2, 0.9, 0.15)
                ctx.move_to(x, y)
                ctx.line_to(x_outer, y_outer)
                ctx.stroke()

    # 2. SWISS GRID ELEMENTS (SYSTEMATIC BLOCKS)
    # Precise, modulated blocks following the polar transformation
    ctx.set_line_width(1.5)
    for i in range(4, rings, 2):
        r = math.pow(i / rings, 1.2) * (width * 0.45)
        block_width = (i / rings) * 12
        
        for s in range(0, segments, 4):
            theta = (s / segments) * 2 * math.pi + (i * 0.1) # Spiral phase shift
            x, y = polar_to_cartesian(cx, cy, r, theta)
            
            ctx.save()
            ctx.translate(x, y)
            ctx.rotate(theta + math.pi/2)
            
            # High-contrast interaction
            if (i + s) % 3 == 0:
                ctx.set_source_rgba(*amber)
                ctx.rectangle(-block_width/2, -1, block_width, 2)
            else:
                ctx.set_source_rgba(*white)
                ctx.rectangle(-block_width/2, -0.5, block_width, 1)
            ctx.fill()
            ctx.restore()

    # 3. MOIRÉ INTERFERENCE LAYER (HIGH-FREQUENCY LINES)
    # Extreme line-weight modulation creating optical mixing
    ctx.set_line_width(0.15)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    for s in range(segments * 4):
        theta = (s / (segments * 4)) * 2 * math.pi
        # Varying line lengths creates radial depth
        length_mod = math.sin(theta * 12) * 40 + (width * 0.3)
        x1, y1 = polar_to_cartesian(cx, cy, 20, theta)
        x2, y2 = polar_to_cartesian(cx, cy, length_mod, theta)
        
        ctx.move_to(x1, y1)
        ctx.line_to(x2, y2)
        ctx.stroke()

    # 4. DIFFUSION TEXTURE (DIGITAL DITHERING)
    # Small bitmapped-style dots clustered around structural nodes
    for _ in range(1200):
        # Favoring the center-outward expansion
        angle = random.uniform(0, 2 * math.pi)
        dist = math.pow(random.random(), 0.7) * (width * 0.4)
        dot_x, dot_y = polar_to_cartesian(cx, cy, dist, angle)
        
        # Color shift based on distance
        alpha = random.uniform(0.1, 0.6)
        if random.random() > 0.8:
            ctx.set_source_rgba(1.0, 0.7, 0.1, alpha) # Amber dither
        else:
            ctx.set_source_rgba(0.9, 0.9, 1.0, alpha * 0.5) # White/Blue dither
            
        size = random.uniform(0.5, 1.8)
        ctx.arc(dot_x, dot_y, size, 0, 2 * math.pi)
        ctx.fill()

    # 5. AXIAL DIRECTIONAL OVERLAYS
    # Large transparent gradients to define "Spectral Shift"
    # Using multiple strokes to simulate a radial gradient mass
    for r_mass in range(50, 150, 2):
        alpha_mass = (1 - (r_mass / 150)) * 0.05
        ctx.set_source_rgba(0.0, 0.4, 1.0, alpha_mass) # Ultramarine glow
        ctx.arc(cx - 40, cy - 40, r_mass, 0, 2 * math.pi)
        ctx.fill()
        
        ctx.set_source_rgba(1.0, 0.5, 0.0, alpha_mass * 0.8) # Amber glow
        ctx.arc(cx + 80, cy + 60, r_mass * 0.6, 0, 2 * math.pi)
        ctx.fill()

# Execution
draw_structural_diffusion()
