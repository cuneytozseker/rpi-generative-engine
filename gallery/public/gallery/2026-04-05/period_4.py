import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep "Systemic" Cobalt/Black
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

# Constants
cx, cy = width / 2, height / 2
phi = (1 + 5**0.5) / 2  # Golden ratio for spacing
num_rings = 42
num_rays = 72
max_radius = min(width, height) * 0.8

def polar_to_cartesian(r, theta, distortion_factor=0):
    """Applies a radial distortion to the polar mapping."""
    # Modulate radius based on a combination of angle and base radius
    # creating a 'blooming' or 'breathing' grid effect
    r_mod = r * (1 + distortion_factor * math.sin(6 * theta + r * 0.02))
    x = cx + r_mod * math.cos(theta)
    y = cy + r_mod * math.sin(theta)
    return x, y

def draw_systemic_grid():
    # 1. THE RADIAL FIELD (Rays)
    ctx.set_line_width(0.4)
    for i in range(num_rays):
        angle = (i / num_rays) * 2 * math.pi
        
        # Determine color: mostly muted grey, occasional spectral accent
        if i % 12 == 0:
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.6) # Cyan pulse
            ctx.set_line_width(0.8)
        else:
            ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
            ctx.set_line_width(0.3)
            
        ctx.move_to(cx, cy)
        # Draw rays as distorted paths
        segments = 20
        for s in range(1, segments + 1):
            r = (s / segments) * max_radius
            # Distortion increases with distance from center
            distort = 0.15 * (r / max_radius)
            px, py = polar_to_cartesian(r, angle, distort)
            ctx.line_to(px, py)
        ctx.stroke()

    # 2. THE CONCENTRIC SCALE (Rings)
    # Using logarithmic/phi-based spacing for a Swiss-inspired progression
    current_r = 15
    for i in range(num_rings):
        # Progressively increase radius using phi
        current_r += 4 * (phi ** (i * 0.08))
        if current_r > max_radius: break
        
        alpha = 0.1 + (0.5 * (1 - current_r / max_radius))
        ctx.set_source_rgba(1, 1, 1, alpha)
        ctx.set_line_width(0.5 if i % 5 != 0 else 1.2)
        
        # Draw distorted circle
        steps = 200
        for s in range(steps + 1):
            theta = (s / steps) * 2 * math.pi
            distort = 0.12 * (current_r / max_radius)
            px, py = polar_to_cartesian(current_r, theta, distort)
            if s == 0:
                ctx.move_to(px, py)
            else:
                ctx.line_to(px, py)
        ctx.stroke()

    # 3. DATA ANOMALIES (Rectangular blocks mapped to polar grid)
    # This represents the "Typography as visual element"/Swiss block principle
    random.seed(42) # Deterministic randomness
    for _ in range(60):
        r_idx = random.uniform(20, max_radius)
        theta_idx = random.randint(0, num_rays) * (2 * math.pi / num_rays)
        
        # Block size
        bw = random.uniform(5, 25)
        bh = random.uniform(2, 8)
        
        # Coordinates
        distort = 0.15 * (r_idx / max_radius)
        bx, by = polar_to_cartesian(r_idx, theta_idx, distort)
        
        ctx.save()
        ctx.translate(bx, by)
        ctx.rotate(theta_idx + math.pi/2) # Align block to the radial ray
        
        # Color selection: High contrast highlights
        chance = random.random()
        if chance > 0.9:
            ctx.set_source_rgba(1.0, 0.2, 0.4, 0.9) # Vibrant Pink/Red "Event"
        elif chance > 0.7:
            ctx.set_source_rgba(0.0, 1.0, 0.8, 0.7) # Bright Mint
        else:
            ctx.set_source_rgba(1, 1, 1, 0.8) # Technical White
            
        ctx.rectangle(-bw/2, -bh/2, bw, bh)
        ctx.fill()
        ctx.restore()

    # 4. ATMOSPHERIC DIFFUSION (Central Pulse)
    # Creating a radial gradient to soften the center
    gradient = cairo.RadialGradient(cx, cy, 0, cx, cy, max_radius * 0.5)
    gradient.add_color_stop_rgba(0, 0, 0.8, 1, 0.15) # Soft blue core
    gradient.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(gradient)
    ctx.arc(cx, cy, max_radius, 0, 2 * math.pi)
    ctx.fill()

    # 5. HAIRLINE PRECISION OVERLAY
    # Fine diamond-like connections between certain nodes
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.set_line_width(0.2)
    for i in range(0, num_rays, 4):
        theta1 = i * (2 * math.pi / num_rays)
        theta2 = (i + 4) * (2 * math.pi / num_rays)
        for r_step in range(50, int(max_radius), 60):
            x1, y1 = polar_to_cartesian(r_step, theta1, 0.1)
            x2, y2 = polar_to_cartesian(r_step + 30, theta2, 0.1)
            ctx.move_to(x1, y1)
            ctx.line_to(x2, y2)
            ctx.stroke()

draw_systemic_grid()

# Final frame border (Swiss Minimalist Detail)
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()
