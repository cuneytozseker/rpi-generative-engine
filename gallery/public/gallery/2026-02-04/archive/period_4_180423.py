import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep Brutalist Black
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def get_rd_density(x, y):
    """
    Simulates the visual output of a reaction-diffusion (Turing) pattern 
    using multi-scale harmonic synthesis.
    """
    nx, ny = x * 0.015, y * 0.015
    val = 0
    # Layering frequencies to create the "organic/cellular" look
    val += math.sin(nx) * math.cos(ny)
    val += math.sin(nx * 2.1 + ny * 0.5) * 0.5
    val += math.cos(ny * 1.8 - nx * 0.3) * 0.5
    val += math.sin(math.sqrt(nx**2 + ny**2) * 1.5) * 0.3
    
    # Thresholding to create the crisp binary RD boundaries
    return 1.0 if val > 0.2 else 0.0

def draw_dithered_field(ctx, x, y, w, h, grain_density=0.6):
    """
    Creates a stochastic dithered texture based on the RD density field.
    """
    for _ in range(int(w * h * grain_density)):
        px = random.uniform(x, x + w)
        py = random.uniform(y, y + h)
        
        density = get_rd_density(px, py)
        if density > 0:
            # Chromatic Interference: subtle color shifts at the edges of the "ghost"
            if random.random() > 0.98:
                ctx.set_source_rgba(1, 0.1, 0.4, 0.8) # Neon Magenta
            elif random.random() > 0.98:
                ctx.set_source_rgba(0.1, 0.9, 1, 0.8) # Electric Cyan
            else:
                ctx.set_source_rgba(0.95, 0.95, 0.95, 0.7) # Primary White
            
            ctx.rectangle(px, py, 1.2, 1.2)
            ctx.fill()

def draw_recursive_grid(ctx, x, y, w, h, depth):
    """
    Establishes the 'Ordered' foundation through hierarchical subdivision.
    """
    if depth > 0 and (random.random() > 0.4 or depth > 2):
        nw, nh = w / 2, h / 2
        draw_recursive_grid(ctx, x, y, nw, nh, depth - 1)
        draw_recursive_grid(ctx, x + nw, y, nw, nh, depth - 1)
        draw_recursive_grid(ctx, x, y + nh, nw, nh, depth - 1)
        draw_recursive_grid(ctx, x + nw, y + nh, nw, nh, depth - 1)
    else:
        # Draw the structural cell
        ctx.set_line_width(0.4)
        ctx.set_source_rgba(0.3, 0.3, 0.35, 0.5)
        ctx.rectangle(x, y, w, h)
        ctx.stroke()
        
        # Add internal 'Iterative Pulses' - hierarchical lines
        if w > 20:
            margin = 5
            ctx.set_source_rgba(0.5, 0.5, 0.6, 0.2)
            ctx.move_to(x + margin, y + h/2)
            ctx.line_to(x + w - margin, y + h/2)
            ctx.stroke()

# --- EXECUTION ---

# 1. Background Grid Layer (Ordered Foundation)
ctx.set_line_width(0.5)
draw_recursive_grid(ctx, 40, 40, width-80, height-80, 4)

# 2. The 'Generative Ghost' (Reaction-Diffusion Dithering)
# We focus the entropy towards the center to create a sense of 'decay' from the edges
draw_dithered_field(ctx, 60, 60, width-120, height-120, grain_density=0.8)

# 3. High-Frequency Overlays (Systematic Precision)
# Drawing fine vertical data-lines based on the density field
for i in range(0, width, 12):
    for j in range(0, height, 4):
        d = get_rd_density(i, j)
        if d > 0:
            ctx.set_source_rgba(1, 1, 1, 0.15)
            ctx.set_line_width(0.2)
            ctx.move_to(i, j)
            ctx.line_to(i, j + 3)
            ctx.stroke()

# 4. Focal Gaussian Dissipation (Atmospheric Bleed)
# Simulated by soft, low-alpha circles at high-density zones
for _ in range(40):
    rx = random.uniform(100, width-100)
    ry = random.uniform(100, height-100)
    if get_rd_density(rx, ry) > 0:
        rad = random.uniform(5, 25)
        pat = cairo.RadialGradient(rx, ry, 0, rx, ry, rad)
        pat.add_color_stop_rgba(0, 1, 1, 1, 0.08)
        pat.add_color_stop_rgba(1, 1, 1, 1, 0)
        ctx.set_source(pat)
        ctx.arc(rx, ry, rad, 0, 2 * math.pi)
        ctx.fill()

# 5. Final Swiss Framing
ctx.set_source_rgb(0.9, 0.9, 0.9)
ctx.set_line_width(1.5)
ctx.rectangle(30, 30, width-60, height-60)
ctx.stroke()

# Typography-like visual elements (Non-functional 'labels')
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(8)
ctx.move_to(40, 25)
ctx.show_text("SYSTEM: ORDERED_ENTROPY // REF. RD-092")
ctx.move_to(width-140, height-20)
ctx.show_text("STOCHASTIC_DISSIPATION_V.01")

# IMPORTANT: No surface.write_to_png()
