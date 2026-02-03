import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep charcoal for a technical blueprint feel
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def draw_truchet_tile(x, y, size, orientation, weight, color):
    """Draws a multi-arc Truchet tile with transparency."""
    ctx.set_line_width(weight)
    ctx.set_source_rgba(*color)
    
    # Orientation 0: Top-left and bottom-right arcs
    # Orientation 1: Top-right and bottom-left arcs
    if orientation == 0:
        # Top-left
        ctx.arc(x, y, size / 2, 0, 0.5 * math.pi)
        ctx.stroke()
        # Bottom-right
        ctx.arc(x + size, y + size, size / 2, math.pi, 1.5 * math.pi)
        ctx.stroke()
    else:
        # Top-right
        ctx.arc(x + size, y, size / 2, 0.5 * math.pi, math.pi)
        ctx.stroke()
        # Bottom-left
        ctx.arc(x, y + size, size / 2, 1.5 * math.pi, 2 * math.pi)
        ctx.stroke()

def draw_annotation(x, y, size=4):
    """Adds small technical markers (crosses) to simulate a schematic."""
    ctx.set_source_rgba(0.8, 0.9, 1.0, 0.4)
    ctx.set_line_width(0.5)
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

# --- GENERATIVE LAYERING SYSTEM ---

# Layer 1: The "Ghost" Grid (Large, faint background structure)
cell_size_lg = 120
for i in range(int(width / cell_size_lg) + 1):
    for j in range(int(height / cell_size_lg) + 1):
        x, y = i * cell_size_lg, j * cell_size_lg
        orient = random.randint(0, 1)
        # Use mathematical modulation for line weight based on distance from center
        dist = math.sqrt((x - width/2)**2 + (y - height/2)**2)
        weight = 0.5 + (dist / 200)
        draw_truchet_tile(x, y, cell_size_lg, orient, weight, (0.2, 0.3, 0.4, 0.2))

# Layer 2: The Primary Fabric (Medium grid, varied density)
cell_size_md = 40
for i in range(int(width / cell_size_md)):
    for j in range(int(height / cell_size_md)):
        x, y = i * cell_size_md, j * cell_size_md
        
        # Determine density/probability based on a wave function
        prob = (math.sin(i * 0.2) * math.cos(j * 0.2) + 1) / 2
        
        if prob > 0.3:
            orient = random.randint(0, 1)
            # Create a "technical" gradient effect using line weight
            weight = 0.8 if prob < 0.7 else 2.5
            alpha = 0.3 if prob < 0.7 else 0.6
            color = (0.9, 0.9, 1.0, alpha)
            draw_truchet_tile(x, y, cell_size_md, orient, weight, color)
            
            # Occasionally add a secondary nested arc for complexity
            if prob > 0.8:
                draw_truchet_tile(x, y, cell_size_md * 0.6, orient, 0.5, (1.0, 0.4, 0.4, 0.5))

# Layer 3: High-Frequency Detail (Smallest grid, precision lines)
cell_size_sm = 20
for i in range(int(width / cell_size_sm)):
    for j in range(int(height / cell_size_sm)):
        x, y = i * cell_size_sm, j * cell_size_sm
        
        # Sparse placement for high-frequency "data" points
        if random.random() > 0.85:
            orient = random.randint(0, 1)
            draw_truchet_tile(x, y, cell_size_sm, orient, 0.3, (1, 1, 1, 0.8))
        
        # Grid annotations at regular intervals
        if i % 4 == 0 and j % 4 == 0:
            draw_annotation(x, y)

# Final Polish: Linear "Scanner" lines to emphasize the technical aesthetic
ctx.set_line_width(0.2)
ctx.set_source_rgba(0.5, 0.7, 1.0, 0.1)
for k in range(0, height, 4):
    ctx.move_to(0, k)
    ctx.line_to(width, k)
    ctx.stroke()

# Border/Frame for Swiss containment
ctx.set_line_width(20)
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Subtle framing line
ctx.set_line_width(1)
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.rectangle(10, 10, width-20, height-20)
ctx.stroke()
