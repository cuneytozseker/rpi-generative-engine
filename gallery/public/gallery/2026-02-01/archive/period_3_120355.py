import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_to_cartesian(cx, cy, r, angle):
    return cx + r * math.cos(angle), cy + r * math.sin(angle)

def draw_computational_evolution():
    cx, cy = width / 2, height / 2
    
    # 1. THE GRID BASE: Radial distortion of a Swiss grid
    # We map a rectangular coordinate system (u, v) into (radius, theta)
    rows = 40
    cols = 60
    max_radius = min(width, height) * 0.45
    
    # Create interference layers
    for layer in range(3):
        ctx.set_line_width(0.3 + (layer * 0.2))
        alpha = 0.2 + (layer * 0.2)
        
        for i in range(rows):
            # Progressive serialism: shift the "seed" for each row
            row_offset = math.sin(i * 0.1 + layer) * 10
            
            for j in range(cols):
                # Normalize coordinates (0.0 to 1.0)
                u = i / rows
                v = j / cols
                
                # Polar transformation with harmonic distortion
                # The radius is modulated by the column index to create the "fan"
                # The angle is modulated by the row index to create the "rotation"
                angle = (v * 2 * math.pi) + (u * math.pi * 0.5)
                radius = (u * max_radius) + (math.cos(v * math.pi * 4) * 15 * u)
                
                x, y = polar_to_cartesian(cx, cy, radius, angle)
                
                # Draw the "Cellular" nodes
                if j % 4 == 0:
                    # High-contrast monochromatic foundation
                    ctx.set_source_rgba(0.9, 0.9, 1.0, alpha)
                    ctx.rectangle(x, y, 1.5, 1.5)
                    ctx.fill()
                
                # Vector networks (connecting lines)
                if j < cols - 1:
                    next_v = (j + 1) / cols
                    next_angle = (next_v * 2 * math.pi) + (u * math.pi * 0.5)
                    next_radius = (u * max_radius) + (math.cos(next_v * math.pi * 4) * 15 * u)
                    nx, ny = polar_to_cartesian(cx, cy, next_radius, next_angle)
                    
                    ctx.set_source_rgba(0.8, 0.8, 0.9, alpha * 0.5)
                    ctx.move_to(x, y)
                    ctx.line_to(nx, ny)
                    ctx.stroke()

    # 2. DENSITY MODULATION: Halftone/Dither patterns
    # Creating a visual texture that mimics digital artifacts
    for _ in range(2000):
        # Sample points within the system
        r_samp = random.uniform(50, max_radius)
        a_samp = random.uniform(0, math.pi * 2)
        
        # Distort the sampling to cluster in specific bands
        r_samp += math.sin(a_samp * 8) * 20
        
        px, py = polar_to_cartesian(cx, cy, r_samp, a_samp)
        
        # Density check (higher density towards the outer edge)
        if random.random() < (r_samp / max_radius):
            ctx.set_source_rgba(1, 1, 1, 0.4)
            ctx.rectangle(px, py, 0.8, 0.8)
            ctx.fill()

    # 3. SPECTRAL ACCENTS: Luminous clusters
    # Localized bursts of color representing emergent growth
    colors = [
        (0.0, 0.8, 1.0), # Cyan
        (1.0, 0.0, 0.5), # Magenta
        (0.4, 1.0, 0.2)  # Neon Green
    ]
    
    for _ in range(12):
        target_angle = random.uniform(0, math.pi * 2)
        target_radius = random.uniform(100, max_radius)
        tx, ty = polar_to_cartesian(cx, cy, target_radius, target_angle)
        
        clr = random.choice(colors)
        
        # Radial "light" bloom
        for r_offset in range(5):
            ctx.set_source_rgba(clr[0], clr[1], clr[2], 0.15 - (r_offset * 0.03))
            ctx.arc(tx, ty, 2 + r_offset * 4, 0, 2 * math.pi)
            ctx.fill()
            
        # The core "data point"
        ctx.set_source_rgb(1, 1, 1)
        ctx.arc(tx, ty, 1.2, 0, 2 * math.pi)
        ctx.fill()

    # 4. SWISS HIERARCHY: Structural Vector Overlays
    # Adding precise, razor-sharp lines to ground the composition
    ctx.set_line_width(0.5)
    ctx.set_source_rgba(1, 1, 1, 0.8)
    
    # Draw cross-hair markers at mathematical intervals
    marker_dist = 60
    for i in range(-5, 6):
        for j in range(-4, 5):
            mx, my = cx + i * marker_dist, cy + j * marker_dist
            # Only draw if within a certain distance from center
            if math.sqrt((mx-cx)**2 + (my-cy)**2) < max_radius * 1.2:
                ctx.move_to(mx - 3, my)
                ctx.line_to(mx + 3, my)
                ctx.move_to(mx, my - 3)
                ctx.line_to(mx, my + 3)
                ctx.stroke()

    # Final "Scanning" line (Temporal movement hint)
    ctx.set_line_width(1.0)
    ctx.set_source_rgba(0, 0.8, 1.0, 0.4)
    scan_angle = math.pi * 0.25
    sx, sy = polar_to_cartesian(cx, cy, max_radius * 1.1, scan_angle)
    ctx.move_to(cx, cy)
    ctx.line_to(sx, sy)
    ctx.stroke()

# Execution
draw_computational_evolution()
