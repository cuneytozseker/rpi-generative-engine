import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Golden Ratio constant
PHI = (1 + 5**0.5) / 2
INV_PHI = 1 / PHI

# Background: Deep charcoal for a high-contrast void
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_diffused_point(x, y, radius, r, g, b, alpha):
    """Creates a soft-field diffusion effect similar to a light leak."""
    grad = cairo.RadialGradient(x, y, 0, x, y, radius)
    grad.add_color_stop_rgba(0, r, g, b, alpha)
    grad.add_color_stop_rgba(1, r, g, b, 0)
    ctx.set_source(grad)
    ctx.arc(x, y, radius, 0, 2 * math.pi)
    ctx.fill()

def draw_logarithmic_grid(x, y, w, h, density=12):
    """Draws a non-linear grid where line frequency increases toward edges."""
    ctx.set_line_width(0.4)
    for i in range(density + 1):
        # Logarithmic distribution mapping 0..1 to 0..1
        t = i / density
        # Bias t toward the center or edges using a sine wave for "acceleration"
        offset = (1 - math.cos(t * math.pi)) / 2
        
        # Vertical lines
        ctx.set_source_rgba(0.8, 0.8, 0.9, 0.15)
        ctx.move_to(x + offset * w, y)
        ctx.line_to(x + offset * w, y + h)
        ctx.stroke()
        
        # Horizontal lines
        ctx.move_to(x, y + offset * h)
        ctx.line_to(x + w, y + offset * h)
        ctx.stroke()

def recursive_subdivision(x, y, w, h, depth, orientation):
    if depth <= 0 or w < 5 or h < 5:
        return

    # Determine split point using Golden Ratio
    # We create a square and a remaining golden rectangle
    if orientation == 'horizontal':
        split = w * INV_PHI
        sq_x, sq_y, sq_w, sq_h = x, y, split, h
        rem_x, rem_y, rem_w, rem_h = x + split, y, w - split, h
        next_orientation = 'vertical'
    else:
        split = h * INV_PHI
        sq_x, sq_y, sq_w, sq_h = x, y, w, split
        rem_x, rem_y, rem_w, rem_h = x, y + split, w, h - split
        next_orientation = 'horizontal'

    # --- DRAW ORDER (The Structure) ---
    ctx.set_line_width(0.7)
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.rectangle(sq_x, sq_y, sq_w, sq_h)
    ctx.stroke()

    # --- DRAW ENTROPY (The Internal Logic) ---
    # Logarithmic internal grids within the primary squares
    if depth % 2 == 0:
        draw_logarithmic_grid(sq_x, sq_y, sq_w, sq_h, density=int(depth * 3))
    
    # Chromatic intensity at specific data intersections
    if depth < 6:
        # Accent color: Spectral Cyan or Electric Orange
        if random.random() > 0.6:
            draw_diffused_point(sq_x + sq_w/2, sq_y + sq_h/2, sq_w * 0.8, 0.0, 0.8, 1.0, 0.1)
        elif random.random() > 0.8:
            draw_diffused_point(sq_x, sq_y, sq_w * 0.5, 1.0, 0.2, 0.1, 0.2)

    # Ultra-thin "blueprint" details
    ctx.set_line_width(0.2)
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.move_to(sq_x, sq_y)
    ctx.line_to(sq_x + sq_w, sq_y + sq_h)
    ctx.stroke()

    # Recursive call
    recursive_subdivision(rem_x, rem_y, rem_w, rem_h, depth - 1, next_orientation)

# Initialization of the system
# We start with two main branches to fill the screen asymmetrically
margin = 40
main_w = (width - margin * 2)
main_h = (height - margin * 2)

# Set global composition bias
ctx.translate(margin, margin)

# Layer 1: Base recursive structure
recursive_subdivision(0, 0, main_w, main_h, 12, 'horizontal')

# Layer 2: Overlapping Inverse Structure for complexity
ctx.set_operator(cairo.OPERATOR_ADD) # Light additive blending
recursive_subdivision(main_w, main_h, -main_w, -main_h, 8, 'vertical')

# Final "Digital Artifact" Noise/Texture
for _ in range(800):
    tx = random.uniform(0, main_w)
    ty = random.uniform(0, main_h)
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.05, 0.2))
    ctx.rectangle(tx, ty, 0.5, 0.5)
    ctx.fill()

# Geometric focus points
ctx.set_operator(cairo.OPERATOR_OVER)
for i in range(5):
    f_x = random.uniform(0, main_w)
    f_y = random.uniform(0, main_h)
    ctx.set_source_rgba(0, 0.9, 1.0, 0.6)
    ctx.arc(f_x, f_y, 1.5, 0, 2*math.pi)
    ctx.fill()
    # High frequency circles
    ctx.set_line_width(0.1)
    ctx.set_source_rgba(1, 1, 1, 0.3)
    ctx.arc(f_x, f_y, 10, 0, 2*math.pi)
    ctx.stroke()

