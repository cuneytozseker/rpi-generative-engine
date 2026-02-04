import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Black
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

def draw_truchet_unit(x, y, size, variant, weight, alpha, color=(1, 1, 1)):
    """Draws a sophisticated Truchet tile variant with transparency."""
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    ctx.rotate(random.choice([0, math.pi/2, math.pi, 3*math.pi/2]))
    ctx.translate(-size/2, -size/2)
    
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    ctx.set_line_width(weight)

    if variant == 0:  # Orthogonal Arcs (Classic)
        ctx.arc(0, 0, size/2, 0, math.pi/2)
        ctx.stroke()
        ctx.arc(size, size, size/2, math.pi, 3*math.pi/2)
        ctx.stroke()
        
    elif variant == 1:  # Geometric Dithering (Staccato lines)
        steps = 4
        for i in range(steps + 1):
            offset = (i / steps) * size
            ctx.move_to(offset, 0)
            ctx.line_to(offset, size * 0.1)
            ctx.move_to(0, offset)
            ctx.line_to(size * 0.1, offset)
        ctx.stroke()

    elif variant == 2:  # Nested Squares (Hierarchy)
        for i in range(1, 4):
            s = size * (i/4)
            ctx.rectangle(size/2 - s/2, size/2 - s/2, s, s)
            ctx.stroke()

    elif variant == 3:  # Diagonal Logic
        ctx.move_to(0, size/2)
        ctx.line_to(size/2, 0)
        ctx.move_to(size, size/2)
        ctx.line_to(size/2, size)
        ctx.stroke()

    ctx.restore()

# Parameters for Entropic Logic
grid_sizes = [80, 40, 20]  # Multi-layer scale
accent_color = (1.0, 0.2, 0.1) # International Orange
center_x, center_y = width / 2, height / 2

# Iterative Layering
for layer_idx, step in enumerate(grid_sizes):
    for x in range(0, width, step):
        for y in range(0, height, step):
            # Calculate distance from core for density gradient
            dx = (x + step/2) - center_x
            dy = (y + step/2) - center_y
            dist = math.hypot(dx, dy)
            max_dist = math.hypot(width/2, height/2)
            
            # Entropic probability: More likely to draw near center
            norm_dist = dist / max_dist
            probability = 1.0 - (norm_dist * 0.8)
            
            if random.random() < probability:
                # Modulate alpha based on layer and distance
                base_alpha = 0.15 + (0.4 * (1.0 - layer_idx/len(grid_sizes)))
                alpha = base_alpha * (1.2 - norm_dist)
                
                # Weight increases with density
                line_weight = 0.5 + (1.5 * (1.0 - norm_dist))
                
                # Determine color - mostly white, rare chromatic bits at grid intersections
                if random.random() > 0.96:
                    color = accent_color
                    alpha = min(alpha * 2, 1.0)
                    line_weight *= 2
                else:
                    color = (0.9, 0.9, 0.95)
                
                # Choose variant based on distance (order at center, entropy at edges)
                if norm_dist < 0.3:
                    v = random.choice([0, 2]) # Structural
                elif norm_dist < 0.6:
                    v = random.choice([0, 1, 3]) # Transitional
                else:
                    v = random.choice([1, 3]) # Fragmented
                
                draw_truchet_unit(x, y, step, v, line_weight, alpha, color)

# Post-process: Add a "Data Grain" (Stochastic Point Distribution)
for _ in range(2000):
    px = random.uniform(0, width)
    py = random.uniform(0, height)
    # Concentration of grain toward center
    p_dx = px - center_x
    p_dy = py - center_y
    if random.random() > math.hypot(p_dx, p_dy) / max_dist:
        ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.3))
        ctx.rectangle(px, py, 1, 1)
        ctx.fill()

# Final border for Swiss precision
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Clean internal crop
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.set_line_width(1)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()

