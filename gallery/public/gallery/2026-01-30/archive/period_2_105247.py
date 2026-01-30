import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Technical Navy
ctx.set_source_rgb(0.02, 0.05, 0.1)
ctx.paint()

def draw_truchet_cell(x, y, size, style, weight, color):
    """
    Draws a specific Truchet tile variant with precise geometric properties.
    Styles: 0 (Arcs), 1 (Diagonal lines), 2 (Cross-hatch glyph)
    """
    ctx.save()
    ctx.translate(x + size/2, y + size/2)
    # Random orthogonal rotation
    ctx.rotate(random.choice([0, math.pi/2, math.pi, 1.5*math.pi]))
    ctx.translate(-size/2, -size/2)
    
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    ctx.set_line_width(weight)
    ctx.set_line_cap(cairo.LINE_CAP_SQUARE)

    if style == 0:  # Classic Arcs
        ctx.arc(0, 0, size/2, 0, math.pi/2)
        ctx.stroke()
        ctx.arc(size, size, size/2, math.pi, 1.5*math.pi)
        ctx.stroke()
    elif style == 1:  # Geometric Vectors
        ctx.move_to(size/2, 0)
        ctx.line_to(size, size/2)
        ctx.stroke()
        ctx.move_to(0, size/2)
        ctx.line_to(size/2, size)
        ctx.stroke()
    elif style == 2:  # Technical Glyph (Crosses)
        m = size * 0.2
        ctx.move_to(m, size/2); ctx.line_to(size-m, size/2)
        ctx.move_to(size/2, m); ctx.line_to(size/2, size-m)
        ctx.stroke()
        
    ctx.restore()

def generate_layer(grid_size, weight, style_prob, alpha, color_mod=1.0):
    """Generates a structured grid layer with probabilistic variations."""
    cols = width // grid_size
    rows = height // grid_size
    
    for i in range(cols + 1):
        for j in range(rows + 1):
            # Asymmetric distribution: focus density in specific mathematical clusters
            dist_center = math.sqrt(((i/cols)-0.5)**2 + ((j/rows)-0.5)**2)
            if random.random() > (dist_center * 1.2):
                x = i * grid_size
                y = j * grid_size
                
                # Dynamic style selection based on position
                style = 0 if random.random() < style_prob else 1
                if random.random() > 0.95: style = 2 # Rare glyphs
                
                # Color palette: Bone white and Blueprint Cyan
                if random.random() > 0.8:
                    color = (0.0, 0.7, 1.0, alpha) # Technical Cyan
                else:
                    color = (0.9, 0.9, 0.95, alpha) # Bone White
                
                draw_truchet_cell(x, y, grid_size, style, weight, color)

# --- LAYER 1: Large Structural Infrastructure ---
# Heavy lines, large grid, low alpha
ctx.set_operator(cairo.OPERATOR_ADD) # Lighten/Additive blending for depth
generate_layer(grid_size=120, weight=1.5, style_prob=0.8, alpha=0.15)

# --- LAYER 2: Medium Systematic Network ---
# Standard Truchet tiles providing the main visual rhythm
generate_layer(grid_size=40, weight=0.8, style_prob=0.5, alpha=0.4)

# --- LAYER 3: Micro-Data Topography ---
# Fine lines, high frequency, concentrated in 'data clusters'
generate_layer(grid_size=10, weight=0.4, style_prob=0.2, alpha=0.6)

# --- FINAL SYSTEM OVERLAY: Technical Marks ---
# Adding "registration marks" and coordinate lines to reinforce the schematic aesthetic
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.2)
ctx.set_line_width(0.2)

# Horizontal/Vertical coordinate lines
for i in range(0, width, 60):
    ctx.move_to(i, 0); ctx.line_to(i, height); ctx.stroke()
for j in range(0, height, 60):
    ctx.move_to(0, j); ctx.line_to(width, j); ctx.stroke()

# Small "Node" Markers
for _ in range(30):
    nx, ny = random.randint(0, width), random.randint(0, height)
    s = 4
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.move_to(nx - s, ny); ctx.line_to(nx + s, ny)
    ctx.move_to(nx, ny - s); ctx.line_to(nx, ny + s)
    ctx.stroke()
    
    # Tiny numeric labels (simulated)
    if random.random() > 0.7:
        ctx.rectangle(nx + 5, ny + 5, 12, 4)
        ctx.fill()

# Border frame
ctx.set_source_rgba(0.9, 0.9, 1.0, 0.8)
ctx.set_line_width(1.0)
ctx.rectangle(20, 20, width-40, height-40)
ctx.stroke()

# Visual balance - darker vignette to emphasize the center
radial = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
radial.add_color_stop_rgba(0, 0, 0, 0, 0)
radial.add_color_stop_rgba(1, 0.02, 0.05, 0.1, 0.7)
ctx.set_source(radial)
ctx.paint()

