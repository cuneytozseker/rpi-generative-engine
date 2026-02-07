import cairo
import math
import random

# Setup
width, height = 600, 600 # Square format works better for polar transformations
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background - Deep charcoal for high contrast
ctx.set_source_rgb(0.02, 0.02, 0.03)
ctx.paint()

def draw_deformed_glyph(ctx, x, y, size, angle, entropy):
    """Draws a Swiss-style geometric glyph with entropic distortion."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(angle)
    
    # Base geometry: A rectangular block or line
    if random.random() > 0.3:
        # Structured rectangle
        h = size * (1.0 + entropy * random.uniform(-0.5, 2.0))
        w = size * 0.2
        ctx.rectangle(-w/2, -h/2, w, h)
    else:
        # Circular element
        ctx.arc(0, 0, size * 0.4, 0, 2 * math.pi)
    
    ctx.fill()
    ctx.restore()

def get_spectral_color(t):
    """Returns a high-saturation spectral color based on t (0 to 1)."""
    # Mimics a heatmap: Deep Blue -> Cyan -> Magenta -> Bright Orange
    if t < 0.25:
        return (0, 4*t, 1) # Blue to Cyan
    elif t < 0.5:
        return (0, 1, 1 - 4*(t-0.25)) # Cyan to Green
    elif t < 0.75:
        return (4*(t-0.5), 0, 1) # Blue to Magenta
    else:
        return (1, 1 - 2*(t-0.75), 0.2) # Magenta to Yellow/Orange

# Parameters
center_x, center_y = width / 2, height / 2
rings = 18
slices = 48
max_radius = width * 0.45
attractor_x, attractor_y = width * 0.7, height * 0.3

# 1. Background Grid: Subtle radial lines
ctx.set_line_width(0.5)
for i in range(slices):
    angle = (i / slices) * 2 * math.pi
    ctx.move_to(center_x, center_y)
    ctx.line_to(center_x + math.cos(angle) * max_radius, center_y + math.sin(angle) * max_radius)
    ctx.set_source_rgba(1, 1, 1, 0.05)
    ctx.stroke()

# 2. Main Generative Logic: Polar Grid Transformation
for r_idx in range(1, rings + 1):
    r_norm = r_idx / rings
    radius = r_norm * max_radius
    
    # Entropic factor increases with radius (ordered core -> chaotic edge)
    entropy = math.pow(r_norm, 2.5) 
    
    for s_idx in range(slices):
        angle = (s_idx / slices) * 2 * math.pi
        
        # Scalar Field: Distance to an attractor point distorts the coordinates
        curr_x = center_x + math.cos(angle) * radius
        curr_y = center_y + math.sin(angle) * radius
        dist_to_attractor = math.sqrt((curr_x - attractor_x)**2 + (curr_y - attractor_y)**2)
        distortion = math.exp(-dist_to_attractor / 150.0) * 40.0
        
        # Calculate final coordinates with distortion and entropy
        phi = angle + (distortion * 0.05) + (random.uniform(-0.1, 0.1) * entropy)
        distorted_r = radius + (distortion * 2.0) + (random.uniform(-20, 20) * entropy)
        
        final_x = center_x + math.cos(phi) * distorted_r
        final_y = center_y + math.sin(phi) * distorted_r
        
        # Visual Styling
        # Color based on angle (spectral) and proximity to attractor
        color_t = (angle / (2 * math.pi) + (dist_to_attractor / 500)) % 1.0
        r, g, b = get_spectral_color(color_t)
        
        # Alpha modulation: core is opaque, edges are ethereal
        alpha = 0.9 - (r_norm * 0.5)
        
        # "Digital Smear" - Draw trailing lines for outer elements
        if entropy > 0.4:
            ctx.set_source_rgba(r, g, b, alpha * 0.2)
            ctx.set_line_width(0.5)
            ctx.move_to(final_x, final_y)
            ctx.line_to(final_x + (final_x - center_x) * entropy * 0.2, 
                        final_y + (final_y - center_y) * entropy * 0.2)
            ctx.stroke()

        # Draw the primary geometric primitive
        ctx.set_source_rgba(r, g, b, alpha)
        glyph_size = (1.5 + (1.0 - r_norm) * 8.0) * (1.0 + distortion * 0.02)
        draw_deformed_glyph(ctx, final_x, final_y, glyph_size, phi, entropy)

# 3. Overlays: Geometric Swiss elements for "Ordered" feel
ctx.set_source_rgba(1, 1, 1, 0.8)
ctx.set_line_width(1.0)
# Small crosshairs at cardinal points
for i in range(4):
    a = i * (math.pi / 2)
    cx = center_x + math.cos(a) * (max_radius + 20)
    cy = center_y + math.sin(a) * (max_radius + 20)
    ctx.move_to(cx - 5, cy); ctx.line_to(cx + 5, cy)
    ctx.move_to(cx, cy - 5); ctx.line_to(cx, cy + 5)
    ctx.stroke()

# Framing circle
ctx.set_source_rgba(1, 1, 1, 0.15)
ctx.arc(center_x, center_y, max_radius + 40, 0, 2 * math.pi)
ctx.stroke()

# 4. Focal "Data" points
for _ in range(12):
    px = random.uniform(50, width-50)
    py = random.uniform(50, height-50)
    ctx.set_source_rgba(1, 1, 1, 0.6)
    ctx.arc(px, py, 1, 0, 2 * math.pi)
    ctx.fill()
    # Tiny numeric labels (simulated)
    ctx.rectangle(px + 4, py - 2, 10, 1)
    ctx.fill()

# Final Polish: Variable Line Weight Grid
ctx.set_source_rgba(1, 1, 1, 0.03)
for x in range(0, width, 40):
    ctx.move_to(x, 0)
    ctx.line_to(x, height)
    ctx.stroke()
