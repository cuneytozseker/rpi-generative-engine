import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.04, 0.04, 0.05)
ctx.paint()

def draw_grid_lines(ctx, angle, spacing, color, line_width=0.5):
    """Draws a series of parallel lines across the entire canvas at a specific angle."""
    ctx.save()
    ctx.set_source_rgba(*color)
    ctx.set_line_width(line_width)
    
    # Calculate diagonal to ensure coverage during rotation
    diag = math.sqrt(width**2 + height**2)
    
    ctx.translate(width / 2, height / 2)
    ctx.rotate(angle)
    
    for i in range(int(-diag / spacing), int(diag / spacing)):
        x = i * spacing
        ctx.move_to(x, -diag)
        ctx.line_to(x, diag)
        ctx.stroke()
    ctx.restore()

def draw_ui_elements(ctx):
    """Adds pseudo-data annotations and technical markers for the 'cartography' feel."""
    ctx.set_source_rgb(0.9, 0.9, 0.9)
    ctx.set_line_width(1.0)
    
    # Random coordinate markers
    for _ in range(12):
        x, y = random.randint(50, width-50), random.randint(50, height-50)
        size = 4
        # Crosshair
        ctx.move_to(x - size, y)
        ctx.line_to(x + size, y)
        ctx.move_to(x, y - size)
        ctx.line_to(x, y + size)
        ctx.stroke()
        
        # Tiny binary-style blocks
        if random.random() > 0.5:
            ctx.rectangle(x + 6, y - 2, 2, 2)
            ctx.fill()
            ctx.rectangle(x + 6, y + 2, 2, 2)
            ctx.fill()

def spatial_partition_mask(ctx, complexity=5):
    """Creates a fragmented mask to break the grids into segments."""
    for _ in range(complexity):
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        w = random.uniform(50, 200)
        h = random.uniform(50, 200)
        
        # Draw a 'data block'
        ctx.set_source_rgba(1, 1, 1, 0.05)
        ctx.rectangle(x, y, w, h)
        ctx.fill()
        
        # Stroke boundary
        ctx.set_source_rgba(1, 1, 1, 0.2)
        ctx.set_line_width(0.5)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()

# --- Generative Logic ---

# 1. Base Layer: Static fine grid
draw_grid_lines(ctx, math.radians(45), 4, (1, 1, 1, 0.15))

# 2. Moiré Interference Layers
# We use two grids with very slight angular differences (0.5 to 2 degrees)
# This creates the mathematical "beats" or interference patterns.
angle_base = random.uniform(0, math.pi)
angle_offset = 0.025 # The interference frequency controller

# Layer 1: Stark White
draw_grid_lines(ctx, angle_base, 3.5, (1, 1, 1, 0.8), 0.4)

# Layer 2: Cobalt Blue (Dithered feeling via transparency/thickness)
# This creates the secondary interference wave
draw_grid_lines(ctx, angle_base + angle_offset, 3.5, (0.2, 0.4, 1.0, 0.7), 0.4)

# 3. Fragmented Overlays
# Applying a "glitch" or block-based logic to break the continuity
for i in range(8):
    ctx.save()
    # Create a clipping region for local distortion
    rx, ry = random.randint(0, width), random.randint(0, height)
    rw, rh = random.randint(100, 300), random.randint(20, 100)
    ctx.rectangle(rx, ry, rw, rh)
    ctx.clip()
    
    # Redraw a subset of lines at a different frequency within the clip
    draw_grid_lines(ctx, angle_base - angle_offset * 2, 2.5, (1, 1, 1, 0.3), 0.2)
    ctx.restore()

# 4. Circular Harmonics
# Adding a "lens" or "radar" effect to centralize the composition
ctx.set_line_width(0.3)
center_x, center_y = width * 0.5, height * 0.5
for r in range(50, 400, 40):
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.arc(center_x, center_y, r, 0, 2 * math.pi)
    ctx.stroke()
    
    # Add a "scanning" segment
    ctx.set_source_rgba(1, 1, 1, 0.5)
    ctx.arc(center_x, center_y, r, angle_base, angle_base + 0.4)
    ctx.stroke()

# 5. UI and Texture
draw_ui_elements(ctx)

# 6. Final Bitmapped Grain/Dither Effect
# Simulate high-frequency noise by drawing thousands of tiny 1x1 rects
for _ in range(5000):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0, 0.15))
    gx = random.uniform(0, width)
    gy = random.uniform(0, height)
    ctx.rectangle(gx, gy, 1, 1)
    ctx.fill()

# Lateral bar (Swiss Design Hierarchy)
ctx.set_source_rgb(1, 1, 1)
ctx.rectangle(20, 20, 2, height - 40)
ctx.fill()
ctx.rectangle(width - 22, 20, 2, height - 40)
ctx.fill()

# Clean layout border
ctx.set_source_rgba(1, 1, 1, 0.1)
ctx.set_line_width(20)
ctx.rectangle(0, 0, width, height)
ctx.stroke()

