import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Constants
PHI = (1 + 5**0.5) / 2
ITERATIONS = 14
BG_COLOR = (0.02, 0.02, 0.03)
ACCENT_COLOR = (0.0, 0.9, 0.8) # Spectral Cyan
CONTRAST_COLOR = (1.0, 0.2, 0.4) # Vibrant Magenta

# Background
ctx.set_source_rgb(*BG_COLOR)
ctx.paint()

def draw_digital_dither(ctx, x, y, w, h, density=0.3):
    """Adds a 'bitmapped' constraint texture to a region."""
    step = 4
    ctx.set_line_width(0.5)
    for i in range(0, int(w), step):
        for j in range(0, int(h), step):
            if random.random() < density:
                # Draw a tiny 'pixel' or cross
                ctx.move_to(x + i, y + j)
                ctx.line_to(x + i + 1, y + j)
                ctx.stroke()

def draw_vector_flow(ctx, x, y, w, h):
    """Adds directional progression lines within a box."""
    ctx.set_line_width(0.3)
    segments = 10
    for i in range(segments):
        offset = (i / segments) * h
        ctx.move_to(x, y + offset)
        # S-curve flow
        ctx.curve_to(x + w * 0.3, y + offset, 
                     x + w * 0.7, y + offset + (random.uniform(-10, 10)), 
                     x + w, y + offset)
        ctx.set_source_rgba(1, 1, 1, 0.15)
        ctx.stroke()

def recursive_subdivision(x, y, w, h, depth):
    if depth <= 0:
        return

    # Draw the frame
    ctx.set_line_width(0.7 / (depth * 0.5 + 1))
    
    # Visual logic: atmospheric vs granular
    # Some boxes get gradients, some get 'bitmaps'
    chance = random.random()
    
    if chance > 0.7:
        # Atmospheric Gradient
        grad = cairo.LinearGradient(x, y, x + w, y + h)
        alpha = 0.1 / (15 - depth)
        grad.add_color_stop_rgba(0, *ACCENT_COLOR, alpha)
        grad.add_color_stop_rgba(1, *CONTRAST_COLOR, 0)
        ctx.set_source(grad)
        ctx.rectangle(x, y, w, h)
        ctx.fill()
    elif chance > 0.4:
        # Granular Precision (Dithering)
        ctx.set_source_rgba(0.8, 0.8, 1.0, 0.2)
        draw_digital_dither(ctx, x, y, w, h, density=0.2)
    
    # Systematic border
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()

    # Subdivision Logic (Golden Ratio)
    if w > h:
        new_w = w / PHI
        # Rectilinear progression
        recursive_subdivision(x, y, new_w, h, depth - 1)
        recursive_subdivision(x + new_w, y, w - new_w, h, depth - 1)
    else:
        new_h = h / PHI
        recursive_subdivision(x, y, w, new_h, depth - 1)
        recursive_subdivision(x, y + new_h, w, h - new_h, depth - 1)

# Initialize a foundational vector field (low-frequency movement)
for _ in range(30):
    ctx.set_source_rgba(0.2, 0.4, 1.0, 0.05)
    ctx.set_line_width(random.uniform(0.5, 2.0))
    y_pos = random.uniform(0, height)
    ctx.move_to(0, y_pos)
    ctx.line_to(width, y_pos + random.uniform(-100, 100))
    ctx.stroke()

# Create the recursive structure
# Start with a margin for Swiss layout precision
margin = 40
recursive_subdivision(margin, margin, width - margin*2, height - margin*2, ITERATIONS)

# Add "Global Luminosity" overlay
overlay_grad = cairo.RadialGradient(width*0.8, height*0.2, 10, width*0.8, height*0.2, 400)
overlay_grad.add_color_stop_rgba(0, 0, 0.8, 1.0, 0.08)
overlay_grad.add_color_stop_rgba(1, 0, 0, 0, 0)
ctx.set_source(overlay_grad)
ctx.rectangle(0, 0, width, height)
ctx.fill()

# Geometric Annotations (Digital Markers)
ctx.set_source_rgba(1, 1, 1, 0.6)
ctx.set_line_width(1.0)
for _ in range(12):
    rx, ry = random.uniform(0, width), random.uniform(0, height)
    size = 3
    # Draw crosshair markers
    ctx.move_to(rx - size, ry)
    ctx.line_to(rx + size, ry)
    ctx.move_to(rx, ry - size)
    ctx.line_to(rx, ry + size)
    ctx.stroke()

# Final atmospheric dust (High-frequency noise)
for _ in range(800):
    ctx.set_source_rgba(1, 1, 1, random.uniform(0.1, 0.3))
    px, py = random.uniform(0, width), random.uniform(0, height)
    ctx.rectangle(px, py, 0.5, 0.5)
    ctx.fill()

