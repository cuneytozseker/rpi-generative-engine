import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Abyss
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_interference_grid(cx, cy, num_lines, rotation_offset, color, line_width):
    """Draws a radial grid of lines to create Moiré patterns when overlapped."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rotation_offset)
    
    r_max = math.sqrt(width**2 + height**2)
    angle_step = (2 * math.pi) / num_lines
    
    ctx.set_source_rgba(*color)
    ctx.set_line_width(line_width)
    
    for i in range(num_lines):
        angle = i * angle_step
        ctx.move_to(0, 0)
        # Using a slight curve to create more complex interference
        ctx.line_to(math.cos(angle) * r_max, math.sin(angle) * r_max)
        ctx.stroke()
        
    ctx.restore()

def draw_thermal_gradient():
    """Adds a subtle 'optical fog' gradient to represent energy intensity."""
    grad = cairo.RadialGradient(width/2, height/2, 50, width/2, height/2, width*0.8)
    grad.add_color_stop_rgba(0, 0.1, 0.05, 0.2, 0.3)  # Indigo core
    grad.add_color_stop_rgba(0.7, 0.05, 0.02, 0.1, 0.1) # Fade to dark
    grad.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(grad)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

def recursive_subdivision(x, y, w, h, depth):
    """Hierarchical partitioning to anchor the composition in Swiss design logic."""
    if depth > 4 or (depth > 1 and random.random() > 0.7):
        # Draw micro-punctuations or data marks at leaf nodes
        if random.random() > 0.5:
            ctx.set_source_rgba(1, 0.4, 0.1, 0.6) # Thermal Orange
            ctx.arc(x + w/2, y + h/2, 1.5, 0, 2*math.pi)
            ctx.fill()
        return

    # Draw subdivision lines
    ctx.set_source_rgba(1, 1, 1, 0.1)
    ctx.set_line_width(0.5)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Split
    if w > h:
        nw = w * random.uniform(0.3, 0.7)
        recursive_subdivision(x, y, nw, h, depth + 1)
        recursive_subdivision(x + nw, y, w - nw, h, depth + 1)
    else:
        nh = h * random.uniform(0.3, 0.7)
        recursive_subdivision(x, y, w, nh, depth + 1)
        recursive_subdivision(x, y + nh, w, h - nh, depth + 1)

# 1. Establish Hierarchical Grid
recursive_subdivision(20, 20, width-40, height-40, 0)

# 2. Apply Atmospheric Flux
draw_thermal_gradient()

# 3. Primary Moiré Interference Systems
# We use additive blending to make intersections glow
ctx.set_operator(cairo.OPERATOR_ADD)

# Set A: Cool Indigo Grid
draw_interference_grid(
    width * 0.45, height * 0.5, 
    num_lines=360, 
    rotation_offset=0, 
    color=(0.2, 0.3, 0.8, 0.4), 
    line_width=0.4
)

# Set B: Warm Offset Grid (The "Beat" frequency generator)
# Rotating this slightly creates the signature Moiré "petals"
draw_interference_grid(
    width * 0.55, height * 0.5, 
    num_lines=362, # Slightly different count for frequency interference
    rotation_offset=math.radians(1.5), 
    color=(0.9, 0.4, 0.1, 0.3), 
    line_width=0.4
)

# 4. Center Focal Point - Structured Geometry
ctx.set_operator(cairo.OPERATOR_OVER)
ctx.set_source_rgba(1, 1, 1, 0.9)
ctx.set_line_width(1.2)
# Golden ratio based framing
side = 120
ctx.rectangle(width/2 - side/2, height/2 - side/2, side, side)
ctx.stroke()

# Micro-fine details: Cross-hatching in corners for texture
def draw_texture_hash(x, y, size):
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(0.3)
    for i in range(0, size, 4):
        ctx.move_to(x + i, y)
        ctx.line_to(x + i, y + size)
        ctx.move_to(x, y + i)
        ctx.line_to(x + size, y + i)
    ctx.stroke()

draw_texture_hash(30, 30, 40)
draw_texture_hash(width-70, height-70, 40)

# Final spectral depth: A soft vignette
vignette = cairo.RadialGradient(width/2, height/2, width/4, width/2, height/2, width/1.5)
vignette.add_color_stop_rgba(0, 0, 0, 0, 0)
vignette.add_color_stop_rgba(1, 0, 0, 0, 0.6)
ctx.set_source(vignette)
ctx.paint()

# Swiss-style "Data" Labels
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(40, height - 40)
ctx.show_text("REF: MOIRÉ_INTERFERENCE_09")
ctx.move_to(40, height - 30)
ctx.show_text("SYS: RADIATING_ANGULAR_GRID // OFFSET: 1.5 DEG")

# Small technical square markers
for i in range(3):
    ctx.rectangle(width - 50, 40 + (i*15), 10, 2)
    ctx.fill()

