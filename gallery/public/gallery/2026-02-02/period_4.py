import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Obsidian
ctx.set_source_rgb(0.04, 0.04, 0.05)
ctx.paint()

def draw_modulated_grid(ctx, cx, cy, angle, spacing, num_lines, color, alpha, weight_factor):
    """
    Draws a grid of lines with modulated weights and a slight stochastic curve 
    to simulate flow and mechanical precision.
    """
    r, g, b = color
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(angle)
    
    for i in range(-num_lines // 2, num_lines // 2):
        x = i * spacing
        
        # Non-linear line weight: thinner at edges, thicker towards center
        dist_norm = abs(i) / (num_lines / 2)
        weight = (1.2 - dist_norm) * weight_factor
        
        # Set color with layered transparency
        ctx.set_source_rgba(r, g, b, alpha * (1.0 - dist_norm * 0.5))
        ctx.set_line_width(weight)
        
        # Draw line with subtle organic "shimmy" using a sine wave
        ctx.move_to(x, -height)
        for segment in range(-int(height), int(height), 20):
            # Stochastic flow: slight perturbation in the x-coordinate
            shift = math.sin(segment * 0.01 + i * 0.5) * 2.0
            ctx.line_to(x + shift, segment)
        
        ctx.stroke()
    ctx.restore()

# Parameters for Kinetic Equilibrium
center_x, center_y = width / 2, height / 2
line_count = 120
base_spacing = 6.5
rotation_offset = math.radians(2.5) # The critical angle for Moiré interference

# 1. Atmospheric Diffusion Layer (Lower opacity, wider lines)
# Creating a "temporal echo" or motion blur effect
for i in range(3):
    fade_angle = rotation_offset * (i * 0.2)
    draw_modulated_grid(ctx, center_x, center_y, fade_angle, base_spacing, 
                        line_count, (0.3, 0.3, 0.35), 0.1, 0.8)

# 2. Primary Moiré System
# Grid A: The "Anchor" (Warm Parchment tone)
draw_modulated_grid(ctx, center_x, center_y, 0, base_spacing, 
                    line_count, (0.94, 0.94, 0.91), 0.7, 0.5)

# Grid B: The "Kinetic" (Slightly rotated to create interference patterns)
draw_modulated_grid(ctx, center_x, center_y, rotation_offset, base_spacing, 
                    line_count, (0.94, 0.94, 0.91), 0.7, 0.5)

# 3. Spectral Pulses (Chromatic aberration/High-contrast accents)
# Subtle cyan and magenta shifts at the fringes of the interference
ctx.set_operator(cairo.OPERATOR_ADD) # Lighten overlapping areas

# Cyan pulse
draw_modulated_grid(ctx, center_x + 2, center_y, rotation_offset * 1.05, base_spacing, 
                    line_count // 2, (0.0, 0.8, 0.9), 0.15, 0.3)
# Magenta pulse
draw_modulated_grid(ctx, center_x - 2, center_y, rotation_offset * 0.95, base_spacing, 
                    line_count // 2, (0.9, 0.1, 0.4), 0.15, 0.3)

ctx.set_operator(cairo.OPERATOR_OVER)

# 4. Geometric Overlays (Swiss Design precision elements)
# Adding a central focal structure to ground the entropy
def draw_focal_element(ctx, x, y, size):
    ctx.set_source_rgba(1, 1, 1, 0.9)
    ctx.set_line_width(0.5)
    
    # Crosshair
    ctx.move_to(x - size, y)
    ctx.line_to(x + size, y)
    ctx.move_to(x, y - size)
    ctx.line_to(x, y + size)
    ctx.stroke()
    
    # Nested circles with Golden Ratio spacing
    for i in range(1, 4):
        radius = size * (1.618 ** -i)
        ctx.arc(x, y, radius, 0, 2 * math.pi)
        ctx.stroke()

draw_focal_element(ctx, center_x, center_y, 180)

# 5. Framing and Hierarchy
# Vertical bars to emphasize the "staccato" motion
ctx.set_source_rgba(0.04, 0.04, 0.05, 0.8)
ctx.rectangle(0, 0, 40, height)
ctx.rectangle(width - 40, 0, 40, height)
ctx.fill()

# Fine hairline borders
ctx.set_source_rgba(0.94, 0.94, 0.91, 0.4)
ctx.set_line_width(0.25)
ctx.move_to(50, 20)
ctx.line_to(width - 50, 20)
ctx.move_to(50, height - 20)
ctx.line_to(width - 50, height - 20)
ctx.stroke()

# Final subtle noise/texture could be added here, but Cairo is best at clean lines.
# The Moiré itself provides the visual complexity.
