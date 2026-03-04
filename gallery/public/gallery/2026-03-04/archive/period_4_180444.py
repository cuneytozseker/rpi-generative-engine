import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Obsidian
ctx.set_source_rgb(0.02, 0.02, 0.05)
ctx.paint()

def get_thermal_color(t, alpha=1.0):
    """Returns a thermal gradient color based on t (0.0 to 1.0)"""
    # Deep Blue -> Cyan -> Magenta -> Orange -> White
    if t < 0.25:
        # Blue to Cyan
        r, g, b = 0, t * 4, 0.5 + t * 2
    elif t < 0.5:
        # Cyan to Magenta
        r, g, b = (t - 0.25) * 4, 1.0 - (t - 0.25) * 4, 1.0
    elif t < 0.75:
        # Magenta to Orange
        r, g, b = 1.0, 0, 1.0 - (t - 0.5) * 4
    else:
        # Orange to White/Yellow
        r, g, b = 1.0, (t - 0.75) * 4, (t - 0.75) * 2
    
    return (r, g, b, alpha)

def draw_diffused_rect(ctx, x, y, w, h, t):
    """Draws a grid element with simulated diffusion/glow"""
    r, g, b, a = get_thermal_color(t, 0.1)
    
    # Draw glow layers
    for i in range(4, 0, -1):
        glow_size = i * 2
        ctx.set_source_rgba(r, g, b, 0.05 / i)
        ctx.rectangle(x - glow_size/2, y - glow_size/2, w + glow_size, h + glow_size)
        ctx.fill()
    
    # Draw core element
    ctx.set_source_rgba(r, g, b, 0.8)
    ctx.rectangle(x, y, w, h)
    ctx.fill()

# Main Compositional Parameters
center_x, center_y = width / 2, height / 2
rings = 42
segments = 72
max_radius = 350

# 1. LAYER: Base Polar Grid (Digital Entropy)
# Systematic but slightly warped
ctx.set_line_width(0.5)
for r_idx in range(rings):
    radius = (r_idx / rings) ** 1.2 * max_radius # Rhythmic expansion
    # Density factor: higher near center
    density = 1.0 - (radius / max_radius)
    
    for s_idx in range(segments):
        angle = (s_idx / segments) * 2 * math.pi
        
        # Stochastic displacement: rigid grid disrupted by organic warping
        noise_r = math.sin(angle * 5 + radius * 0.05) * 5
        noise_a = math.cos(radius * 0.1) * 0.02
        
        curr_r = radius + noise_r
        curr_a = angle + noise_a
        
        px = center_x + math.cos(curr_a) * curr_r
        py = center_y + math.sin(curr_a) * curr_r
        
        # Draw high-frequency "bitmapped" detail
        if random.random() < density * 0.6:
            size = random.uniform(0.5, 2.0)
            t = (1.0 - density) * 0.8 + random.uniform(0, 0.2)
            ctx.set_source_rgba(*get_thermal_color(t, 0.4))
            ctx.rectangle(px, py, size, size)
            ctx.fill()

# 2. LAYER: Modular Grid Subdivisions (Swiss Design)
# Concentric rectangular fragments transformed into polar space
for r_idx in range(5, rings, 4):
    radius = (r_idx / rings) * max_radius
    thickness = 8 * (1.0 - radius/max_radius) + 1
    
    for s_idx in range(0, segments, 6):
        # Create a block in polar coordinates
        angle_start = (s_idx / segments) * 2 * math.pi
        angle_end = ((s_idx + 3) / segments) * 2 * math.pi
        
        # Thermal intensity based on distance and segment
        t = abs(math.sin(angle_start * 2)) * (1.0 - radius/max_radius)
        
        # Drawing the "curved" rectangle segment
        ctx.new_path()
        ctx.arc(center_x, center_y, radius, angle_start, angle_end)
        ctx.arc_negative(center_x, center_y, radius + thickness, angle_end, angle_start)
        ctx.close_path()
        
        # Color based on thermal friction
        r, g, b, a = get_thermal_color(t, 0.7)
        ctx.set_source_rgba(r, g, b, a)
        ctx.fill_preserve()
        
        # Sharp stroke for "surgical precision"
        ctx.set_source_rgba(1, 1, 1, 0.3)
        ctx.set_line_width(0.3)
        ctx.stroke()

# 3. LAYER: Horizontal Pulse (Echoing Forms)
# This establishes the rhythmic sequence mentioned in the brief
for i in range(12):
    y_pos = 40 * i + 20
    freq = 0.02 + (i * 0.005)
    
    for x_pos in range(0, width, 10):
        # Interference pattern logic
        wave = math.sin(x_pos * freq) * 20
        dist_from_center = math.sqrt((x_pos - center_x)**2 + (y_pos + wave - center_y)**2)
        
        if dist_from_center < max_radius * 0.8:
            # Scale and alpha based on radial dispersion
            scale = (1.0 - dist_from_center / max_radius) * 4
            alpha = (1.0 - dist_from_center / max_radius) * 0.5
            
            t = 0.5 + 0.5 * math.sin(dist_from_center * 0.05 - i)
            
            ctx.set_source_rgba(*get_thermal_color(t, alpha))
            ctx.rectangle(x_pos, y_pos + wave, scale, scale * 0.5)
            ctx.fill()

# 4. LAYER: Spectral Hotspots (Incandescent Overlaps)
# Small, bright points where grids "interfere"
for _ in range(150):
    angle = random.uniform(0, math.pi * 2)
    dist = random.uniform(0, max_radius * 0.5)
    
    # Polar to cartesian
    hx = center_x + math.cos(angle) * dist
    hy = center_y + math.sin(angle) * dist
    
    # Hotspot glow
    radial_grad = cairo.RadialGradient(hx, hy, 0, hx, hy, random.uniform(5, 15))
    c1 = get_thermal_color(0.9, 0.6)
    c2 = get_thermal_color(0.7, 0.0)
    radial_grad.add_color_stop_rgba(0, *c1)
    radial_grad.add_color_stop_rgba(1, *c2)
    
    ctx.set_source(radial_grad)
    ctx.arc(hx, hy, 15, 0, 2 * math.pi)
    ctx.fill()

# Final Polish: Fine Grain Texture
for _ in range(2000):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0, 0.15))
    gx, gy = random.random() * width, random.random() * height
    ctx.rectangle(gx, gy, 0.7, 0.7)
    ctx.fill()

