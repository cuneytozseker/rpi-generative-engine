import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format for radial symmetry
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal/Cobalt hybrid
ctx.set_source_rgb(0.05, 0.07, 0.1)
ctx.paint()

def polar_to_cartesian(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)

def draw_grid_layer(ctx, cx, cy, rings, slices, rotation_offset, distortion_factor, alpha, color_mode="neutral"):
    """
    Generates a polar-mapped Swiss grid with radial distortion.
    """
    max_radius = min(width, height) * 0.45
    
    # 1. Draw Radial Ribs (Slices)
    for s in range(slices):
        angle = (s / slices) * (2 * math.pi) + rotation_offset
        
        ctx.move_to(cx, cy)
        for r_step in range(10, int(max_radius), 5):
            # Apply radial distortion: radius expands and contracts based on angle
            distorted_r = r_step * (1 + distortion_factor * math.sin(angle * 4 + r_step * 0.02))
            
            x, y = polar_to_cartesian(cx, cy, distorted_r, angle)
            ctx.line_to(x, y)
        
        # Spectral transition based on angle/density
        if color_mode == "spectral":
            r_val = 0.2 + 0.5 * math.sin(angle)
            g_val = 0.4 + 0.4 * math.cos(angle * 0.5)
            b_val = 0.9
            ctx.set_source_rgba(r_val, g_val, b_val, alpha * 0.8)
        else:
            ctx.set_source_rgba(0.9, 0.9, 0.9, alpha)
            
        ctx.set_line_width(0.3)
        ctx.stroke()

    # 2. Draw Concentric Rings with Stochastically Perturbed Connectivity
    for r_idx in range(1, rings):
        r_base = (r_idx / rings) * max_radius
        
        ctx.new_path()
        for s in range(slices + 1):
            angle = (s / slices) * (2 * math.pi) + rotation_offset
            
            # Interference logic: distortion shifts based on ring index
            distortion = distortion_factor * math.sin(angle * 6 + r_base * 0.05)
            r_final = r_base * (1 + distortion)
            
            x, y = polar_to_cartesian(cx, cy, r_final, angle)
            
            if s == 0:
                ctx.move_to(x, y)
            else:
                ctx.line_to(x, y)
        
        # Line weight modulation based on radius (Swiss hierarchy)
        weight = 0.5 if r_idx % 4 == 0 else 0.15
        ctx.set_line_width(weight)
        ctx.stroke()

def draw_intersections(ctx, cx, cy, rings, slices, rotation_offset, distortion_factor):
    """
    Adds geometric 'data nodes' at grid intersections to simulate bitmapped dither.
    """
    max_radius = min(width, height) * 0.45
    for r_idx in range(4, rings, 4):
        r_base = (r_idx / rings) * max_radius
        for s in range(0, slices, 2):
            angle = (s / slices) * (2 * math.pi) + rotation_offset
            distortion = distortion_factor * math.sin(angle * 6 + r_base * 0.05)
            r_final = r_base * (1 + distortion)
            x, y = polar_to_cartesian(cx, cy, r_final, angle)
            
            # Small Brutalist squares instead of circles
            size = random.uniform(0.5, 2.0)
            ctx.rectangle(x - size/2, y - size/2, size, size)
            ctx.set_source_rgba(1, 1, 1, 0.7)
            ctx.fill()

# --- Execution ---

cx, cy = width / 2, height / 2

# Layer 1: Background Atmospheric Grid (Subtle Moire)
draw_grid_layer(ctx, cx, cy, rings=40, slices=60, rotation_offset=0, 
                distortion_factor=0.05, alpha=0.1)

# Layer 2: Secondary Offset Grid (Creates Interference)
draw_grid_layer(ctx, cx, cy, rings=35, slices=55, rotation_offset=math.pi/30, 
                distortion_factor=0.08, alpha=0.15)

# Layer 3: The Primary "Spectral" Structural Grid
draw_grid_layer(ctx, cx, cy, rings=25, slices=90, rotation_offset=-math.pi/15, 
                distortion_factor=0.12, alpha=0.4, color_mode="spectral")

# Layer 4: High-Density Nodes (Stochastic Perturbation)
draw_intersections(ctx, cx, cy, rings=25, slices=90, rotation_offset=-math.pi/15, 
                   distortion_factor=0.12)

# Layer 5: Typographic/Modular Elements (Swiss Precision)
# Adding "Ghost" shapes through clipping and repetition
for i in range(5):
    ctx.set_source_rgba(1, 1, 1, 0.05)
    size = 100 + i * 40
    ctx.set_line_width(0.5)
    ctx.arc(cx, cy, size, 0, math.pi * 0.5) # Quarter circles
    ctx.stroke()

# Final Polish: Asymmetric Swiss Layout Element
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.move_to(20, height - 40)
ctx.show_text("POLAR_INTERFERENCE // REV_04")
ctx.move_to(20, height - 25)
ctx.set_line_width(1)
ctx.line_to(150, height - 25)
ctx.stroke()

# Create a small "Balance" element in the top right
ctx.rectangle(width - 50, 40, 30, 2)
ctx.fill()
