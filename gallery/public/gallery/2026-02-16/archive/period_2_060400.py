import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Technical Deep Blue
ctx.set_source_rgb(0.02, 0.05, 0.1)
ctx.paint()

def draw_truchet_tile(x, y, size, variation, weight, alpha):
    """Draws a complex Truchet tile with concentric internal geometry."""
    ctx.save()
    ctx.translate(x, y)
    
    # Random rotation for the tile orientation
    rotation = random.choice([0, 90, 180, 270])
    ctx.translate(size/2, size/2)
    ctx.rotate(math.radians(rotation))
    ctx.translate(-size/2, -size/2)

    ctx.set_line_width(weight)
    ctx.set_source_rgba(0.2, 0.8, 1.0, alpha)

    if variation == 0:
        # Dual Arcs (Standard) with concentric internal lines
        num_lines = 4
        for i in range(num_lines):
            offset = (i + 1) * (size / (num_lines + 1))
            # Top-left arc
            ctx.arc(0, 0, offset, 0, math.pi / 2)
            ctx.stroke()
            # Bottom-right arc
            ctx.arc(size, size, offset, math.pi, 3 * math.pi / 2)
            ctx.stroke()
    elif variation == 1:
        # Cross-hatch diagonal variant
        num_lines = 6
        for i in range(num_lines):
            step = (i / num_lines) * size
            ctx.move_to(step, 0)
            ctx.line_to(size, size - step)
            ctx.stroke()
            ctx.move_to(0, step)
            ctx.line_to(size - step, size)
            ctx.stroke()
    else:
        # Structured Entropy: Rectangular subdivision
        for _ in range(3):
            sub_w = random.uniform(2, size/2)
            ctx.rectangle(random.uniform(0, size-sub_w), random.uniform(0, size-sub_w), sub_w, 1)
            ctx.fill()

    ctx.restore()

def draw_metadata(x, y, text):
    """Draws small typographic markers reminiscent of technical blueprints."""
    ctx.select_font_face("Monospace", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(6)
    ctx.set_source_rgba(0.7, 0.9, 1.0, 0.4)
    ctx.move_to(x + 2, y + 8)
    ctx.show_text(text)

# --- GENERATIVE LAYERS ---

# Layer 1: Large, faint background grid
grid_size_lg = 120
for i in range(int(width / grid_size_lg) + 1):
    for j in range(int(height / grid_size_lg) + 1):
        ctx.set_source_rgba(1, 1, 1, 0.03)
        ctx.set_line_width(0.5)
        ctx.rectangle(i * grid_size_lg, j * grid_size_lg, grid_size_lg, grid_size_lg)
        ctx.stroke()

# Layer 2: Primary Truchet System (Dense)
grid_size = 40
for x in range(0, width, grid_size):
    for y in range(0, height, grid_size):
        # Determine density based on a pseudo-random cluster logic
        dist_to_center = math.sqrt((x - width/2)**2 + (y - height/2)**2)
        probability = math.cos(dist_to_center * 0.01) * 0.5 + 0.5
        
        if random.random() < probability:
            draw_truchet_tile(x, y, grid_size, random.randint(0, 1), 0.5, 0.6)
            
            # Occasional "Metadata" labels
            if random.random() > 0.92:
                draw_metadata(x, y, f"SEC_{x//grid_size}.{y//grid_size}")

# Layer 3: Overlapping "Moiré" Layer (Offset grid)
ctx.set_operator(cairo.OPERATOR_ADD) # Additive transparency for vibration
grid_size_sm = 20
for x in range(0, width, grid_size_sm):
    for y in range(0, height, grid_size_sm):
        if (x + y) % 3 == 0:
            ctx.set_source_rgba(0.1, 0.4, 0.8, 0.15)
            ctx.arc(x, y, 1, 0, 2 * math.pi)
            ctx.fill()
            
            # Fine noise lines
            if random.random() > 0.98:
                draw_truchet_tile(x, y, grid_size_sm, 2, 0.2, 0.8)

# Layer 4: Structural Border and Coordinates
ctx.set_operator(cairo.OPERATOR_OVER)
margin = 20
ctx.set_source_rgba(1, 1, 1, 0.3)
ctx.set_line_width(1)
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Coordinate markers on axis
for i in range(margin, width - margin, 50):
    ctx.move_to(i, margin - 5)
    ctx.line_to(i, margin)
    ctx.stroke()
    draw_metadata(i, margin - 15, f"{i:03d}")

# Final "Glitch" elements - Horizontal scanlines
for _ in range(12):
    y_pos = random.randint(0, height)
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.set_line_width(0.3)
    ctx.move_to(0, y_pos)
    ctx.line_to(width, y_pos)
    ctx.stroke()

# Signature detail
ctx.set_source_rgba(1, 1, 1, 0.5)
ctx.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(width - 80, height - 10)
ctx.show_text("TRUCHET_v0.4.SYS")

