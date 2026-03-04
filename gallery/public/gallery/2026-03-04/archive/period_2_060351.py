import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Charcoal
ctx.set_source_rgb(0.05, 0.05, 0.07)
ctx.paint()

def polar_transform(x, y, tx, ty, strength=0.15):
    """
    Maps Cartesian coordinates to a distorted Polar space.
    x: normalized width (0-1), y: normalized height (0-1)
    """
    # Map x to angle, y to radius
    angle = x * 2 * math.pi
    radius = y * 250
    
    # Apply radial distortion (Hierarchical Entropy)
    distortion = math.sin(angle * 4 + y * 10) * strength * radius
    radius += distortion
    
    px = tx + radius * math.cos(angle)
    py = ty + radius * math.sin(angle)
    return px, py

def draw_recursive_unit(x, y, w, h, depth):
    if depth > 4:
        return

    # Deterministic randomness for visual consistency in hierarchy
    state = random.getstate()
    random.seed(int((x + y) * 1000))
    
    # Decide whether to subdivide or draw
    should_subdivide = depth < 2 or (random.random() > 0.4 and depth < 4)
    
    cx, cy = 300, 240 # Center of projection

    if should_subdivide:
        nw, nh = w / 2, h / 2
        draw_recursive_unit(x, y, nw, nh, depth + 1)
        draw_recursive_unit(x + nw, y, nw, nh, depth + 1)
        draw_recursive_unit(x, y + nh, nw, nh, depth + 1)
        draw_recursive_unit(x + nw, y + nh, nw, nh, depth + 1)
    else:
        # Draw a geometric motif mapped to polar space
        # Calculate momentum for color: center-weighted
        dist_from_center = math.sqrt((x-0.5)**2 + (y-0.5)**2)
        momentum = 1.0 - dist_from_center
        
        # Color logic: Neutral base with high-chroma spectral accents
        if random.random() > 0.85:
            # Saturated "Momentum" colors (Cyan/Magenta/Yellow)
            colors = [(0.0, 0.9, 1.0), (1.0, 0.1, 0.5), (1.0, 0.8, 0.0)]
            r, g, b = random.choice(colors)
            alpha = 0.8
        else:
            # Neutral Swiss tones
            c = 0.7 + random.random() * 0.3
            r, g, b = c, c, c
            alpha = 0.2
            
        ctx.set_source_rgba(r, g, b, alpha)
        ctx.set_line_width(0.5 / (depth + 1))
        
        # Draw distorted grid lines within the cell
        steps = 4
        for i in range(steps + 1):
            # Vertical-ish flow lines (Radial)
            ctx.move_to(*polar_transform(x + (i/steps)*w, y, cx, cy))
            for j in range(1, 6):
                ctx.line_to(*polar_transform(x + (i/steps)*w, y + (j/5)*h, cx, cy))
            ctx.stroke()
            
            # Horizontal-ish flow lines (Angular)
            ctx.move_to(*polar_transform(x, y + (i/steps)*h, cx, cy))
            for j in range(1, 6):
                ctx.line_to(*polar_transform(x + (j/5)*w, y + (i/steps)*h, cx, cy))
            ctx.stroke()

        # Add "Atmospheric Diffusion" - subtle glow layers
        if depth == 3:
            ctx.set_source_rgba(r, g, b, 0.03)
            for s in range(3):
                p1 = polar_transform(x, y, cx, cy)
                p2 = polar_transform(x+w, y, cx, cy)
                p3 = polar_transform(x+w, y+h, cx, cy)
                p4 = polar_transform(x, y+h, cx, cy)
                ctx.move_to(*p1)
                ctx.line_to(*p2)
                ctx.line_to(*p3)
                ctx.line_to(*p4)
                ctx.close_path()
                ctx.fill()
    
    random.setstate(state)

# Execute the Generative System
# We map a 1.0 x 1.0 abstract grid into the polar function
draw_recursive_unit(0, 0, 1.0, 1.0, 0)

# Overlay: Precision Vector Field Elements
# Adding sharp, high-contrast markers to ground the entropy
for _ in range(120):
    rx = random.random()
    ry = random.random()
    cx, cy = 300, 240
    
    px, py = polar_transform(rx, ry, cx, cy)
    
    # Draw small cross-hairs or ticks
    size = 2.5
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.set_line_width(0.7)
    ctx.move_to(px - size, py)
    ctx.line_to(px + size, py)
    ctx.move_to(px, py - size)
    ctx.line_to(px, py + size)
    ctx.stroke()

# Final structural framing: concentric guide rings (Swiss precision)
ctx.set_source_rgba(1, 1, 1, 0.05)
ctx.set_line_width(1)
for r in [50, 100, 150, 200, 250]:
    ctx.arc(300, 240, r, 0, 2 * math.pi)
    ctx.stroke()

# Subtle typographic hint (abstract Swiss geometry)
ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.set_source_rgba(1, 1, 1, 0.4)
ctx.move_to(20, 460)
ctx.show_text("POLAR_SUBDIVISION_V.01 // GRID_ENTROPY")
