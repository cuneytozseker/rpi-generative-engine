import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for "Digital Archaeology" feel
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_truchet_tile(x, y, size, variant, weight, color, alpha):
    """Draws a modified Smith-style Truchet tile with arcs or diagonals."""
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(weight)
    
    r = size / 2
    if variant == 0:
        # Top-left and bottom-right arcs
        ctx.arc(x, y, r, 0, math.pi / 2)
        ctx.stroke()
        ctx.arc(x + size, y + size, r, math.pi, 1.5 * math.pi)
        ctx.stroke()
    else:
        # Top-right and bottom-left arcs
        ctx.arc(x + size, y, r, math.pi / 2, math.pi)
        ctx.stroke()
        ctx.arc(x, y + size, r, 1.5 * math.pi, 2 * math.pi)
        ctx.stroke()

def draw_glitch_rects(x, y, size, density):
    """Adds 'digital noise' through dithered rectangular fragments."""
    for _ in range(density):
        if random.random() > 0.5:
            w = random.uniform(1, size * 0.2)
            h = random.uniform(1, 2)
            ctx.set_source_rgba(0.4, 0.9, 1.0, random.uniform(0.1, 0.4))
            ctx.rectangle(x + random.uniform(0, size), y + random.uniform(0, size), w, h)
            ctx.fill()

# Parameters
base_grid = 40
layers = 3
center_x, center_y = width / 2, height / 2

# Colors
color_white = (0.95, 0.95, 0.95)
color_cyan = (0.0, 0.8, 1.0)
color_dark_blue = (0.1, 0.2, 0.4)

# Multi-layered Generation
for layer in range(layers):
    # Each layer has a different scale and "kinetic energy"
    scale_mod = [1.0, 0.5, 2.0][layer]
    current_grid = int(base_grid * scale_mod)
    alpha = [0.1, 0.4, 0.05][layer]
    
    for i in range(-1, width // current_grid + 1):
        for j in range(-1, height // current_grid + 1):
            x = i * current_grid
            y = j * current_grid
            
            # Calculate distance from center for "Centrifugal Expansion"
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            norm_dist = dist / (width / 2)
            
            # Entropy factor: tiles further away or very close are more chaotic
            entropy = math.sin(norm_dist * math.pi) 
            
            # Skip tiles randomly based on density modulation
            if random.random() < (0.1 * layer):
                continue
            
            # Displacement logic (Flow field influence)
            offset_x = math.cos(norm_dist * 5) * 5 * layer
            offset_y = math.sin(norm_dist * 5) * 5 * layer
            
            # Determine tile variant (0 or 1)
            variant = 1 if (random.random() > 0.5) else 0
            
            # Line weight varies by entropy
            weight = (1.5 + (1.0 - norm_dist) * 3) / scale_mod
            
            # Color selection: Mostly white, occasional cyan "interruptions"
            current_color = color_white
            if random.random() < 0.05:
                current_color = color_cyan
                weight *= 2
            elif layer == 2:
                current_color = color_dark_blue

            # Draw the main tile
            draw_truchet_tile(x + offset_x, y + offset_y, current_grid, variant, weight, current_color, alpha)
            
            # Add archaeology texture/glitch in high-entropy zones
            if entropy > 0.7 and layer == 1:
                draw_glitch_rects(x, y, current_grid, int(5 * entropy))

# Final Systematic Overlay - Orthogonal Grid Fragments
ctx.set_line_width(0.5)
for k in range(0, width, base_grid * 2):
    # Vertical "Scanning" lines
    opacity = random.uniform(0.05, 0.15)
    ctx.set_source_rgba(0.0, 0.8, 1.0, opacity)
    ctx.move_to(k, 0)
    ctx.line_to(k, height)
    ctx.stroke()

# Add a subtle "HUD" or architectural framing element
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.6)
ctx.set_line_width(1)
ctx.rectangle(40, 40, 120, 2) # Top left accent
ctx.fill()
ctx.rectangle(width-160, height-42, 120, 2) # Bottom right accent
ctx.fill()

# Centrifugal blur effect simulation (subtle lines)
ctx.set_line_width(0.3)
for _ in range(40):
    angle = random.uniform(0, math.pi * 2)
    length = random.uniform(100, 300)
    start_r = random.uniform(0, 50)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.move_to(center_x + math.cos(angle)*start_r, center_y + math.sin(angle)*start_r)
    ctx.line_to(center_x + math.cos(angle)*length, center_y + math.sin(angle)*length)
    ctx.stroke()

