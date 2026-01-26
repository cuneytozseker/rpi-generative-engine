import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep architectural black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_truchet_cell(x, y, size, rotation, complexity, color_rgba):
    """
    Draws a sophisticated Truchet tile variation with nested arcs.
    Complexity determines the number of concentric lines.
    """
    r, g, b, a = color_rgba
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    ctx.rotate(rotation * (math.pi / 2))
    ctx.translate(-size/2, -size/2)
    
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(0.5)
    
    # Smith's Truchet variant with structural modulation
    steps = complexity
    for i in range(1, steps + 1):
        dist = (i / steps) * (size / 2)
        
        # Arc 1: Top-left
        ctx.arc(0, 0, dist, 0, math.pi / 2)
        ctx.stroke()
        
        # Arc 2: Bottom-right
        ctx.arc(size, size, dist, math.pi, 1.5 * math.pi)
        ctx.stroke()
        
    # Add a structural 'anchor' dot at corners for Swiss grid feel
    if complexity > 3:
        ctx.set_source_rgba(r, g, b, a * 1.5)
        dot_size = 0.8
        ctx.arc(0, 0, dot_size, 0, 2 * math.pi)
        ctx.fill()
        ctx.arc(size, size, dot_size, 0, 2 * math.pi)
        ctx.fill()
        
    ctx.restore()

def recursive_grid(x, y, size, depth):
    """
    Subdivides space to create a hierarchical structural framework.
    """
    # Use a flow-field logic to determine rotation
    # Based on position to create "Kinetic" movement
    angle_func = math.sin(x * 0.01) + math.cos(y * 0.01)
    rotation = int(abs(angle_func * 2)) % 4
    
    # Probability of subdivision decreases with depth
    if depth < 3 and (random.random() < 0.6 / (depth + 1) or depth < 1):
        new_size = size / 2
        recursive_grid(x, y, new_size, depth + 1)
        recursive_grid(x + new_size, y, new_size, depth + 1)
        recursive_grid(x, y + new_size, new_size, depth + 1)
        recursive_grid(x + new_size, y + new_size, new_size, depth + 1)
    else:
        # Layer 1: Structural Base (White/Grey)
        draw_truchet_cell(x, y, size, rotation, 4, (0.8, 0.8, 0.9, 0.3))
        
        # Layer 2: Kinetic Detail (Accent or High Contrast)
        # Shifted slightly for "Vibrational" effect
        if random.random() > 0.4:
            accent_color = random.choice([
                (0.9, 0.1, 0.2, 0.5), # Brutalist Red
                (0.1, 0.6, 0.9, 0.5), # Blueprint Cyan
                (1.0, 1.0, 1.0, 0.6)  # High White
            ])
            draw_truchet_cell(x, y, size, (rotation + 1) % 4, 2, accent_color)

# 1. Background Grid Texture
ctx.set_source_rgba(0.2, 0.2, 0.3, 0.1)
ctx.set_line_width(0.2)
grid_spacing = 20
for i in range(0, width, grid_spacing):
    ctx.move_to(i, 0)
    ctx.line_to(i, height)
    ctx.stroke()
for j in range(0, height, grid_spacing):
    ctx.move_to(0, j)
    ctx.line_to(width, j)
    ctx.stroke()

# 2. Draw the hierarchical tiles
base_tile_size = 120
for i in range(0, width, base_tile_size):
    for j in range(0, height, base_tile_size):
        recursive_grid(i, j, base_tile_size, 0)

# 3. Global Flow Overlay (Vector-guided flow field)
# Adds "emergent density" through thousands of hairline strokes
ctx.set_operator(cairo.OPERATOR_ADD) # Light accumulation
for _ in range(400):
    tx = random.uniform(0, width)
    ty = random.uniform(0, height)
    ctx.set_source_rgba(0.5, 0.7, 1.0, 0.05)
    ctx.set_line_width(0.15)
    
    ctx.move_to(tx, ty)
    # Parametric trajectory influenced by the "global field"
    for _ in range(10):
        angle = math.sin(tx * 0.005) * math.cos(ty * 0.005) * math.pi * 2
        tx += math.cos(angle) * 15
        ty += math.sin(angle) * 15
        ctx.line_to(tx, ty)
    ctx.stroke()

# 4. Swiss Typography/Labeling (Visual Element)
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgba(1, 1, 1, 0.8)

# Margin metadata
ctx.move_to(20, height - 20)
ctx.show_text("STRUCTURAL_BLUEPRINT_V.04")
ctx.move_to(width - 140, height - 20)
ctx.show_text("KINETIC_FLOW_SYS // 2024")

# Small coordinate markers
for x_mark in [20, width-20]:
    for y_mark in [20, height-20]:
        ctx.set_line_width(1)
        ctx.move_to(x_mark - 5, y_mark)
        ctx.line_to(x_mark + 5, y_mark)
        ctx.move_to(x_mark, y_mark - 5)
        ctx.line_to(x_mark, y_mark + 5)
        ctx.stroke()

# Final atmospheric pass: Vignette-like density
radial = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
radial.add_color_stop_rgba(0, 0, 0, 0, 0)
radial.add_color_stop_rgba(1, 0, 0, 0, 0.4)
ctx.set_source(radial)
ctx.paint()
