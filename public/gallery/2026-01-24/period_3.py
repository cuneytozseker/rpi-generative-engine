import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep charcoal for high-contrast brutalist base
ctx.set_source_rgb(0.02, 0.02, 0.02)
ctx.paint()

def draw_line_field(ctx, angle, spacing, weight, color=(1, 1, 1, 0.5)):
    """
    Generates a dense field of parallel lines across the entire canvas.
    Used to create the primary interference layers.
    """
    ctx.save()
    ctx.set_source_rgba(*color)
    ctx.set_line_width(weight)
    
    # Translate to center to rotate around the middle
    ctx.translate(width / 2, height / 2)
    ctx.rotate(angle)
    
    # Calculate span needed to cover the diagonal of the canvas
    diagonal = math.sqrt(width**2 + height**2)
    steps = int(diagonal / spacing) + 2
    
    for i in range(-steps, steps):
        x = i * spacing
        ctx.move_to(x, -diagonal)
        ctx.line_to(x, diagonal)
    
    ctx.stroke()
    ctx.restore()

def recursive_subdivision(x, y, w, h, depth):
    """
    Recursive function to create a Swiss-style hierarchical grid.
    Places localized interference patterns in specific modules.
    """
    if depth > 4 or (depth > 1 and random.random() > 0.7):
        # Draw a localized dense grid in this sector
        if random.random() > 0.3:
            draw_sector_grid(x, y, w, h, depth)
        return

    # Split logic (Golden Ratio-ish or Halves)
    if w > h:
        split = w * (0.382 if random.random() > 0.5 else 0.5)
        recursive_subdivision(x, y, split, h, depth + 1)
        recursive_subdivision(x + split, y, w - split, h, depth + 1)
    else:
        split = h * (0.382 if random.random() > 0.5 else 0.5)
        recursive_subdivision(x, y, w, split, depth + 1)
        recursive_subdivision(x, y + split, w, h - split, depth + 1)

def draw_sector_grid(x, y, w, h, depth):
    """
    Adds local geometric weight to a grid cell.
    """
    ctx.save()
    # Masking to the cell
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    
    # Modulated density based on recursion depth
    density = 2 + depth
    ctx.set_source_rgba(1, 1, 1, 0.15)
    ctx.set_line_width(0.5)
    
    # Internal grid lines
    for i in range(1, density):
        # Vertical
        vx = x + (i * w / density)
        ctx.move_to(vx, y)
        ctx.line_to(vx, y + h)
        # Horizontal
        vy = y + (i * h / density)
        ctx.move_to(x, vy)
        ctx.line_to(x + w, vy)
    ctx.stroke()
    
    # Symbolic mark (Brutalist element)
    if random.random() > 0.6:
        ctx.set_source_rgba(1, 1, 1, 0.8)
        ctx.rectangle(x + 5, y + 5, 4, 4)
        ctx.fill()
        
    ctx.restore()

# --- GENERATIVE EXECUTION ---

# 1. Primary Moiré System
# Two layers of extremely dense lines with a subtle angular offset
base_angle = math.pi / 4
offset = 0.015  # The "slow rotation" difference (approx 0.8 degrees)

# Layer A: Static Grid
draw_line_field(ctx, base_angle, spacing=2.5, weight=0.3, color=(1, 1, 1, 0.4))

# Layer B: Offset Grid creating Moiré interference patterns
draw_line_field(ctx, base_angle + offset, spacing=2.4, weight=0.3, color=(1, 1, 1, 0.4))

# 2. Secondary Moiré System (Orthogonal)
# Adds complexity to the interference fringes
draw_line_field(ctx, base_angle + math.pi/2, spacing=12, weight=0.5, color=(1, 1, 1, 0.2))
draw_line_field(ctx, base_angle + math.pi/2 + (offset * 2), spacing=12.2, weight=0.5, color=(1, 1, 1, 0.2))

# 3. Hierarchical Grid Overlay
# Applying Swiss design principles of subdivision and negative space
random.seed(42) # For compositional balance
recursive_subdivision(20, 20, width - 40, height - 40, 0)

# 4. Final Accent: Structural Framing
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(1.0)
ctx.move_to(20, 20)
ctx.line_to(width-20, 20)
ctx.stroke()

# Create a "Technical Data" block (Typography simulation)
def draw_data_block(ctx, x, y):
    ctx.set_source_rgb(1, 1, 1)
    for i in range(5):
        w = random.uniform(10, 40)
        ctx.rectangle(x, y + (i * 6), w, 2)
        ctx.fill()

draw_data_block(ctx, 30, height - 60)

# Final Polish: Add a subtle vignette through transparency to center the focus
radial = cairo.RadialGradient(width/2, height/2, 100, width/2, height/2, 400)
radial.add_color_stop_rgba(0, 1, 1, 1, 0)
radial.add_color_stop_rgba(1, 0, 0, 0, 0.3)
ctx.set_source(radial)
ctx.paint()

