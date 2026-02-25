import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width * 0.45, height * 0.5  # Slightly off-center for asymmetry
num_rings = 40
num_slices = 90
swiss_red = (0.89, 0.12, 0.09)
white = (0.95, 0.95, 0.95)
grey = (0.4, 0.4, 0.4)

def get_distortion(r, theta, strength=15):
    """Creates a vector-flow influence based on harmonic frequencies."""
    # Combining sine waves to simulate a complex, non-linear flow field
    d_r = math.sin(theta * 3 + r * 0.02) * strength
    d_theta = math.cos(r * 0.05) * (strength / (r + 10)) * 2
    return d_r, d_theta

def polar_to_cartesian(r, theta, dr=0, dt=0):
    """Maps polar coordinates to screen space with distortion."""
    x = center_x + (r + dr) * math.cos(theta + dt)
    y = center_y + (r + dr) * math.sin(theta + dt)
    return x, y

# 1. THE FOUNDATIONAL ASYMMETRIC GRID
# Drawing subtle radial guidelines to establish the "Swiss" structure
ctx.set_line_width(0.3)
ctx.set_source_rgba(*grey, 0.3)
for i in range(num_rings):
    r = i * 12
    ctx.new_path()
    for j in range(num_slices + 1):
        theta = (j / num_slices) * math.pi * 2
        x, y = polar_to_cartesian(r, theta)
        if j == 0: ctx.move_to(x, y)
        else: ctx.line_to(x, y)
    ctx.stroke()

# 2. THE VECTOR FLOW FIELD (Structured Entropy)
# These lines represent the transition from order to organic flow
for i in range(1, num_rings, 2):
    r_base = i * 12
    # Varying line weight based on distance from center (radial hierarchy)
    ctx.set_line_width(0.5 + (i / num_rings) * 1.2)
    
    for j in range(num_slices):
        theta = (j / num_slices) * math.pi * 2
        
        # Calculate distortion for this point
        dr, dt = get_distortion(r_base, theta, strength=25)
        x, y = polar_to_cartesian(r_base, theta, dr, dt)
        
        # Draw "hair-thin filaments" as short segments following the flow
        ctx.set_source_rgba(*white, random.uniform(0.2, 0.7))
        
        # Create a dashed/stippled effect
        if random.random() > 0.3:
            # Flow direction segment
            dr2, dt2 = get_distortion(r_base + 5, theta + 0.05, strength=25)
            x2, y2 = polar_to_cartesian(r_base, theta, dr2, dt2)
            
            ctx.move_to(x, y)
            ctx.line_to(x2, y2)
            ctx.stroke()

# 3. HARMONIC SUBDIVISIONS & PUNCTUATED SYMBOLS
# Adding dense clusters and specific data-markers (Swiss Red)
for i in range(0, num_rings, 4):
    for j in range(0, num_slices, 6):
        r = i * 12
        theta = (j / num_slices) * math.pi * 2
        dr, dt = get_distortion(r, theta, strength=25)
        x, y = polar_to_cartesian(r, theta, dr, dt)
        
        # Selective Chromatic Punctuation
        if (i + j) % 13 == 0:
            # Drawing a 'Swiss cross' style marker or a data-point
            ctx.set_source_rgb(*swiss_red)
            ctx.set_line_width(2.0)
            size = 4
            ctx.move_to(x - size, y)
            ctx.line_to(x + size, y)
            ctx.move_to(x, y - size)
            ctx.line_to(x, y + size)
            ctx.stroke()
        elif (i * j) % 7 == 0:
            # Small stippled dots for texture
            ctx.set_source_rgba(*white, 0.8)
            ctx.arc(x, y, 1.2, 0, math.pi * 2)
            ctx.fill()

# 4. OVERLAYING THE VOID
# Using large, low-opacity radial gradients to suggest 3D terrain/depth
# This creates the "Emergent Topography" mentioned in the brief
for i in range(5):
    grad_r = random.randint(100, 300)
    gx, gy = polar_to_cartesian(grad_r, random.uniform(0, math.pi*2))
    
    pat = cairo.RadialGradient(gx, gy, 0, gx, gy, random.randint(50, 150))
    pat.add_color_stop_rgba(0, 1, 1, 1, 0.05) # Subtle white glow
    pat.add_color_stop_rgba(1, 0, 0, 0, 0)
    
    ctx.set_source(pat)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

# 5. MARGINALIA (The Systematic Edge)
# Adding small geometric annotations at the corners to reinforce the design grid
ctx.set_source_rgb(*grey)
ctx.set_line_width(1)
margin = 20
ctx.move_to(margin, margin)
ctx.line_to(margin + 40, margin)
ctx.move_to(margin, margin)
ctx.line_to(margin, margin + 40)
ctx.stroke()

ctx.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.move_to(width - 120, height - margin)
ctx.show_text("SYS_ENTROPY_V.01 // 45.1N_9.2E")

# Final touch: A single, long high-contrast line cutting across the composition
ctx.set_source_rgba(*swiss_red, 0.6)
ctx.set_line_width(0.5)
ctx.move_to(0, height * 0.8)
ctx.line_to(width, height * 0.2)
ctx.stroke()
