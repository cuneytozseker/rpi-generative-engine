import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format for radial symmetry
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Matte Black
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

def draw_modulated_grid(cx, cy, rotation, num_lines, radius, color, alpha, weight):
    """
    Draws a grid of lines that converge toward a central axis, 
    modulated by a rotation parameter to induce Moiré interference.
    """
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rotation)
    
    ctx.set_source_rgba(color[0], color[1], color[2], alpha)
    ctx.set_line_width(weight)
    
    # Non-linear scaling: lines are denser towards the center
    # Using a power function to distribute angles
    for i in range(num_lines):
        # Normalize i to -1 to 1
        t = (i / (num_lines - 1)) * 2 - 1
        # Apply power to pull values toward 0 (the center)
        # Sign preserved to keep distribution across the diameter
        sign = 1 if t >= 0 else -1
        offset = sign * (abs(t) ** 1.5) * radius
        
        # Draw vertical-ish lines across the circular field
        length = math.sqrt(max(0, radius**2 - offset**2))
        ctx.move_to(offset, -length)
        ctx.line_to(offset, length)
        ctx.stroke()
        
    ctx.restore()

def draw_accent_elements(cx, cy, radius):
    """
    Adds Swiss-style geometric accents to break the symmetry
    and provide focal points of high saturation.
    """
    # International Orange accent
    accent_color = (1.0, 0.25, 0.0) 
    
    ctx.save()
    ctx.translate(cx, cy)
    
    # Small heavy-weight square as a rhythmic interruption
    ctx.set_source_rgb(*accent_color)
    side = 12
    ctx.rectangle(-radius - 20, -radius - 20, side, side)
    ctx.fill()
    
    # A single precise 'data' line
    ctx.set_line_width(1.5)
    ctx.move_to(-radius, radius + 30)
    ctx.line_to(radius, radius + 30)
    ctx.stroke()
    
    # Label-like geometry
    ctx.rectangle(radius + 10, -radius, 2, radius * 2)
    ctx.fill()
    
    ctx.restore()

# --- Main Composition ---

center_x, center_y = width / 2, height / 2
base_radius = 240
line_count = 180

# Layer 1: The Base Grid (Static reference)
# High density, low opacity creates the "optical gray"
draw_modulated_grid(
    center_x, center_y, 
    rotation=0, 
    num_lines=line_count, 
    radius=base_radius, 
    color=(0.9, 0.9, 0.9), 
    alpha=0.3, 
    weight=0.5
)

# Layer 2: The Interfering Grid (Slightly rotated)
# The 1.5 to 3 degree offset is the "sweet spot" for moiré patterns
draw_modulated_grid(
    center_x, center_y, 
    rotation=math.radians(2.5), 
    num_lines=line_count, 
    radius=base_radius, 
    color=(1.0, 1.0, 1.0), 
    alpha=0.4, 
    weight=0.5
)

# Layer 3: Recursive Central Detail
# Nested smaller grid with different density to create hierarchical depth
draw_modulated_grid(
    center_x, center_y, 
    rotation=math.radians(-5.0), 
    num_lines=60, 
    radius=base_radius * 0.4, 
    color=(1.0, 1.0, 1.0), 
    alpha=0.6, 
    weight=0.8
)

# Layer 4: Mathematical Texture (Radial harmonics)
# Connecting the grids with subtle radial ticks
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.set_line_width(0.3)
for i in range(72):
    angle = (i / 72) * math.pi * 2
    inner = base_radius * 0.95
    outer = base_radius * 1.05
    ctx.move_to(center_x + math.cos(angle) * inner, center_y + math.sin(angle) * inner)
    ctx.line_to(center_x + math.cos(angle) * outer, center_y + math.sin(angle) * outer)
    ctx.stroke()

# Layer 5: Visual Accents
draw_accent_elements(center_x, center_y, base_radius)

# Final Framing: Minimalist border
ctx.set_source_rgb(0.8, 0.8, 0.8)
ctx.set_line_width(1)
margin = 40
ctx.rectangle(margin, margin, width - margin*2, height - margin*2)
ctx.stroke()

# IMPORTANT: No surface.write_to_png()
