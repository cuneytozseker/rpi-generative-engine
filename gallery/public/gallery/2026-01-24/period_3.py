import cairo
import math
import random

# Setup
width, height = 800, 800
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep technical indigo
ctx.set_source_rgb(0.02, 0.03, 0.05)
ctx.paint()

def draw_moire_field(ctx, cx, cy, radius, angle, spacing, alpha):
    """Generates a field of parallel lines to create interference."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    
    ctx.set_source_rgba(1, 1, 1, alpha)
    ctx.set_line_width(0.5)
    
    # Draw lines across the clipping area
    num_lines = int(radius * 2 / spacing)
    for i in range(-num_lines, num_lines):
        x = i * spacing
        ctx.move_to(x, -radius)
        ctx.line_to(x, radius)
        ctx.stroke()
    ctx.restore()

def draw_technical_annotation(ctx, x, y, size):
    """Draws small blueprint-like markers and 'data' nodes."""
    ctx.save()
    ctx.translate(x, y)
    
    # Small crosshair
    ctx.set_source_rgb(1, 1, 1)
    ctx.set_line_width(0.8)
    ctx.move_to(-size, 0)
    ctx.line_to(size, 0)
    ctx.move_to(0, -size)
    ctx.line_to(0, size)
    ctx.stroke()
    
    # Binary 'data' blocks (Swiss style hierarchy)
    ctx.set_line_width(0.3)
    for i in range(3):
        for j in range(3):
            if random.random() > 0.5:
                ctx.rectangle(size + 5 + (i * 4), -size + (j * 4), 2, 2)
                ctx.fill()
    ctx.restore()

def draw_recursive_subdivision(ctx, x, y, size, depth):
    """Partitions space based on local density logic."""
    if depth <= 0 or random.random() < 0.3:
        # Draw a technical node at this quadrant
        draw_technical_annotation(ctx, x + size/2, y + size/2, size * 0.1)
        
        # Subtle border for some cells
        if random.random() > 0.7:
            ctx.set_source_rgba(1, 1, 1, 0.15)
            ctx.set_line_width(0.5)
            ctx.rectangle(x, y, size, size)
            ctx.stroke()
        return

    half = size / 2
    draw_recursive_subdivision(ctx, x, y, half, depth - 1)
    draw_recursive_subdivision(ctx, x + half, y, half, depth - 1)
    draw_recursive_subdivision(ctx, x, y + half, half, depth - 1)
    draw_recursive_subdivision(ctx, x + half, y + half, half, depth - 1)

# --- 1. Base Layer: The Moiré Interference ---
# Center the interaction slightly off-canvas for dynamic asymmetry
center_x, center_y = width * 0.45, height * 0.55

# Primary rotating grid
draw_moire_field(ctx, center_x, center_y, 1000, math.radians(12), 4.0, 0.4)

# Secondary rotating grid - slightly different angle and frequency to create beat patterns
draw_moire_field(ctx, center_x, center_y, 1000, math.radians(13.5), 4.2, 0.4)

# --- 2. Structural Layer: Recursive Mapping ---
# Use a quadtree-style distribution to create 'information clusters'
draw_recursive_subdivision(ctx, 50, 50, 700, 4)

# --- 3. Detail Layer: Precision Markers ---
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1.0)

# Vertical ruler logic
for i in range(0, height, 40):
    ctx.move_to(10, i)
    ctx.line_to(20 if i % 80 == 0 else 15, i)
    ctx.stroke()

# Horizontal ruler logic
for i in range(0, width, 40):
    ctx.move_to(i, height - 10)
    ctx.line_to(i, height - (20 if i % 80 == 0 else 15))
    ctx.stroke()

# --- 4. Focal Elements: Interconnected Nodes ---
nodes = [(random.randint(100, 700), random.randint(100, 700)) for _ in range(12)]
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.set_line_width(0.4)

# Connect nodes based on proximity (Graph-based logic)
for i, n1 in enumerate(nodes):
    for n2 in nodes[i+1:]:
        dist = math.sqrt((n1[0]-n2[0])**2 + (n1[1]-n2[1])**2)
        if dist < 250:
            ctx.move_to(n1[0], n1[1])
            ctx.line_to(n2[0], n2[1])
            ctx.stroke()
            
    # Draw the node itself
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.arc(n1[0], n1[1], 1.5, 0, 2 * math.pi)
    ctx.fill()
    
    # Label simulated metadata
    if random.random() > 0.6:
        ctx.set_source_rgba(1, 1, 1, 0.5)
        ctx.rectangle(n1[0] + 5, n1[1] - 10, 30, 2)
        ctx.fill()

# --- 5. Final Systematic Polish ---
# Vignette-like technical frame
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

# Clean border
ctx.set_source_rgb(1, 1, 1)
ctx.set_line_width(1)
ctx.rectangle(40, 40, width-80, height-80)
ctx.stroke()

# Metadata block in bottom right
ctx.rectangle(width-150, height-70, 100, 20)
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.fill()
ctx.set_source_rgba(1, 1, 1, 1)
ctx.set_line_width(0.5)
ctx.move_to(width-145, height-60)
ctx.line_to(width-60, height-60)
ctx.stroke()
