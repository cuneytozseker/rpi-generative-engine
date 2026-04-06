import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_modular_grid(ctx, angle, spacing, line_width, color, alpha, shift_x=0, shift_y=0):
    """
    Draws a systematic grid of lines with modulated thickness and 
    dash patterns to create complex interference.
    """
    ctx.save()
    ctx.translate(width / 2 + shift_x, height / 2 + shift_y)
    ctx.rotate(angle)
    
    r, g, b = color
    ctx.set_source_rgba(r, g, b, alpha)
    
    # Range covers the diagonal to ensure full screen coverage after rotation
    extent = int(math.sqrt(width**2 + height**2))
    
    for i in range(-extent // 2, extent // 2, spacing):
        # Systematic line weight modulation based on distance from center
        dist_factor = abs(i) / (extent / 2)
        current_weight = line_width * (1.2 - dist_factor)
        ctx.set_line_width(current_weight)
        
        # Dash pattern frequency modulation: creates a secondary 'texture' 
        # that dissolves towards the edges (Digital Lithograph effect)
        dash_size = 2 + (10 * dist_factor)
        if i % (spacing * 4) == 0:
            ctx.set_dash([dash_size, 2])
        else:
            ctx.set_dash([])
            
        ctx.move_to(i, -extent // 2)
        ctx.line_to(i, extent // 2)
        ctx.stroke()
        
    ctx.restore()

def draw_radial_echo(ctx, center_x, center_y, rings, color):
    """
    Adds a radial intensity field to ground the composition, 
    mimicking an 'underlying noise function'.
    """
    ctx.save()
    r, g, b = color
    for i in range(rings):
        radius = (i * 25)
        opacity = 0.15 * (1 - (i / rings))
        ctx.set_source_rgba(r, g, b, opacity)
        ctx.set_line_width(0.5)
        ctx.arc(center_x, center_y, radius, 0, 2 * math.pi)
        ctx.stroke()
    ctx.restore()

# --- Execution ---

# 1. Background Texture: Subtle radial structure
draw_radial_echo(ctx, width/2, height/2, 15, (0.4, 0.6, 1.0))

# 2. Primary Moiré System
# We use two grids with a very slight angular offset (2.5 degrees)
# and a tiny spatial translation to trigger the interference patterns.

# Grid A: The "Cool" Static Field
draw_modular_grid(
    ctx, 
    angle=math.radians(45), 
    spacing=6, 
    line_width=0.7, 
    color=(0.1, 0.8, 0.9), # Cyan spectral tone
    alpha=0.6
)

# Grid B: The "Warm" Interference Field
# Rotated slightly differently to create the 'Moiré' blooms
draw_modular_grid(
    ctx, 
    angle=math.radians(47.5), 
    spacing=6, 
    line_width=0.7, 
    color=(0.9, 0.2, 0.4), # Magenta spectral tone
    alpha=0.6,
    shift_x=2
)

# 3. Orthogonal Modular Layer
# Adding a vertical grid of 'glyphs' (short segments) to add density
ctx.save()
ctx.set_line_width(1.2)
ctx.set_source_rgba(1, 1, 1, 0.8) # Stark White for structural hierarchy
grid_step = 30
for x in range(0, width + grid_step, grid_step):
    for y in range(0, height + grid_step, grid_step):
        # Stochastic density: only draw based on a mathematical threshold
        if (math.sin(x * 0.01) + math.cos(y * 0.01)) > 0.5:
            length = 8 * math.sin((x + y) * 0.05)
            ctx.move_to(x, y - length)
            ctx.line_to(x, y + length)
            ctx.stroke()
            
            # Small "bits" for Brutalist texture
            if random.random() > 0.9:
                ctx.rectangle(x-2, y-2, 4, 4)
                ctx.fill()
ctx.restore()

# 4. Final Swiss Detail: Frame and Labeling
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(1)
margin = 20
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# Aesthetic "Metadata" glyphs in corners
def draw_marker(x, y):
    size = 10
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()

draw_marker(margin, margin)
draw_marker(width - margin, margin)
draw_marker(margin, height - margin)
draw_marker(width - margin, height - margin)

# Final high-frequency overlay for 'digital lithograph' feel
ctx.set_source_rgba(1, 1, 1, 0.05)
for _ in range(1000):
    ctx.rectangle(random.randint(0, width), random.randint(0, height), 1, 1)
    ctx.fill()

