import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def polar_transform(x, y, entropy=0.0):
    """
    Transforms normalized (0-1) grid coordinates into a distorted polar space.
    Adds 'entropy' which jitters the coordinates based on distance from center.
    """
    cx, cy = 0.5, 0.5
    dx, dy = x - cx, y - cy
    
    # Calculate radius and angle
    r = math.sqrt(dx*dx + dy*dy)
    theta = math.atan2(dy, dx)
    
    # Apply a rhythmic 'pulse' distortion
    r_mod = r + (math.sin(r * 20) * 0.02)
    # Apply entropy: more noise at the edges
    noise_factor = r * entropy
    r_mod += random.uniform(-noise_factor, noise_factor)
    theta += random.uniform(-noise_factor, noise_factor) * 0.5
    
    # Map back to screen coordinates
    # Center the radial system on the canvas
    screen_x = (width / 2) + (r_mod * math.cos(theta) * width * 0.8)
    screen_y = (height / 2) + (r_mod * math.sin(theta) * height * 0.8)
    
    return screen_x, screen_y

def draw_deconstructed_grid(cols, rows, entropy_level):
    """
    Draws a Swiss-inspired grid that transforms into atmospheric noise.
    """
    for i in range(cols + 1):
        u = i / cols
        
        # Draw the main "meridians" with variable line weight
        ctx.set_line_width(0.4 if i % 5 == 0 else 0.15)
        
        # Trace path segment by segment to allow for polar curvature
        first_point = True
        steps = 40
        for s in range(steps + 1):
            v = s / steps
            
            # Chromatic aberration logic: slight offset for R and B
            px, py = polar_transform(u, v, entropy_level * v)
            
            if first_point:
                ctx.move_to(px, py)
                first_point = False
            else:
                ctx.line_to(px, py)
        
        # Color leakage: faint cyan/magenta fringes
        if i % 10 == 0:
            ctx.set_source_rgba(0.0, 0.8, 1.0, 0.4) # Cyan
        elif i % 10 == 5:
            ctx.set_source_rgba(1.0, 0.1, 0.4, 0.4) # Magenta
        else:
            ctx.set_source_rgba(0.9, 0.9, 0.9, 0.6) # Off-white
            
        ctx.stroke()

def add_stippled_noise(density):
    """
    Adds granular texture to simulate low-res data noise and atmospheric diffusion.
    """
    for _ in range(density):
        # Focus noise in a ring around the center
        u, v = random.random(), random.random()
        r = math.sqrt((u-0.5)**2 + (v-0.5)**2)
        
        if random.random() < r: # Density increases with radius
            px, py = polar_transform(u, v, 0.05)
            
            # Tiny pixel-like squares
            ctx.rectangle(px, py, 0.8, 0.8)
            ctx.set_source_rgba(0.8, 0.8, 1.0, random.uniform(0.1, 0.5))
            ctx.fill()

def recursive_subdivision(x, y, w, h, depth):
    """
    Partitions the grid space recursively to create varied resolution.
    """
    if depth > 0 and random.random() > 0.4:
        # Split
        if random.random() > 0.5:
            recursive_subdivision(x, y, w/2, h, depth-1)
            recursive_subdivision(x+w/2, y, w/2, h, depth-1)
        else:
            recursive_subdivision(x, y, w, h/2, depth-1)
            recursive_subdivision(x, y+h/2, w, h/2, depth-1)
    else:
        # Draw a cell-specific detail
        px, py = polar_transform(x + w/2, y + h/2, 0.02)
        
        # Draw a tiny technical crosshair at the cell center
        size = 2.0
        ctx.set_line_width(0.3)
        ctx.set_source_rgba(1, 1, 1, 0.3)
        ctx.move_to(px - size, py)
        ctx.line_to(px + size, py)
        ctx.move_to(px, py - size)
        ctx.line_to(px, py + size)
        ctx.stroke()

# --- Execution ---

# 1. Background Grid (The systematic foundation)
draw_deconstructed_grid(40, 40, 0.02)

# 2. High-entropy breakdown (The "Noise")
add_stippled_noise(8000)

# 3. Structural elements (Swiss precision markers)
recursive_subdivision(0.2, 0.2, 0.6, 0.6, 4)

# 4. Focal Pulses (Concentrated energy sources)
for _ in range(3):
    pulse_x, pulse_y = random.uniform(0.3, 0.7), random.uniform(0.3, 0.7)
    for r_ring in range(3, 15, 3):
        ctx.set_line_width(0.1)
        ctx.set_source_rgba(1, 0.9, 0.2, 0.15) # Warm spectral glow
        
        steps = 100
        first = True
        for s in range(steps + 1):
            angle = (s / steps) * math.pi * 2
            # Map a small circle through the polar distortion
            offset_x = pulse_x + math.cos(angle) * (r_ring / 500)
            offset_y = pulse_y + math.sin(angle) * (r_ring / 500)
            px, py = polar_transform(offset_x, offset_y, 0.01)
            
            if first:
                ctx.move_to(px, py)
                first = False
            else:
                ctx.line_to(px, py)
        ctx.stroke()

# Final Polish: Centralized tension circle
ctx.set_line_width(0.5)
ctx.set_source_rgba(1, 1, 1, 0.8)
px, py = polar_transform(0.5, 0.5, 0)
ctx.arc(px, py, 5, 0, 2*math.pi)
ctx.stroke()

