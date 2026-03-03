import cairo
import math
import random

# Setup
width, height = 600, 480
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# Background: Deep Vellum/Charcoal aesthetic
ctx.set_source_rgb(0.05, 0.05, 0.05)
ctx.paint()

# Configuration
center_x, center_y = width / 2, height / 2
rings = 18
slices = 48
max_radius = min(width, height) * 0.45

def polar_to_cartesian(r, theta):
    return center_x + r * math.cos(theta), center_y + r * math.sin(theta)

# Helper for Drawing Swiss-style Glyphs
def draw_glyph(x, y, size, rotation, color):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rotation)
    r, g, b, a = color
    ctx.set_source_rgba(r, g, b, a)
    
    glyph_type = random.random()
    if glyph_type < 0.4:  # Precision Cross
        ctx.set_line_width(0.5)
        ctx.move_to(-size, 0)
        ctx.line_to(size, 0)
        ctx.move_to(0, -size)
        ctx.line_to(0, size)
        ctx.stroke()
    elif glyph_type < 0.7:  # Solid Block
        ctx.rectangle(-size/2, -size/2, size, size)
        ctx.fill()
    else:  # Open Circle
        ctx.set_line_width(0.8)
        ctx.arc(0, 0, size/2, 0, 2 * math.pi)
        ctx.stroke()
    ctx.restore()

# 1. Structural Layer: Logarithmic Grid with Radial Distortion
# We map a Swiss modular grid into polar space with an exponential bias
for i in range(rings):
    # Logarithmic spacing creates depth and tension
    r = max_radius * (math.log(i + 1) / math.log(rings + 1))
    
    # Line weight modulation based on radius
    ctx.set_line_width(0.3 + (i / rings) * 1.2)
    
    # Introduce a "spiral distortion" to the grid
    distortion = (i / rings) * math.pi * 0.25
    
    for j in range(slices):
        theta = (j / slices) * 2 * math.pi + distortion
        theta_next = ((j + 1) / slices) * 2 * math.pi + distortion
        
        # Color: High contrast neutral with subtle transparency
        alpha = 0.2 + (i / rings) * 0.5
        ctx.set_source_rgba(0.9, 0.9, 0.9, alpha)
        
        # Draw radial segment
        p1_x, p1_y = polar_to_cartesian(r, theta)
        p2_x, p2_y = polar_to_cartesian(r * 1.1, theta)
        ctx.move_to(p1_x, p1_y)
        ctx.line_to(p2_x, p2_y)
        ctx.stroke()
        
        # Draw arc segment (only on every 2nd ring for "negative space" rhythm)
        if i % 2 == 0:
            ctx.arc(center_x, center_y, r, theta, theta_next)
            ctx.stroke()

# 2. Stochastic Layer: Vector Flow Field Particles
# Where the grid "breaks" into kinetic motion
num_particles = 1200
for _ in range(num_particles):
    # Distribution weighted towards the outer edges
    norm_r = math.sqrt(random.random())
    r = norm_r * max_radius * 1.2
    angle = random.uniform(0, 2 * math.pi)
    
    # Vector Flow Field: Angle is influenced by the polar coordinates
    # Creating a swirling motion that fights the rigid grid
    flow_force = math.sin(r * 0.02) * 2.0
    distorted_angle = angle + flow_force
    
    x, y = polar_to_cartesian(r, distorted_angle)
    
    # Computational Hatching / Optical Dither
    # Colors: Primarily off-white, with strategic "Chromatic Bursts" (Swiss Red)
    if random.random() > 0.98:
        color = (1.0, 0.2, 0.1, 0.9) # International Orange/Red
        size = 3.0
    else:
        # Greyscale variation
        val = random.uniform(0.7, 1.0)
        color = (val, val, val, random.uniform(0.1, 0.6))
        size = random.uniform(0.5, 1.5)
    
    # Only draw if within reasonable bounds to maintain axial focus
    if 50 < r < max_radius * 1.3:
        draw_glyph(x, y, size, distorted_angle, color)

# 3. Geometric Anchors: Axial Symmetry Elements
# Large, rigid structures to ground the composition
ctx.set_line_width(1.0)
for side in [-1, 1]: # Left/Right symmetry
    anchor_r = max_radius * 0.6
    anchor_theta = math.pi/2 + (side * math.pi/4)
    ax, ay = polar_to_cartesian(anchor_r, anchor_theta)
    
    ctx.set_source_rgba(1, 1, 1, 0.8)
    # Vertical "Swiss" rule lines
    ctx.move_to(ax, ay - 40)
    ctx.line_to(ax, ay + 40)
    ctx.stroke()
    
    # Density markers
    for step in range(5):
        ctx.rectangle(ax + (side * 10), ay - 40 + (step * 20), 4, 4)
        ctx.fill()

# 4. Center Focal Point: Recursive Partitioning
# A tight inner core of order
ctx.set_line_width(0.5)
for i in range(5):
    inner_r = 10 + (i * 8)
    ctx.set_source_rgba(1, 1, 1, 1.0 - (i * 0.2))
    ctx.arc(center_x, center_y, inner_r, 0, 2 * math.pi)
    ctx.stroke()
    
    # Crosshair
    ctx.move_to(center_x - 5, center_y)
    ctx.line_to(center_x + 5, center_y)
    ctx.move_to(center_x, center_y - 5)
    ctx.line_to(center_x, center_y + 5)
    ctx.stroke()

# Final Polish: Subtle noise grain / scanlines across the whole canvas
ctx.set_line_width(0.5)
for i in range(0, height, 4):
    ctx.set_source_rgba(1, 1, 1, 0.03)
    ctx.move_to(0, i)
    ctx.line_to(width, i)
    ctx.stroke()
